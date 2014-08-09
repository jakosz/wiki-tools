#!/usr/bin/python
# -*- coding:utf-8 -*-

import bz2
import sys

try:
    LANG = sys.argv[1]
except IndexError:
    print 'select LANG'

'''
    Filters the dump .bz2 archive (pmh) according to selected criteria
    (in this case, uid in sample, ns is 0, # timestamp has 2013-)
'''

criteria = [{'col': 1, 'fun': lambda x: x == '0'},
            {'col': 4, 'fun': lambda x: x in sample}] 
            # {'col': 5, 'fun': lambda x: x[:5] == '2013-'}]

data_dir = '/home/y/proj/wiki/data/dumps'
samplef = '%s/%s_pmh.user_sample.csv' % (data_dir, LANG)
dumpf = '%s/%s_pmh.csv.bz2' % (data_dir, LANG)
filteredf = '%s/%s_pmh_sample_filtered.csv' % (data_dir, LANG)

with open(samplef, 'r') as f:
    sample = map(lambda x: x.replace('\n', ''), f.readlines())

dump = bz2.BZ2File(dumpf, 'r')

for i, line in enumerate(dump):
    cLine = line.split(';')
    cTest = []
    for test in criteria:
        cTest.append(test['fun'](cLine[test['col']]))
    if all(cTest):
        with open(filteredf, 'a') as f:
            f.writelines(line)
    if i % 10**6 == 0:
        print i / 10**6
