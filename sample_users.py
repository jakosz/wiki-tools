#!/usr/bin/python
# -*- coding:utf-8 -*-

import bz2
import random
import sys

'''
    Reads in bz2 compressed pmh (pages-meta-history) file.
    Writes random sample of user ids.
'''

try:
    LANG = sys.argv[1]
except IndexError:
    print 'select language'

datadir = '../data/dumps'
inFile = bz2.BZ2File('%s/%s_pmh.csv.bz2' % (datadir, LANG), 'r')
outFile = '%s/%s_pmh.user_sample.csv' % (datadir, LANG)

population = set()
for i, line in enumerate(inFile):
    if i != 0:
        try:
            cid = line.split(';')[4]
            int(cid) # force value error when there's IP instead of ID
            population.add(cid+'\n')
        except ValueError:
            pass
    if i % 10**6 == 0:
        print i / 10**6

sample = random.sample(population, int(1.2*10**4))

with open(outFile, 'w') as f:
    f.writelines(sample)
