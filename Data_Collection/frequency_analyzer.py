from requests import get as HTTPGet
from re import match as regexMatch

from sh import file as file_info, sox, mv, rm

from numpy import mean, std
import librosa

def downloadSample(songLink, songTitle, songArtist):
    file_name = songTitle + ' - ' + songArtist + '.unknown'

    with open(file_name, 'wb') as f:
        f.write(HTTPGet(songLink).content)

    return file_name

def convertSample(file_name):
    info = file_info(file_name).replace(file_name + ': ', '')

    if regexMatch('Audio file with', info):
        info = info.replace('Audio file with ', '')
    else:
        aac_match = regexMatch("ISO Media, Apple iTunes (.*)", info)
        if aac_match:
            encoding = aac_match.group(1)
            print("!! Error: Unsupported Apple audio encoding:", encoding)
            return None
        print("!! Error: Downloaded 'audio' file", "'"+file_name+"'", "with attributes:")
        print("         ", info)
        return None

    mp3_match = regexMatch("ID3 version (.*) contains:(.*)", info)
    if mp3_match:
        id3_version, encoding = mp3_match.groups()
        new_file_name = file_name.replace('.unknown', '.mp3')
    elif False:
        new_file_name = ''
    else:
        print("!! Error: Unrecognized audio container:", info)
        return None

    mv(file_name, new_file_name)

    flac_file_name = file_name.replace('.unknown', '.flac')
    sox(new_file_name, flac_file_name)
    rm(new_file_name)
    
    return flac_file_name
    
def songFrequency(flac_file_name):
    y, sr = librosa.core.load(flac_file_name)
    frequencies = librosa.feature.spectral_centroid(y=y, sr=sr)[0]


    standard_deviation = std(frequencies)
    average            = mean(frequencies)

    low  = average - 2*standard_deviation
    high = average + 2*standard_deviation

    frequencies = frequencies[frequencies < high]
    frequencies = frequencies[frequencies > low]

    '''
    import matplotlib.pyplot as plot

    plot.plot(frequencies)
    plot.show()
    '''

    average = int(mean(frequencies))
    rm(flac_file_name)

    print("## Status: Successfully analyzed average frequency from", flac_file_name+".")
    return average
