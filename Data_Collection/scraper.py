from sys import exit

from re import sub as regexReplace
from re import match as regexMatch

from sh import rm
from validators import url as valid_url

from Data_Collection.frequency_analyzer import downloadSample
from Data_Collection.frequency_analyzer import convertSample
from Data_Collection.frequency_analyzer import songFrequency

###
### Page Table
###
def getPageTable(pageSoup):
    return pageSoup.body.find('div', class_='body-content').find('table')

def getSongRows(pageTable):
    return [row for row in pageTable.find_all('tr')[1:]]

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

def checkColumnLabels(pageTable, expectedColumns):
    foundColTitles = []
    for colLabel in pageTable.thead.tr.find_all('th'):
        if 'title' in colLabel.attrs:
            foundColTitles.append(sanitizeColumnTitle(colLabel.attrs['title']))
        else:
            title_text = sanitizeColumnTitle(colLabel.text)
            if title_text != '':
                foundColTitles.append(title_text)
            else:
                for img in colLabel.find_all('img'):
                    foundColTitles.append(sanitizeColumnTitle(img.attrs['title']))
    missing = []
    for colIndex in range(len(expectedColumns)):
        if expectedColumns[colIndex] != foundColTitles[colIndex]:
            missing.append(expectedColumns[colIndex])
               
    if len(missing):
        print("!! Error: Page table is missing the following expected labels:", missing)
        print("!!        Please update the data collection program to the new website format.")
        print("!!        Note that the expected label list must be correctly ordered.")
        exit(0)
    else:
        print("## Status: Found all expected page table column labels in expected order.")

###
### Songs
###
def songTitle(songRow):
    try:
        return songRow.find_all('td')[1].a.text
    except:
        return None

def songArtist(songRow):
    try:
        return songRow.find_all('td')[2].a.text
    except:
        return None

def songTempo(songRow):
    try:
        return int(songRow.find_all('td')[3].a.text)
    except:
        return None

def songBeatStrength(songRow):
    try:
        return float(regexMatch("This song has a beat strength of (\d{1,2}\.\d{1,2})",
                                songRow.find_all('td')[4]
                                       .find_all('a')[0]
                                       .img.attrs['title']
                               ).group(1)
                )
    except:
        return None

def songEnergy(songRow):
    try:
        return float(regexMatch("This song has an energy level of (\d{1,2}\.\d{1,2})",
                                songRow.find_all('td')[4]
                                       .find_all('a')[1]
                                       .img.attrs['title']
                               ).group(1)
                )
    except:
        return None

def songMood(songRow):
    try:
        return float(regexMatch("This song has a mood level of (\d{1,2}\.\d{1,2})",
                                songRow.find_all('td')[4]
                                       .find_all('a')[2]
                                       .img.attrs['title']
                               ).group(1)
                    )
    except:
        return None

def songDanceStyles(songRow):
    styles = []
    tds = songRow.find_all('td')
    if tds and len(tds) >= 6:
        for a in tds[5].select("a[data-dance-name]"):
            if a.attrs['data-dance-name']:
                styles.append(a.attrs['data-dance-name'].lower())
        return styles
    else:
        return None

def songTags(songRow):
    tags = []
    tds = songRow.find_all('td')
    if tds and len(tds) >= 7:
        for a in tds[6].select("a[data-tag-value]"):
            if a.attrs['data-tag-value']:
                tags.append(a.attrs['data-tag-value'].lower())
        return tags
    else:
        return None

def songLink(songRow):
    try:
        link = songRow.find_all('td')[0].select("a[data-sample]")[0].attrs['data-sample'].strip()
        if valid_url(link):
            return link
        else:
            return None
    except:
        return None

def songData(songRow):
    title = songTitle(songRow)
    artist = songArtist(songRow)
    link = songLink(songRow)
    if not link:
        return None

    file_name = downloadSample(link, title, artist)
    file_name = convertSample(file_name)
    if not file_name:
        return None

    return {
        "title":    title,
        "artist":   artist,
        "avgfreq":  songFrequency(file_name),
        "tempo":    songTempo(songRow),
        "beat":     songBeatStrength(songRow),
        "energy":   songEnergy(songRow),
        "mood":     songMood(songRow),
        "dances":   songDanceStyles(songRow),
        "tags":     songTags(songRow)
    }
###
### Interface
###
def getSongs(dataBaseSiteSoup, expectedColumns):
    # Validate table columns
    pageSongTable = getPageTable(dataBaseSiteSoup)
    checkColumnLabels(pageSongTable, expectedColumns)

    songRows      = getSongRows(pageSongTable)
    songs         = []
    for s in songRows:
        data = songData(s)
        if data:
            songs.append(data)
    print("## Status: Successfully parsed", len(songs), "songs.")
    return songs

    
