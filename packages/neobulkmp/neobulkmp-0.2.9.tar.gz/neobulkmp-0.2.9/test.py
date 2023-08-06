import numpy, math


def _trend(data: dict) -> int:
    """Return the trend of a number list in degree.
    0 = no trend
    postive number (max 90) = numbers go upwarts
    negative number (min -90) = numbers trending downwards

    Args:
        data (list): e.g. [1,34,564,1,23]

    Returns:
        int: trend as a degree number between -90 to 90
    """
    if len(data) > 1:
        # i am too stupid to get numpy.polynomial.polynomial.Polynomial.fit to work
        """
            coeffs = numpy.polynomial.polynomial.Polynomial.fit(
                range(0, len(data)), list(data), 1
            )
            print(list(range(0, len(data))))
            print(data)
            coeffs_convert = coeffs.convert().coef
            try:
                slope = list(coeffs_convert)[1]
            except:
                slope = 0
            print("coeffs", coeffs)
            print("coeffs_convert", list(coeffs_convert))
            print("slope", slope)
            angle_rad = math.atan(slope)
            angle_deg = math.degrees(angle_rad)
            return round(float(angle_deg), 2)
        else:
            return 0
        """
        """
        # lets use the old numpy api
        coeffs = numpy.poly1d(
            numpy.polyfit(numpy.arange(0, len(data)), numpy.array(data), 1)
        )
        print("coeffs", coeffs)
        slope = list(coeffs)[-2]
        print("slope", round(slope))
        angle_rad = math.atan(slope)
        angle_deg = math.degrees(angle_rad)
        return round(float(angle_deg), 2)
        """
        import datetime as dt
        from scipy import stats
        import pandas as pd

        print(data)
        df = pd.DataFrame(data, columns=["date", "value"])
        df.date = pd.to_datetime(df.date)
        df["date_ordinal"] = pd.to_datetime(df["date"]).map(dt.datetime.toordinal)
        print(df)
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            df["date_ordinal"], df["value"]
        )
        print(slope)
        return slope


l = [
    (1234567891111111, 100000),
    (1244567891111111, 100000),
    (1254567891111111, 100000),
    (1264567891111111, 100000),
    (1274567891111111, 100201),
]
print(_trend(l))
exit()
l = [2, 2, 2, 3]
print(_trend(l))

l = [1, 2, 3, 4]
print(_trend(l))
