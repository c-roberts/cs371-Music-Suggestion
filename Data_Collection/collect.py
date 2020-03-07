from bs4 import BeautifulSoup

from Data_Collection import cacher
from Data_Collection import scraper

def getSongs():
    databaseSiteBaseURL      = "https://www.music4dance.net/song"
    databaseSiteHTMLDumpPath = "Data_Collection/site_HTML.pickle"
    databaseDumpPath         = "Data_Collection/data.json"

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

    database = cacher.loadCachedDatabase(databaseDumpPath)
    if not database:
        databaseSiteHTML = cacher.loadAndCacheDatabaseHTML(databaseSiteBaseURL,
                                                           databaseSiteHTMLDumpPath
                                                          )

        # Parse HTML
        databaseSiteSoup = BeautifulSoup(databaseSiteHTML,
                                         features="html.parser"
                                        )
        print("## Status: Parsed HTML into internal representation.")

        # Get songs
        database = scraper.getSongs(databaseSiteSoup, expectedColumns)
        cacher.cacheDatabase(databaseDumpPath, database)
        print("## Status: Cached copy of Music 4 Dance database for later.")

    return database
