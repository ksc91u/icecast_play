#!/usr/bin/env python
#http://dir.xiph.org/yp.xml
import xml.etree.ElementTree as ET
import random
import os, os.path, sys


def which(pgm):
    path=os.getenv('PATH')
    for p in path.split(os.path.pathsep):
        p=os.path.join(p,pgm)
        if os.path.exists(p) and os.access(p,os.X_OK):
            return p

sysr = random.SystemRandom()
sysr.seed()
tree = ET.parse('yp.xml')
element_root = tree.getroot()

urls = []

for child in element_root:
    for entryc in child:
        if (entryc.tag == 'listen_url'):
            url = entryc.text
        if (entryc.tag == 'genre' and ('classical' in entryc.text.lower())):
            urls.append(url)
            continue

r =  sysr.randint(0, len(urls)-1)
url = urls[r]

ffplay = which('ffplay')
mplayer = which('mplayer')
if (ffplay is not None):
    os.execl(ffplay,'ffplay','-nodisp','-bufsize','256k',url)
elif (mplayer is not None):
    os.execl(mplayer,'mplayer','-prefer-ipv4','-cache','256','-vo','null',url)
