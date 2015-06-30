#!/usr/bin/env python3
from inspect import getsourcefile
from os.path import abspath
import xml.etree.ElementTree as ET
import random
import os, os.path, sys
import sqlite3


def createdb():
    conn = sqlite3.connect(module_path() + 'channels.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE channels
                 (server_name text, listen_url text UNIQUE, server_type text, bitrate int, genre text, source text)''')
    conn.commit()
    conn.close()

def which(pgm):
    path=os.getenv('PATH')
    for p in path.split(os.path.pathsep):
        p=os.path.join(p,pgm)
        if os.path.exists(p) and os.access(p,os.X_OK):
            return p
def module_path():
    return os.path.dirname(abspath(getsourcefile(lambda:0))) + "/../"

def playUrl(url):
    ffplay = which('ffplay')
    mplayer = which('mplayer')
    if (ffplay is not None):
        os.execl(ffplay,'ffplay','-nodisp','-bufsize','256k',url)
    elif (mplayer is not None):
        os.execl(mplayer,'mplayer','-prefer-ipv4','-cache','256','-vo','null',url)
