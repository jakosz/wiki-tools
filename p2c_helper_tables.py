#!/usr/bin/python
# -*- coding:utf-8 -*-

import MySQLdb
import settings.mysql

'''
    This script documents the construction of helper tables used by p2c.py
'''

db = MySQLdb.connect(host = settings.mysql.host, 
                     user = settings.mysql.usr,
                     passwd = settings.mysql.pwd, 
                     db = settings.mysql.db)

