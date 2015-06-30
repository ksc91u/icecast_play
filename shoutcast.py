#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from inspect import getsourcefile
from os.path import abspath
import random
import os, os.path, sys
import json
from pprint import pprint
import urllib.request as urllib2
import urllib.parse
from utils.utils import *

def search(key):
    data = {
        'query':key,
	'limit':str(500)
    }
    data = urllib.parse.urlencode(data)
    headers = {
        'X-Requested-With':'XMLHttpRequest'
    }
    req = urllib2.Request('http://www.shoutcast.com/Search/UpdateSearch', data.encode('ascii'), headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    json_data = json.loads(the_page.decode('utf-8'))
    ids = []
    for d in json_data:
        ids.append(d['ID'])
    print("Found " + str(len(ids)) + " channels")
    return ids

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

def getFromTop(genre):
    json_data=open(module_path() + "shoutcast.json",'rb').read().decode('utf-8')
    data = json.loads(json_data)

    ids = []

    for d in data:
        if (genre in d['Genre'].lower()):
            ids.append(d['ID'])
    return ids

if (len(sys.argv) < 2):
    genre = 'classical'
else:
    genre = sys.argv[1]

ids = search(genre)
if (len(ids) <= 0):
    ids = getFromTop(genre)
r =  sysr.randint(0, len(ids)-1)
url = getPlayUrl(ids[r])
print(url)

playUrl(url)

