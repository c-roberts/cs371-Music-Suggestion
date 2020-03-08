from sys import exit

from requests import get as getHTML

from os import path
from pickle import dump as pdump
from pickle import load as pload
from json import dumps as jdump
from json import loads as jload

def loadCachedDatabase(databaseDumpPath):
    if path.exists(databaseDumpPath):
        print("## Status: Found cached copy of Music 4 Dance database.")
        with open(databaseDumpPath, 'r') as f:
            return jload(f.read())
    else:
        return None

def cacheDatabase(databaseDumpPath, database):
    with open(databaseDumpPath, 'w') as f:
        f.write(jdump(database))

def loadAndCacheDbHTMLPages(databaseSiteBaseURL, databaseSiteHTMLDumpPath, numPages):
    if path.exists(databaseSiteHTMLDumpPath):
        print("## Status: Found cached copy of Music 4 Dance website.")
        databaseSiteHTMLPages = pload(open(databaseSiteHTMLDumpPath, "rb"))
    else:
        # Make HTTP request
        try:
            databaseSiteHTMLPages = []
            for i in range(numPages):
                databaseSiteHTMLPages.append(getHTML(databaseSiteBaseURL + "?page=%d" % (i+1)).text)
        except:
            print("!! Error: Retrieving Music 4 Dance website unsuccessfull.")
            exit(0)
        else:
            print("## Status: Retrieved Music 4 Dance website.")


        # Save for later
        pdump(databaseSiteHTMLPages, open(databaseSiteHTMLDumpPath, "wb"))
        print("## Status: Cached copy of Music 4 Dance website for later.")

    return databaseSiteHTMLPages
