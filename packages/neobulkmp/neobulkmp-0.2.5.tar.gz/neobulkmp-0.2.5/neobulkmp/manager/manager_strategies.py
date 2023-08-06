import operator
import os
import psutil
import graphio
import math
import humanfriendly
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .manager import Manager


class StrategyBase:
    cache_storage_warning_limit: int = 80
    cache_storage_clogged_limit: int = 90
    max_advantage_cache_graphobjects_count: int = 1000000
    target_advantage_cache_graphobjects_count: int = 500000
    graphio_batchsize: int = 50000

    cache_storage_total = None

    # On large server with huge core counts, the sourcing workers can fly the cache quickly into the ceilling. thats why we create a default max amount of sourcing workers
    max_sourcing_workers = None

    def __init__(self, manager: "Manager"):
        self.manager = manager
        self._cache_untouched = True
        self._cache_first_hit_time = 0
        if self.cache_storage_total is None:
            self.cache_storage_total = getattr(psutil.virtual_memory(), "total") * 0.80
        else:
            self.cache_storage_total = humanfriendly.parse_size(
                self.cache_storage_total
            )

    def amount_loading_cores(self) -> int:
        if (
            self.manager.statistics.is_sourcing_phase_done()
            or self.manager.statistics.get_cache_storage_used()
            >= self.manager.cache_size
            or self.manager.statistics.get_cache_storage_level() in ["ORANGE", "RED"]
        ):
            return self.manager.cpu_count
        c = round(self.manager.cpu_count - self.amount_sourcing_cores())
        if c == 0:
            c = 1
        return c * 2

    def amount_loading_nodes_cores(self) -> int:
        c = round(self.amount_loading_cores() * 0.9)
        if c == 0:
            c = 1
        # We can take more cores as available because loading processes are waiting a lot for the db and wont use any cpu time during that
        return math.ceil(c * 1.5)

    def amount_loading_rels_cores(self) -> int:
        # if we ended the sourcing phase (all sourcing workers finished) we first load all nodesets and after that all relsets can load without draining)
        if (
            self.manager.statistics.get_count_left_sourcing_workers() == 0
            and len(self.manager.cache.list_SetsMeta(graphio.NodeSet)) > 0
        ):
            return 0
        # if we are low on nodeSets in the cache we can start more RelSet loaders
        nodesets_cores_needed: int = len(
            self.manager.cache.list_SetsMeta(graphio.NodeSet)
            + self.manager.manager_loading._get_workers(
                status=("initial", "running"),
                tag=self.manager.manager_loading.worker_tag_nodesets,
            )
        )
        if nodesets_cores_needed < self.amount_loading_nodes_cores():
            return self.amount_loading_cores() - nodesets_cores_needed
            # else
        # By default we apply 50% of available loading cores to RelSets (or at least one Core)
        c = round(self.amount_loading_cores() * 0.5)
        if c == 0:
            c = 1
        return math.ceil(c)

    def amount_sourcing_cores(self) -> int:
        c = 0
        if self._cache_untouched:
            # when noting is in cache yet we only let one parser work.
            # this way we can carefully increase parser workers without cloging the cache
            if self.manager.statistics.get_cached_graphobjects_total() > 0:
                # first objects arrive in cache.
                # from here on we can increase the amount of parsing workers
                self._cache_untouched = False
                self._cache_first_hit_time = (
                    self.manager.statistics.start_time - time.time()
                )
                if self._cache_first_hit_time < 3:
                    # we want at least a cooldown time of 3 sec for spawning new parsers
                    self._cache_first_hit_time = 3
                self._sourcing_cool_down_target_time = (
                    time.time() + self._cache_first_hit_time
                )
            c = 1
        else:
            if self.manager.statistics.get_cache_storage_level() == "RED":
                return 0
            if self._sourcing_cool_down_target_time < time.time():
                # Reset timer
                self._sourcing_cool_down_target_time = (
                    time.time() + self._cache_first_hit_time
                )
                mean_exceed = (
                    self.manager.statistics.get_mean_graph_objects_cache_exceedes_loaded_count()
                )
                if mean_exceed < (self.target_advantage_cache_graphobjects_count):
                    c = self._last_amount_sourcing_cores + 1
                elif mean_exceed > (self.target_advantage_cache_graphobjects_count):
                    c = self._last_amount_sourcing_cores - 1
            else:
                c = self._last_amount_sourcing_cores
        max_c = math.floor(self.manager.cpu_count * 0.6)
        if c > max_c:
            c = max_c
        if c < 1:
            c = 1
        self._last_amount_sourcing_cores = c

        return c
