#!/usr/bin/env python

import os
import bz2
import sys
import gzip
import json
import redis

from os.path import join
from dateutil.parser import parse as parse_date

stats = redis.StrictRedis()
stats.flushdb()

def analyze(tweets_file):
    for line in open(tweets_file):
        tweet = json.loads(line)
        t = parse_date(tweet['created_at']).strftime('%Y-%m-%d')
        stats.incr('tweets-%s' % t)

        if 'entities' in tweet:
            for hashtag in tweet['entities']['hashtags']:
                tag = hashtag['text'].lower()
                if tag == 'ferguson':
                    continue
                stats.zincrby('hashtags-%s' % t, tag, 1)

        if 'entities' in tweet and 'media' in tweet['entities']:
            for media in tweet['entities']['media']:
                stats.zincrby('media-%s' % t, media['media_url'], 1)

        if 'entities' in tweet and 'urls' in tweet['entities']:
            for url in tweet['entities']['urls']:
                stats.zincrby('urls-%s' % t, url['expanded_url'], 1)

        if 'retweeted_status' in tweet:
            stats.zincrby('retweets-%s' % t, tweet['retweeted_status']['id_str'], 1)
            stats.zincrby('users-%s' % t, tweet['retweeted_status']['user']['screen_name'], 1)

def tweets(data_dir):
    count = 0
    for filename in os.listdir(data_dir):
        path = join(data_dir, filename)
        print "loading %s" % path
        if filename.endswith('json.bz2'):
            fh = bz2.BZ2File(path)
        elif filename.endswith('json.gz'):
            fh = gzip.GzipFile(path)
        else:
            continue
        for line in fh:
            count += 1
            if count % 10000 == 0:
                sys.stdout.write('.')
                sys.stdout.flush()
            try:
                yield json.loads(line)
            except:
                sys.stdout.write('x')
                sys.stdout.flush()

for filename in os.listdir('data'):
    if filename.endswith('.json'):
        analyze(join('data', filename))
