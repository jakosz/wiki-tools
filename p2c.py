#!/usr/bin/python
# -*- coding:utf-8 -*-

import threading as t
import pandas as p
from settings import data
import time
import json

LANG = 'de'

def mainc_find(x):
    return pg.loc[pg.title == x, :]

# prepare sql tables
cl = '%s/%swiki-latest-categorylinks.sql.csv' % (data.dumps, LANG)
pg = '%s/%swiki-latest-page.sql.csv' % (data.dumps, LANG)

cl = p.read_csv(cl, sep = ';', quotechar = "'", header = None).iloc[:,:2]
pg = p.read_csv(pg, sep = ';', quotechar = "'", header = None)

ns0 = pg.iloc[:,1] == 0
ns14 = pg.iloc[:,1] == 14

pg = pg.loc[ns0 | ns14, :]

pg.set_axis(1, ['id', 'ns', 'title'])
cl.set_axis(1, ['from_id', 'title'])

# id-to-id lookup table
ii = p.merge(cl, pg, on='title', how='inner')
ii = ii.loc[ii.ns == 14, :]
ii = ii.sort('from_id')

# id-to-id lookup dict
def build_dict(ii):
    i4 = dict.fromkeys(ii.from_id.unique().tolist())
    for i, key in enumerate(i4.keys()):
        i4[key] = ii.id[ii.from_id == key].tolist()
        ii = ii.loc[ii.from_id != key]
    return i4

# zintegrować to w jedną funkcję z powyższym:
'''
i2 = ii
Dict = {}
for i in range(1, 1000):
    t0 = time.time()
    subDf = i2.loc[i2.from_id < i * 10000]
    Dict.update(build_dict(subDf))
    i2 = i2.loc[i2.from_id >= i * 10000]
    print '%s:\t%s\t%s' % (i, time.time()-t0, len(Dict.keys()))
    if i % 100 == 0:
        with open('%s/p2c.json' % data.trans, 'w') as f:
            f.write(json.dumps(Dict))
'''

# takes pageid (x) and returns parent categories found across n iterations up
# pDict is a graph of page-category relations
def nParents(x, n = 1000):
    res = set()
    x = [x]
    for i in range(n):
        cRes = []
        for e in x:
            try:
                cRes.append(pDict[e])
            except KeyError:
                pass
        x = cRes
        x = [e for sublist in x for e in sublist]
        if len(x) == 0:
            return list(res)
        [res.add(e) for e in x]
    return list(res)

# takes pageids (x) and outputs their category profiles
def pageProfiler(x, categories):
    res = {}
    for e in x: 
        eParents = nParents(e)
        eProfile = [int(c in eParents) for c in categories]
        res.update({e: eProfile})
    return res

#------------------------------------------------------------------------------

# input table (pmh filtered by sampled user ids)
sample = p.read_csv('%s/%s_pmh_sample_filtered.csv' % (data.dumps, LANG), sep = ';', header = None)
sample.columns = ['pageid','ns','revid','parentid','userid','timestamp','size','diff','line']
pageids = sample.pageid.unique()
pids = p.Series(pageids)

with open('%s/%s_p2c.json' % (data.trans, LANG), 'r') as f:
    pDict = json.loads(f.read())
    # json keeps keys as strings!
    pDict = dict((int(k), v) for k, v in pDict.iteritems())

mainc = data.meta['mainc'][LANG]
with open('%s/%s_page_profiles.json' % (data.trans, LANG), 'w') as f:
    f.write(json.dumps(pageProfiler(pids.tolist(), mainc)))
