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
from pprint import pprint
import concurrent.futures

def mapped_search(keys):
    ids = []
    for k in keys.split(','):
        print(k)
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(search, k)
            print("mapped_search i " + str(len(future.result())))
            ids.extend(future.result())
    return ids

def search(key):
    conn = sqlite3.connect(module_path() + 'channels.db')
    c = conn.cursor()

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
        try:
            c.execute('''INSERT INTO channels (server_name, listen_url, server_type, bitrate, genre, source) values (?,?,?,?,?,?)''', (d['Name'], d['ID'], d['Format'], d['Bitrate'], d['Genre'].lower(), 'scst'))
        except sqlite3.IntegrityError:
            pass
        if(d['Listeners'] == 0):
            pass
        else:
            ids.append(d['ID'])

    conn.commit()
    conn.close()
    print("Found " + str(len(ids)) + " channels")
    return ids

def searchFromDb(key):
    conn = sqlite3.connect(module_path() + 'channels.db')
    c = conn.cursor()
    c.execute('''select * from ( select listen_url, genre from channels where genre like ? and source="scst") order by RANDOM() limit 1''',[(key.lower()+"%")])
    ids = []
    one = c.fetchone()
    if (one is None):
        return ids
    ids.append(one[0])
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
try:
    searchFromDb('anything g')
except sqlite3.OperationalError:
    createdb()


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

ids_search = mapped_search(sys.argv[1])
print("mapped_search result "+ str(len(ids_search)))

ids = searchFromDb(genre)
print("Db result "+ str(len(ids)))
ids.extend(ids_search)
if (len(ids) <= 0):
    ids = search(genre)
    print("Search result "+ str(len(ids)))
    if (len(ids) <= 0):
        ids = getFromTop(genre)
r =  sysr.randint(0, len(ids)-1)
url = getPlayUrl(ids[r])
print(url)

playUrl(url)

