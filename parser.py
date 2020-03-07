#from Data_Collection.collect import getSongs
import json
import sys

def translateVal(v):
    if v <= (1/3):
        return "lowL"
    elif v <= (2/3):
        return "mediumL"
    else:
        return "highL"

## run scraper -> dictionary
##song_list = getSongs()

# open song list from json
with open(sys.path[0] + '/Data_Collection/data.json') as f:
    song_list = json.load(f)

print("Loaded data from json file.")

# initialize file
with open("KRR-SongsFacts.krf", "w") as f:
    f.write("(in-microtheory cs371-Music-Suggestion)\n")

    for s in song_list:
        s_title = s['title'].replace(" ", "").replace("'", "")
        s_artist = s['artist'].replace(" ", "")
        
        if s['beat'] == None or s['energy'] == None or s['mood'] == None or s['tempo'] == None:
            print("Song \"{}\" skipped due to missing essential data".format(s_title))
            continue
        else: 
            # write stuff to file as ISAs
            
            f.write("\n(isa {} Song-CW)\n".format(s_title))
            f.write("(composerOfMusicalCW {} {})\n".format(s_artist, s_title))
            f.write("(TempoOfSong {} {})\n".format(s['tempo'], s_title))
            f.write("(EnergyOfSong {} {})\n".format(translateVal(s['energy']), s_title))
            #f.write("(MoodOfSong {} {})\n".format(translateVal(s['mood']), s_title))
            f.write("(BeatOfSong {} {})\n".format(translateVal(s['beat']), s_title))

            # dances
            for d in s['dances']:
                d_i = d.replace(" ", "").replace("(", "/").replace(")", "")
                f.write("(CanBeDancedTo {} {})\n".format(d_i, s_title))
        #print("Done with \"{}\".".format(s_title))

    print('Finished parsing {} to knowledge base.'.format(len(song_list)))
    

