# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import time, math
import pandas
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

def calc_r2(data1, data2):
    y_list = data1
    y_hat_list = data2
    y_mean = np.mean(data1)
    e = sum([(y - yhat) ** 2 for y, yhat in zip(y_list, y_hat_list)])
    d = sum([(y - y_mean) ** 2 for y in y_list])
    r2 = 1.0 - e/d
    return r2

def calc_residuals(d1, d2):
    return [math.sqrt((x1 - x2) ** 2) for x1, x2 in zip(d1, d2)]

def make_point_list(data):
    return [i for i, v in enumerate(sorted(data.iteritems())) if v[1] == 1]

def fill_range(df, _from, _to):
    td = timedelta(minutes=1)
    current = _from
    while current <= _to:
        if not pandas.Timestamp(current) in df.index:
            df[pandas.Timestamp(current)] = 0
        current += td
    df = df.sort_index()
    return df

def convert_to_utime(df):
    return [time.mktime(pandas.Timestamp(value).timetuple()) for value in df.index.values]

def compress(df, window='1min'):
    compressed = pandas.DataFrame({'counts': np.ones(len(df))},
                                  index=df.index)
    compressed = compressed.resample(window, how='sum')
    compressed[compressed.counts>=1] = 1
    compressed = compressed['counts'].fillna(value=0)
    return compressed

def aggregate(data, unit):
    return [sum(data[i:i+int(unit)]) for i in range(0, len(data), int(unit))]

def remove_dummies(flags, df1, df2):
    list1 = df1
    list2 = df2
    if flags[0]: list1 = df1[1:]
    if flags[1]: list2 = df2[1:]
    if flags[2]: list1 = df1[:-1]
    if flags[3]: list2 = df2[:-1]
    return list1, list2
