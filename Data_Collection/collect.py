from bs4 import BeautifulSoup

from Data_Collection import cacher
from Data_Collection import scraper

def getSongs():
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

    # Get songs
    return scraper.getSongs(dataBaseSiteSoup, expectedColumns)
