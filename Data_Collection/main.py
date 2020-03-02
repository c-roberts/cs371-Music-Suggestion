from sys import exit
from pprint import pprint

from bs4 import BeautifulSoup
from requests import get as getHTML

from re import sub as regexReplace
from math import floor

dataBaseSiteBaseURL = "https://www.music4dance.net/song"

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


# Make HTTP request
try:
    dataBaseSiteResponse = getHTML(dataBaseSiteBaseURL)
except:
    print("!! Error: Retrieving Music 4 Dance website unsuccessfull.")
    exit(0)
else:
    print("## Status: Retrieved Music 4 Dance website.")


# Parse HTML 
dataBaseSiteSoup = BeautifulSoup(dataBaseSiteResponse.text,
                                 features="html.parser"
                                )

# Get song table
def getPageTable(pageSoup):
    return pageSoup.body.find('div', class_='body-content').find('table')

def getSongRows(pageTable):
    return [row for row in pageTable.find_all('tr')]

pageSongTable = getPageTable(dataBaseSiteSoup)
songRows = getSongRows(pageSongTable)

# Parse table columns
def sanitizeColumnTitle(raw_title):
    title = raw_title.strip()
    title = title.split(':')[0]
    title = regexReplace("Click to sort by [\w ]+\.", "",
                         title
                        )
    title = regexReplace("\([\w ]+ icons represent [\w ]+\)\.", "",
                         title
                        )
    title = title.strip()
    return title

def getColumnIndices(pageTable):
    indices = {}
    index = 0
    for colLabel in pageTable.thead.tr.find_all('th'):
        if 'title' in colLabel.attrs:
            indices[
                    sanitizeColumnTitle(colLabel.attrs['title'])
                   ] = index
        else:
            title_text = sanitizeColumnTitle(colLabel.text)
            if title_text != '':
                indices[title_text] = index
            else:
                sub_index = 0
                for img in colLabel.find_all('img'):
                    indices[sanitizeColumnTitle(img.attrs['title'])] \
                        = index + sub_index/10
                    sub_index += 1
        index += 1
    return indices

def checkColumnLabels(colIndicesDict):
    missing = []
    for label in expectedColumns:
        if label not in colIndicesDict:
            missing.append(label)
    if len(missing):
        print("!! Error: Website table is missing the following expected labels:", missing)
        print("!!        Please update the data collection program to the new website format.")
        exit(0)
    else:
        print("## Status: Found all expected website table columns.")

colIndicesByLabel = getColumnIndices(pageSongTable)
checkColumnLabels(colIndicesByLabel)

# Accessing song table elements
def songAttrByIdx(songRow, index):
    el = songRow.find_all('td')[floor(index)]
    if (index % 1) == 0:
        return el.a.text
    else:
        # loop through sub_index

print(songAttrByIdx(songRows[3], 2))

