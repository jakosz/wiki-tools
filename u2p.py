#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import multiprocessing
import pandas as p

try:
    with open(sys.argv[1], 'r') as f:
        colNames = f.next().replace('\n', '')
        inFile = [f.next().replace('\n', '') for i in range(1, 30)]
except IndexError:
    sys.exit(1)

def mapper(L):
    '''
    Takes as an input a list of csv rows, converts them to a pandas.DataFrame
    and returns aggregates for user-page
    '''
    df = p.DataFrame(map(lambda x: x.split(';'), inFile), columns = colNames.split(';'))
    df = df.loc[:,['userid', 'pageid', 'diff']]
    df['diff'] = df['diff'].astype(int)
    gf = df.groupby(['userid', 'pageid'])
    def sum_abs(x):
        return sum(abs(x))
    res = gf.aggregate([len, sum])
    print res

if __name__ == '__main__':
    mapper(inFile)
