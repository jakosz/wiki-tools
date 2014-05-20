#!/usr/bin/python
# -*- coding:utf-8 -*-

import bz2
import sys
import os
import time

# ------------------------------------------------------------------------------ setup

emsg = '''usage:
    $ python pages_meta_history.py input_file [output_file]
    '''
try:
    inFile = bz2.BZ2File(sys.argv[1], 'r')
except IndexError:
    print emsg
    sys.exit(1)

try:
    outFile = sys.argv[2]
except IndexError:
    outFile = sys.argv[1].replace('.bz2', '.csv')

# Initialize flags...
page_lock = 0
rev_lock = 0
user_lock = 0
text_lock = 0
# ...and (some) variables:
text_size = 'NA'
text_diff = 'NA'

'''
An object for holding page text sizes at given revisions, used to compute next revision size
(deleted when found as parentid in next revision)
'''
difflog = {}

# file
csv_header = 'pageid;ns;revid;parentid;userid;timestamp;size;diff;line'
with open(outFile, 'w') as f:
    f.write(csv_header + '\n')

# ------------------------------------------------------------------------------ helpers

def clean(S, T):
    ''' String, Tag '''
    return S.replace('<%s>' % T, '').replace('</%s>' % T, '').replace(' ', '').replace('\n', '')

def has(S, T):
    ''' String, Tag '''
    if S.find(T) != -1:
        return True
    else:
        return False

# ------------------------------------------------------------------------------ processing

for i, line in enumerate(inFile):
    '''
    flags for determining cursor's position in the XML file:
    '''
    if has(line, '<page>'):
        page_lock = 1
        page_data = {}
    if has(line, '</page>'):
        page_lock = 0
    if has(line, '<revision>'):
        rev_lock = 1
        rev_data = {}
        rev_data['line'] = i
    if has(line, '</revision>'):
        rev_lock = 0
    if has(line, '<text '):
        text_lock = 1
        text_data = ''
    if has(line, '</text>'):
        text_lock = 0
    
    # ++ debug
    #print '%s,%s,%s' % (i, page_lock, rev_lock)
    # -- debug
    
    '''
    page properties
    '''
    if page_lock and not rev_lock:
        if has(line, '<id>'):
            page_data['pageid'] = clean(line, 'id')
        if has(line, '<ns>'):
            page_data['ns'] = clean(line, 'ns')
    '''
    revision properties
    '''
    if page_lock and rev_lock:
        if has(line, '<contributor>'):
            user_lock = 1
        if has(line, '</contributor>'):
            user_lock = 0
        if has(line, '<id>'):
            if not user_lock:
                rev_data['revid'] = clean(line, 'id')
            if user_lock:
                rev_data['userid'] = clean(line, 'id')
        if has(line, '<timestamp>'):
            rev_data['timestamp'] = clean(line, 'timestamp')
        if has(line, '<parentid>'):
            parentid = clean(line, 'parentid')
        if has(line, '<ip>'):
            rev_data['userid'] = clean(line, 'ip')

    if text_lock:
        text_data = text_data + line

    '''
    prepare entry for the finished revision & write a line to csv
    '''
    if has(line, '</revision>'):
        # text size & diff:
        text_data = text_data.replace('<text xml:space="preserve">', '').replace('</text>', '')
        text_size = len(text_data)
        if not text_lock and 'revid' in rev_data.keys():
            if len(text_data) != 0:
                difflog[rev_data['revid']] = text_size
        try:
            text_diff = text_size - difflog[parentid]
        except KeyError:
            text_diff = 'NA'
            parentid = 'NA'
        if 'userid' in rev_data.keys():
            with open(outFile, 'a') as f:
                f.write('%s;%s;%s;%s;%s;%s;%s;%s;%s\n' % (page_data['pageid'], 
                                                       page_data['ns'], 
                                                       rev_data['revid'], 
                                                       parentid, 
                                                       rev_data['userid'], 
                                                       rev_data['timestamp'], 
                                                       text_size, 
                                                       text_diff,
                                                       rev_data['line']))
    if not rev_lock:
        try:
            del difflog[parentid]
        except:
            pass
        parentid = 'NA'
    
    if i % 10**7 == 0:
        print '%s: %s' % (time.ctime(), i)
