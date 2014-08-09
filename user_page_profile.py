#!/usr/bin/python
# -*- coding:utf-8 -*-

import pandas as p
from settings import data
import json

LANG = 'de'
namec = data.meta['namec'][LANG]

page_profile_file = '%s/%s_page_profiles.json' % (data.trans, LANG)
user_page_file = '%s/%s_user_page.csv' % (data.trans, LANG)

pg = '%s/%swiki-latest-page.sql.csv' % (data.dumps, LANG)
pg = p.read_csv(pg, sep = ';', quotechar = "'", header = None)
pg.set_axis(1, ['id', 'ns', 'title'])
pg = pg[pg.ns == 0]

# -- get pageids of good and featured articles

def readl(path):
    with open(path, 'r') as f:
        res = f.readlines()
        res = map(lambda x: x.replace('\n', ''), res)
        return res

pGood = readl('%s/%s_good_names' % (data.trans, LANG))
pFeatured = readl('%s/%s_featured_names' % (data.trans, LANG))

pGood = pg[pg.title.isin(pGood)]
pFeatured = pg[pg.title.isin(pFeatured)]

dGood = dict.fromkeys(pGood.id.tolist())
dFeatured = dict.fromkeys(pFeatured.id.tolist())

# -- assign page profile to each row in user-page table:

with open(page_profile_file, 'r') as f:
    page_profile = json.loads(f.read())
    page_profile = dict((int(k), v) for k, v in page_profile.iteritems())

user_page = p.read_csv(user_page_file, sep = ';')

user_page_profile = ['pageid;good;featured;Geographie;Geschichte;Gesellschaft;Kunst_und_Kultur;Religion;Sport;Technik;Wissenschaft\n']
for i, pid in enumerate(user_page.pageid):
    cProfile = page_profile[pid]
    try:
        dGood[pid]
        cGood = '1'
    except KeyError:
        cGood = '0'
    try:
        dFeatured[pid]
        cFeatured = '1'
    except KeyError:
        cFeatured = '0'
    cLine = ';'.join([str(pid), cGood, cFeatured])
    cLineProfile = ';'.join(map(lambda x: str(x), cProfile)) + '\n'
    user_page_profile.append(cLine + ';' + cLineProfile)
    if i % 10000 == 0:
        print i

with open('%s/%s_user_page_profiles.csv' % (data.trans, LANG), 'w') as f:
    f.writelines(user_page_profile)
