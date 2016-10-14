#!/usr/bin/env python

# you'll need to run load.py before you can run this

import redis

stats = redis.StrictRedis()
times = [s.split('-', 1)[1] for s in stats.keys('tweets-*')]
times.sort()

def main():
    print \
"""
# Tweet Analysis

The reports include:

* [Tweets per day](#user-content-tweets)
* [Top Users per day](#user-content-users)
* [Top Hashtags per day](#user-content-hashtags)
* [Top Media files per day](#user-content-media)
* [Top URLs per day](#user-content-urls)
* [Top Retweets per day](#user-content-retweets)

The twitter JSON data is parsed and features are stored in Redis where
they can be counted easily.

"""
    tweets()
    users()
    hashtags()
    media()
    urls()
    retweets()

def hashtags():
    print
    print "## Hashtags"
    print "The top ten most used hashtags per day."
    for time in times:
        print
        print "### %s" % time
        print 
        print "| Hashtag | Tweets |"
        print "| ------- | ------:|"
        for tag in stats.zrevrange('hashtags-%s' % time, 0, 10, withscores=True):
            print '| %s | %i |' % tag

def media():
    print
    print "## Media"
    print "The top ten most used media files by day."
    for time in times:
        print
        print "### %s" % time
        print "| Media | Tweets |"
        print "| ----- | ------:|"
        for tag in stats.zrevrange('media-%s' % time, 0, 10, withscores=True):
            print '| [%s](%s) | %i |' % (tag[0], tag[0], tag[1])

def retweets():
    print
    print "## Retweets"
    print "The top ten retweets by day."
    for time in times:
        print
        print "### %s" % time
        print "| Tweet | Retweets |"
        print "| ----- | --------:|"
        for tag in stats.zrevrange('retweets-%s' % time, 0, 10, withscores=True):
            # TODO get the tweet text and ids for these
            print '| %s | %i |' % tag

def tweets():
    print
    print "## Tweets"
    print
    print "Number of tweets per day."
    print
    print "| Date | Tweets |"
    print "| ---- | ------:|"
    total = 0
    for time in times:
        num = int(stats.get('tweets-%s' % time))
        print "| %s | %s |" % (time, num)
        total += num
    print "| Total | %s |" % total

def urls():
    print
    print "## URLs"
    print "The top ten most tweeted URLs by day."
    for time in times:
        print
        print "### %s" % time
        print "| URL | Tweets |"
        print "| --- | ------:|"
        for tag in stats.zrevrange('urls-%s' % time, 0, 10, withscores=True):
            print '|%s|%i|' % tag

def users():
    print
    print "## Users"
    print "The top ten most retweeted users by day."
    for time in times:
        print
        print "### %s" % time
        print "| Username | Re(tweets) |"
        print "| -------- | ----------:|"
        for tag in stats.zrevrange('users-%s' % time, 0, 10, withscores=True):
            print '| [%s](http://twitter.com/%s) | %i |' % (tag[0], tag[0], tag[1])

if __name__ == "__main__":
    main()
