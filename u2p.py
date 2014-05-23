#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import multiprocessing as m
import pandas as p

try:
    inFile = sys.argv[1]
    with open(sys.argv[1], 'r') as f:
        colNames = f.next().replace('\n', '').split(';')
        for i, line in enumerate(f):
            pass
        inLines = i + 2
except IndexError:
    # sys.exit(1)
    pass

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
    return res

def reducer(L):
    pass

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
                print 'chunk length: %s' % len(res)
                return res
    return res

def u2p(L):
    outFile = '%s_%s-%s.csv' % (sys.argv[1], L[0], L[1])
    print 'started %s' % outFile
    res = mapper(chread(inFile, L[0], L[1]))
    res.to_csv(outFile)
    print 'done %s' % outFile

if __name__ == '__main__':
    pool = m.Pool(processes = 8)
    print len(lsplit(inLines, 128))
    pool.map(u2p, lsplit(inLines, 128))
