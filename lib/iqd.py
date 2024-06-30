from statistics import median

import pandas as pd

# See is_outlier below
IQD_FILTER_FOR_NORMAL_DIST = 2.22
MIN_ARRAY_LENGTH = 30  # Same as MAX_LENGTH in main.py.  TODO: Break out constants.py


def iqd(a):
    """
    Return the interquartile distance of array a.
    """
    a = sorted(a)
    mid = len(a) // 2
    q1_median = median(a[:mid])
    q3_median = median(a[mid:])
    return q3_median - q1_median


def clamp_df(df: pd.DataFrame, f: float = IQD_FILTER_FOR_NORMAL_DIST) -> pd.DataFrame:
    """
    Clamp a dataframe to a normal distribution.  See is_outlier()
    for details.
    """
    flat_df = df.to_numpy().flatten()
    iqr_dist = iqd(flat_df)
    med = median(flat_df)

    def _clamp(x):
        high_iqr = med + f * iqr_dist
        low_iqr = med - (f * iqr_dist)
        if x > high_iqr:
            return high_iqr
        elif x < low_iqr:
            return low_iqr
        else:
            return x

    return df.map(_clamp)


def is_outlier(
    a, m, f: float = IQD_FILTER_FOR_NORMAL_DIST, min_length=MIN_ARRAY_LENGTH
):
    """
    Determine if measurement m is an outlier compared to
    array a; return True if so.

    Uses method outlined here: https://stackoverflow.com/questions/23199796/detect-and-exclude-outliers-in-a-pandas-dataframe/69001342#69001342

    Quote:

        Eliminate all data that is more than f times the interquartile
        range away from the median of the data. That's also the
        transformation that sklearn's RobustScaler uses for
        example. IQR and median are robust to outliers, so you
        outsmart the problems of the z-score approach.

        In a normal distribution, we have roughly iqr=1.35*s, so you
        would translate z=3 of a z-score filter to f=2.22 of an
        iqr-filter. This will drop the 999 in the above example.

        The basic assumption is that at least the "middle half" of
        your data is valid and resembles the distribution well,
        whereas you also mess up if your distribution has wide tails
        and a narrow q_25% to q_75% interval.


    Here we're just flagging values rather than eliminating them.

    Exits early (& returns False) if a is too short.
    """
    if len(a) < min_length:
        return False

    iqr_dist = iqd(a)
    med = median(a)
    return abs(m - med) > f * iqr_dist
