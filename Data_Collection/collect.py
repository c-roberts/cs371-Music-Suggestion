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
        databaseSiteHTMLPages = cacher.loadAndCacheDbHTMLPages(databaseSiteBaseURL,
                                                          databaseSiteHTMLDumpPath,
                                                          2
                                                         )

        sitePageSoups = []
        for siteHTMLPage in databaseSiteHTMLPages:
            # Parse HTML
            sitePageSoups.append(BeautifulSoup(siteHTMLPage,
                                               features="html.parser"
                                              ))
        print("## Status: Parsed HTML into internal representation.")

        # Get songs
        database = []
        for sitePageSoup in sitePageSoups:
            database.extend(scraper.getSongs(sitePageSoup, expectedColumns))

        cacher.cacheDatabase(databaseDumpPath, database)
        print("## Status: Cached copy of Music 4 Dance database for later.")

    return database
