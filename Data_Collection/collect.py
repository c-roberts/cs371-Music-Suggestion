from pprint import pprint

from bs4 import BeautifulSoup

import cacher
import scraper

dataBaseSiteBaseURL = "https://www.music4dance.net/song"
dataBaseSiteHTMLDumpPath = "site_HTML.pickle"

# In expected order
expectedColumns = ['Like/Play',
                   'Song Title',
                   'Artist',
                   'Tempo (in Beats Per Minute)',
                   'Strength of the beat',
                   'Energy of the song',
                   'Mood of the song',
                   'Dance Style Tags',
                   'Tags',
                   'Modified'
                  ]

dataBaseSiteHTML = cacher.loadAndCacheDatabaseHTML(dataBaseSiteBaseURL,
                                                   dataBaseSiteHTMLDumpPath
                                                  )

# Parse HTML 
dataBaseSiteSoup = BeautifulSoup(dataBaseSiteHTML,
                                 features="html.parser"
                                )

# Get song table
pageSongTable = scraper.getPageTable(dataBaseSiteSoup)
songRows = 	scraper.getSongRows(pageSongTable)

# Parse table columns
scraper.checkColumnLabels(pageSongTable, expectedColumns)

print(scraper.songTitle(songRows[0]))
print(scraper.songArtist(songRows[0]))
print(scraper.songTempo(songRows[0]))
print(scraper.songBeatStrength(songRows[0]))
print(scraper.songEnergy(songRows[0]))
print(scraper.songMood(songRows[0]))
print(scraper.songDanceStyles(songRows[0]))
print(scraper.songDanceStyles(songRows[-5]))
print(scraper.songTags(songRows[1]))
