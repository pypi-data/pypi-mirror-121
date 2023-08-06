import operator
import os
import psutil
import graphio
import math
import humanfriendly
import time
import multiprocessing
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .manager import Manager


class StrategyBase:
    max_processes_count: int = multiprocessing.cpu_count()
    cache_storage_warning_limit: int = 80
    cache_storage_clogged_limit: int = 90
    max_graphobjects_count_in_cache: int = 1000000
    min_graphobjects_count_in_cache: int = None
    target_graphobjects_count_in_cache: int = None
    graphio_batchsize: int = 50000
    parsing_worker_spawn_min_wait_time_sec = 60

    cache_storage_total = None

    _last_amount_sourcing_cores = 1

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
        if not self.target_graphobjects_count_in_cache:
            self.target_graphobjects_count_in_cache = round(
                self.max_graphobjects_count_in_cache * 0.5
            )
        if not self.min_graphobjects_count_in_cache:
            self.min_graphobjects_count_in_cache = round(
                self.max_graphobjects_count_in_cache * 0.2
            )

    def amount_loading_cores(self) -> int:
        if (
            self.manager.statistics.is_sourcing_phase_done()
            or self.manager.statistics.get_cache_storage_used()
            >= self.manager.cache_size
            or self.manager.statistics.get_cache_storage_level() in ["ORANGE", "RED"]
        ):
            return self.max_processes_count
        c = round(self.max_processes_count - self.amount_sourcing_cores())
        if c == 0:
            c = 1
        # We can take more cores as available because loading processes are waiting a lot for the db and wont use any cpu time during that
        return math.ceil(c * 1.5)

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
        c = self._last_amount_sourcing_cores
        if self._cache_untouched:
            # when nothing is in cache yet we only let one parser work.
            # we want to measure how long the first parser need to load data into the cache
            # this way we can carefully increase parser workers without clogging the cache
            if self.manager.statistics.get_cached_graphobjects_total_count() > 0:
                # first objects arrive in cache.
                # from here on we can increase the amount of parsing workers
                self._cache_untouched = False
                self._cache_first_hit_time = (
                    self.manager.statistics.start_time - time.time()
                )
                if (
                    self._cache_first_hit_time
                    < self.parsing_worker_spawn_min_wait_time_sec
                ):
                    # we want at least a cooldown time of <self.parsing_worker_spawn_min_wait_time_sec> seconds for spawning new parsers
                    # otherwise we take the time the first parser needed to fill first data into the cache (+10 secs)
                    self._cache_first_hit_time = (
                        self.parsing_worker_spawn_min_wait_time_sec
                    )
                self._sourcing_cool_down_target_time = (
                    time.time() + self._cache_first_hit_time + 10
                )
            c = 1
        else:
            if self.manager.statistics.get_cache_storage_level() == "RED":
                # if memory is full, dont start any new parsers. we wait until the situation is better
                return 0
            if self._sourcing_cool_down_target_time < time.time():
                # Reset timer
                self._sourcing_cool_down_target_time = (
                    time.time() + self._cache_first_hit_time
                )
                cache_level_mean = (
                    self.manager.statistics.get_mean_count_graph_objects_in_cache()
                )
                cache_level_current = (
                    self.manager.statistics.get_cached_graphobjects_total_count()
                    - self.manager.statistics.get_loaded_graphobjects_total_count()
                )

                cache_level_trend = (
                    self.manager.statistics.get_cached_graphobjects_total_count_trend()
                )
                if (
                    cache_level_current < self.min_graphobjects_count_in_cache
                    or cache_level_mean < self.min_graphobjects_count_in_cache
                ):
                    # oh we scrape the bottom of the cache. That could distort our trend analyses and is not where we want to be anyway.
                    # turn up the volume
                    c = self._last_amount_sourcing_cores + 1
                # lets have a look at the trend of the cache. it is filling or drying? Based on that we give more or less cores for parsers
                elif cache_level_trend < -45:
                    c = self._last_amount_sourcing_cores + 1
                elif cache_level_trend > +45:
                    c = self._last_amount_sourcing_cores - 1
                else:
                    # no trend identifiable.
                    # lets do nothing and wait for the next tick
                    c = self._last_amount_sourcing_cores

                # but lets have a look at he mean (of the last 2 minutes) and current level of cache filling too
                if (
                    cache_level_mean > self.target_graphobjects_count_in_cache * 0.8
                    and cache_level_mean < self.target_graphobjects_count_in_cache * 1.2
                    and (c > self._last_amount_sourcing_cores)
                ):
                    # we are in the sweetspot of cache level. lets override the trend analyses result of upping one
                    # Here, we can keep feeding the loaders but wont eat too much memory
                    # ❤️ lets keep beeing here happy forever ❤️
                    c = self._last_amount_sourcing_cores
                elif (
                    cache_level_mean > self.max_graphobjects_count_in_cache
                    or cache_level_current > self.max_graphobjects_count_in_cache
                ):
                    # we shot over the max level. no more new parsers until the situation is better.
                    c = 1

            else:
                c = self._last_amount_sourcing_cores
        # max we can want to provide 60% of all cores for parsing
        max_c = math.floor(self.max_processes_count * 0.6)
        if c > max_c:
            c = max_c
        if c < 1:
            c = 1
        self._last_amount_sourcing_cores = c

        return c
