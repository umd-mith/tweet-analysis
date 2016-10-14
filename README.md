# tweet-analysis

This repository contains some code for generating a simple [report] of the
number of tweets per day and popular users, hashtags, media files, urls and
retweets.  It uses a dataset of line oriented twitter data as input. It uses
[Redis] to store statistics and the report is written in [Markdown].

Maybe there will be a Docker container for this some day, but until then here's
what you will need to do (or approximate) to run it:

```
sudo apt-get install redis-server
git clone https://github.com/umd-mith/tweet-analysis
cd tweet-analysis
pip install -r requirements.txt 
cp /path/to/my/tweets.json data/
./load.py
./report.py > report.md
```

[MITH]: http://mith.umd.edu
[report]: https://github.com/edsu/ferguson-analysis/blob/master/report.md
[Redis]: http://redis.io
[Markdown]: https://en.wikipedia.org/wiki/Markdown
