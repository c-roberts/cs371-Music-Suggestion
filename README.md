# cs371-Music-Suggestion

## Problem
Our project explores song classification and recommendation using KRR approaches instead of the more common
statistical (i.e. machine learning) methods. In particular, we reason for recommendation based on mood, reasonable
dance style, and energy. We compute the mood by implementing a classification system adapted from research by
[Michael Nuzzolo](https://sites.tufts.edu/eeseniordesignhandbook/2015/music-mood-classification/) in companions.

## Using
This repository includes trimmed song data scraped from [Music4Dance.net](https://www.music4dance.net/),
analyzed for average pitch locally with python's `librosa`, the `sox` utility for Linux, and Unix's `file` command,
and then parsed into `krf` files. If you would like to collect more data yourself however, follow the instructions
below in Data Collection. Otherwise, skip to the Companions usage section.

### Data Collection
The Data_Collection module in this repository provides the `getSongs()` function
(`from Data_Collection.collect import getSongs` in a python file in the repo root) which can scrape and analyze new
data from Music4Dance, and then cache this data for later use. This function is used by `do_data_collection.py` to
generate the `krf` song file.

Running `do_data_collection.py` requires a few dependences managed by [`pipenv`](https://pipenv.pypa.io/en/latest/).
First install `python3` and `pipenv`. Then run `pipenv install` in the repo root. This will configure the required
dependencies. Now you may run `pipenv run python3 do_data_collection.py`.

If the `Data_Collection/data.json` file is present, the `getSongs()` function will simply return its contents as a
list of python dictionaries. To collect more data, delete or rename this file. The `getSongs()` function will then
cache the website pages in `Data_Collection/site_HTML.pickle`. To force re-downloading of the website, delete or
rename this file. The number of website pages to scrape may be changed by adjusting the integer passed to
`cacher.loadAndCacheDbHTMLPages(...)` in `Data_Collection/collect.py`.

### Companions
In order to work with companions, the fickle beast that it is, we recommend trimming the `krf` song file by removing
songs with non ascii data [^1] or with parens in any of the string fields and splitting the songs into multiple files
so that each file contains no more than 400 lines.

Next, all of the `*Predicate.krf` files should be loaded into companions along with the trimmed song files.

Recommendations may be requested of the system by querying `(songRecommended ?s)` in the `cs371-Music-Suggestion`
micro-theory. Initially, no recommendations will be given. Recommendations are dependent on storing facts of the form
`(userLikes ?song)` and `(userDisLikes ?song)` in the `cs371-Music-Suggestion` micro-theory where `?song` is any
`song-CW` in the song files. Unfortunately, previous song recommendations are not updated by adding extra information.
Instead the micro-theory must be cleared and reloaded, then all `userLikes` and `userDisLikes` stored, and then
`(songRecommended ?s)` called anew.

## Ontology

## Reasoning

[^1]: We aknowledge the unfortunate white-washing that is likely to result... With more time and excess sanity, a more
sensible data sanitization procedure could definitely be devised.
