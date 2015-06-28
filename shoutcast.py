#!/usr/bin/env python
import random
import os, os.path, sys
import json
from pprint import pprint
import urllib.request as urllib2
import urllib.parse

def which(pgm):
    path=os.getenv('PATH')
    for p in path.split(os.path.pathsep):
        p=os.path.join(p,pgm)
        if os.path.exists(p) and os.access(p,os.X_OK):
            return p

def getPlayUrl(id):
    data = {
    	'station':str(id)
    }
    data = urllib.parse.urlencode(data)
    headers = {
    	'X-Requested-With':'XMLHttpRequest'
    }
    req = urllib2.Request('http://www.shoutcast.com/Player/GetStreamUrl', data.encode('ascii'), headers) 
    response = urllib2.urlopen(req)
    the_page = response.read()
    return the_page.decode('ascii').strip('"')


sysr = random.SystemRandom()
sysr.seed()

json_data=open("shoutcast.json").read()
data = json.loads(json_data)

ids = []

for d in data:
    if ('classical' in d['Genre'].lower()):
    	ids.append(d['ID'])

r =  sysr.randint(0, len(ids)-1)
url = getPlayUrl(ids[r])
print(url)

ffplay = which('ffplay')
ffplay=None
mplayer = which('mplayer')
if (ffplay is not None):
    os.execl(ffplay,'ffplay','-nodisp','-bufsize','256k',url)
elif (mplayer is not None):
    os.execl(mplayer,'mplayer','-prefer-ipv4','-cache','256','-vo','null',url)
