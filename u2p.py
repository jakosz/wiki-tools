#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import multiprocessing as m
import pandas as p
import time

'''
    Transforms pages-meta-history (pmh) tables into user-page aggregates.
'''

# ------------------------------------------------------------------------------ setup

t0 = time.time()

emsg = '''
Usage:
    $ python u2c.py infile [nproc] [nchunks]
    %s
'''

try:
    inFile = sys.argv[1]
    with open(sys.argv[1], 'r') as f:
        colNames = f.next().replace('\n', '').split(';')
        for i, line in enumerate(f):
            pass
        inLines = i + 2
except IndexError:
    print emsg % ''
    sys.exit(1)

try:
    NPROC = sys.argv[2]
except IndexError:
    print emsg % 'Number of worker processes set to default (8)\n'
    NPROC = 8

try:
    NCHUNKS = sys.argv[3]
except IndexError:
    print emsg % 'Number of file chunks set to default (256)'
    NCHUNKS = 256

# ------------------------------------------------------------------------------ defs

def aagg(df):
    '''
    After-aggregate: inserts back index names as dataframe columns
    '''
    idf = p.DataFrame([i for i in df.index])
    df.index = range(df.shape[0])
    res = p.concat([idf, df], axis = 1)
    res.columns = ['userid', 'pageid', 'edits', 'chars']
    return res

def mapper(L):
    '''
    Takes as an input a list of [pmh, not split] csv rows, converts them to a pandas.DataFrame
    and returns aggregates for user-page: 
        * total (absolute) number of characters changed
        * total number of edits
    '''
    df = p.DataFrame(map(lambda x: x.split(';'), L), columns = colNames)
    df = df.loc[:,['userid', 'pageid', 'size', 'diff']]
    df['diff'][df['diff'] == 'NA'] = df['size'][df['diff'] == 'NA']
    df['diff'] = df['diff'].astype(int)
    df = df.drop('size', 1)
    gf = df.groupby(['userid', 'pageid'])
    res = gf.aggregate([len, lambda x: sum(abs(x))])
    res.columns = ['edits', 'chars']
    return aagg(res)

def reducer(L):
    '''
    Input: mapper output; a list of pandas.DataFrames
    Output: total aggregates per user-page (as with mapper)
    '''
    df = p.concat(L)
    gf = df.groupby(['userid', 'pageid'])
    res = gf.aggregate(sum)
    return aagg(res)

def lsplit(N, n):
    '''
    Divides range(N) into (usually) n buckets in the form of list of [from, to].
    '''
    Bucket = int(N/n)
    From = range(0, N, Bucket)
    To = map(lambda x: (x + Bucket) - 1, From)
    res = []
    for i,e in enumerate(From):
        res.append([From[i], To[i]])
    return res

def chread(File, From, To, header = True):
    '''
    Returns From:To lines from a File.
    '''
    res = list()
    with open(File, 'r') as f:
        for i, line in enumerate(f):
            if i >= From and i < To:
                if header and i == 0:
                    pass
                else:
                    res.append(line)
            if i >= To:
                return res
    return res

def u2p(L):
    print L
    res = mapper(chread(inFile, L[0], L[1]))
    return res

# ------------------------------------------------------------------------------ proc

if __name__ == '__main__':
    pool = m.Pool(processes = int(NPROC))
    res = pool.map(u2p, lsplit(inLines, int(NCHUNKS)))
    reducer(res).to_csv(sys.argv[1].replace('.csv', '_u2p.csv'))
    print '%s processes did it in %s seconds' % (NPROC, time.time() - t0)
