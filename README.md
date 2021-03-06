# cs371-Music-Suggestion

## Problem
Our project explores song classification and recommendation using KRR approaches instead of the more common
statistical (i.e. machine learning) methods. In particular, we reason for recommendation based on mood, reasonable
dance style, and energy. We compute the mood by implementing a classification system adapted from research by
[Michael Nuzzolo](https://sites.tufts.edu/eeseniordesignhandbook/2015/music-mood-classification/) in companions.

## Using
This repository includes trimmed song data scraped from [Music4Dance.net](https://www.music4dance.net/),
analyzed for average pitch locally with python's `librosa`, the `sox` utility for Linux, and Unix's `file` command,
and then parsed into `krf` files. If you would like to collect more data yourself however, ensure that `sox` and `file`
are installed on your system and follow the instructions below in Data Collection. Otherwise, skip to the Companions
usage section.

### Data Collection
The Data_Collection module in this repository provides the `getSongs()` function
(usable in a python file in the repo root with `from Data_Collection.collect import getSongs`) which can scrape
and analyze new data from Music4Dance, and then cache this data for later use. This function is used by
`do_data_collection.py` to generate the `krf` song file.

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

Next, all of the `*Predicates.krf` files from the `kb` directory should be loaded into companions along with the trimmed
song files.

Recommendations may be requested of the system by querying `(songRecommended ?s)` in the `cs371-Music-Suggestion`
micro-theory. Initially, no recommendations will be given. Recommendations are dependent on storing facts of the form
`(userLikes ?song)` and `(userDisLikes ?song)` in the `cs371-Music-Suggestion` micro-theory where `?song` is any
`Song-CW` in the song files. Unfortunately, previous song recommendations are not updated by adding extra information.
Instead the micro-theory must be cleared and reloaded, then all `userLikes` and `userDisLikes` stored, and then
`(songRecommended ?s)` called anew.

## Ontology
We represented songs using Cyc-style statements. We defined predicates to give songs attributes such as tempo, artist, and energy level. Energy, mood, beat, and pitch are first represented as a scalar value ranging 0.0 to 1.0. This is mapped to a level, low (0.0-0.33), medium (0.34-0.66), or high (0.67-1.0). Meter of a song is represented as a string (i.e. "2/2 or "3/4"). 

```lisp
(isa songInstance Song-CW)
(composerOfMusicalCW artistInstance songInstance)
(isa artistInstance Musician)
(TitleOfSong "Song Instance" songInstance)
(TempoOfSong positiveInteger songInstance)
(EnergyOfSong level songInstance)
(BeatOfSong level songInstance)
(PitchOfSong level songInstance)
(MeterOfSong string songInstance)
```

## Reasoning
There are three reasoning goals in this project: mood, dance styles, and recommendation. First we reason on the pitch,
beat, and energy to conclude the mood. The horn clauses for this can be found in `kb/KRR-SongMoodPredicates.krf`. Dance
style clauses are also in `kb/KRR-SongMoodPredicates.krf`. Here we use tempo and meter to conclude all of the possible
styles that a song could reasonably be danced to. Finally, we use a multistage set of horn clauses from
`kb/KRR-SongLikePredicates.krf`, `kb/KRR-SongDisLikePredicates.krf`, and `kb/KRR-Predicates.krf` to generate
recommendations.

First preferences entered through `(userLikes ?song)` facts entail `(userLikes ?attribute)` for the `?attribute`s
of the `?song` (and similarly for `(userDisLikes ...)`), focusing on mood, dance styles, and energy.

These likes then entail potential recommendations for all the songs which have the liked `?attributes`, represented with
`(userMayLike ?song)` facts. Similarly, dislikes are propogated to other songs as `(userDisMayLike ?song)`. These
potential recommendations are then collected by the `(songRecommended ?s)` predicate, which selects songs sharing
attributes with liked songs, and sharing no attributes with disliked songs.

## Footnotes
[^1]: We aknowledge the unfortunate white-washing that is likely to result... With more time and excess sanity, a more
sensible data sanitization procedure could definitely be devised.
