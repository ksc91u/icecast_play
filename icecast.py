#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#http://dir.xiph.org/yp.xml
from inspect import getsourcefile
from os.path import abspath
import xml.etree.ElementTree as ET
import random
import os, os.path, sys
import sqlite3
from utils.utils import *

def initdb():
    conn = sqlite3.connect(module_path() + 'channels.db')
    c = conn.cursor()
    tree = ET.parse(module_path() + 'yp.xml')
    element_root = tree.getroot()
    for child in element_root:
        channel={}
        for entryc in child:
            channel[entryc.tag] = entryc.text
        c.execute('''INSERT INTO channels (server_name, listen_url, server_type, bitrate, genre, source) values (?,?,?,?,?,?)''', (channel['server_name'], channel['listen_url'], channel['server_type'], channel['bitrate'], channel['genre'].lower(), 'ice'))
        conn.commit()
    conn.close()

def checkdb():
    conn = sqlite3.connect(module_path() + 'channels.db')
    c = conn.cursor()
    try:
        c.execute('''select count(1) from channels where source='ice' ''')
    except sqlite3.OperationalError:
        createdb()
        return False
    if (c.fetchone()[0] > 0):
        return True
    else:
        return False
    conn.close()

if not checkdb():
    print("Initialize db")
    initdb()


if (len(sys.argv) < 2):
    genre = 'classical'
else:
    genre = sys.argv[1]

conn = sqlite3.connect(module_path() + 'channels.db')
c = conn.cursor()
c.execute('''select * from ( select listen_url, genre from channels where genre = ? and source="ice") order by RANDOM() limit 1''',[(genre.lower())])

url = c.fetchone()[0]

playUrl(url)

