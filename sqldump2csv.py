#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys

'''
    Transforms MySQL dump file into a csv table, skipping the extremely slow
    dump load. 
    
    Usage:

    $ python sqldump2csv.py frwiki-latest-categorylinks.sql "[0,1,6]"
    
    You can optionally select which columns to pass to the output file; 
    cols should be a quoted list of table column indices, like above.
    Remember that some columns in the database might be binary. 
'''

try:
    FILE = sys.argv[1]
except IndexError:
    print 'file [cols]'

try:
    COLS = eval(sys.argv[2])
except IndexError:
    COLS = []

data_dir = '/home/y/proj/wiki/data/dumps'
sql = '%s/%s' % (data_dir, FILE)
out = '%s/%s.csv' % (data_dir, FILE)

with open(out, 'w') as f:
    f.write('')

def splitfire(x, quote = "'"):
    res = []
    cRes = ''
    qopen = False
    x = ',%s;' % x
    for i, char in enumerate(x):
        if char == quote and x[i-1] != '\\':
            qopen = not qopen
        if char in [',', ';'] and not qopen:
            res.append(cRes)
            cRes = ''
            continue
        cRes += char
    return res[1:]

def unpackLine(x, c = []):
    x = x.split('VALUES')[1]
    x = x[2:(len(x)-3)]
    x = x.split('),(')
    res = []
    for entry in x:
        cols = splitfire(entry)
        if len(c) != 0:
            row = [v for i, v in enumerate(cols) if i in c]
        else:
            row = cols
        row = map(lambda x: x.replace(';', ''), row)
        row = ';'.join(row) + '\n'
        res.append(row)
    return res

with open(sql, 'r') as f:
    for i, line in enumerate(f):
        if line.find('INSERT INTO') == 0:
            with open(out, 'a') as outf:
                outf.writelines(unpackLine(line, COLS))
        print i
