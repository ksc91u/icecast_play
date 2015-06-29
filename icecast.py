#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#http://dir.xiph.org/yp.xml
import xml.etree.ElementTree as ET
import random
import os, os.path, sys
import sqlite3


def createdb():
    conn = sqlite3.connect('channels.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE channels
                 (server_name text, listen_url text, server_type text, bitrate int, genre text)''')
    conn.commit()
    conn.close()

def which(pgm):
    path=os.getenv('PATH')
    for p in path.split(os.path.pathsep):
        p=os.path.join(p,pgm)
        if os.path.exists(p) and os.access(p,os.X_OK):
            return p

def initdb():
    conn = sqlite3.connect('channels.db')
    c = conn.cursor()
    tree = ET.parse('yp.xml')
    element_root = tree.getroot()
    for child in element_root:
        channel={}
        for entryc in child:
            channel[entryc.tag] = entryc.text
        c.execute('''INSERT INTO channels (server_name, listen_url, server_type, bitrate, genre) values (?,?,?,?,?)''', (channel['server_name'], channel['listen_url'], channel['server_type'], channel['bitrate'], channel['genre']))
        conn.commit()
    conn.close()

def checkdb():
    conn = sqlite3.connect('channels.db')
    c = conn.cursor()
    try:
        c.execute('''select count(1) from channels''')
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

conn = sqlite3.connect('channels.db')
c = conn.cursor()
c.execute('''select listen_url from channels order by RANDOM() limit 1''')

url = c.fetchone()[0]


ffplay = which('ffplay')
mplayer = which('mplayer')
if (ffplay is not None):
    os.execl(ffplay,'ffplay','-nodisp','-bufsize','256k',url)
elif (mplayer is not None):
    os.execl(mplayer,'mplayer','-prefer-ipv4','-cache','256','-vo','null',url)
