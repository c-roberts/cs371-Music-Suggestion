from sys import exit

from requests import get as getHTML

from os import path
from pickle import dump as pdump
from pickle import load as pload

def loadAndCacheDatabaseHTML(dataBaseSiteBaseURL, dataBaseSiteHTMLDumpPath):
    if path.exists(dataBaseSiteHTMLDumpPath):
        print("## Status: Found cached copy of Music 4 Dance website.")
        dataBaseSiteHTML = pload(open(dataBaseSiteHTMLDumpPath, "rb"))
    else:
        # Make HTTP request
        try:
            dataBaseSiteHTML = getHTML(dataBaseSiteBaseURL).text
        except:
            print("!! Error: Retrieving Music 4 Dance website unsuccessfull.")
            exit(0)
        else:
            print("## Status: Retrieved Music 4 Dance website.")

        # Save for later
        pdump(dataBaseSiteHTML, open(dataBaseSiteHTMLDumpPath, "wb"))
        print("## Status: Cached copy of Music 4 Dance website for later.")

    return dataBaseSiteHTML
