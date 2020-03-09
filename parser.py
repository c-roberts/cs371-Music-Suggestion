import json
import sys

def translateVal(v):
    if v <= (1/3):
        return "lowL"
    elif v <= (2/3):
        return "mediumL"
    else:
        return "highL"

def translatePitch(v):
    if v <= 250:
        return "lowL"
    elif v <= 500:
        return "mediumL"
    else:
        return "highL"

## run scraper -> dictionary
#from Data_Collection.collect import getSongs
##song_list = getSongs()

# open song list from json
with open(sys.path[0] + '/Data_Collection/data.json') as fj:
    song_list = json.load(fj)

print("Loaded data from json file.")

# initialize file
f = open(sys.path[0] + '/kb/KRR-SongsFacts.krf', "w") 
f.write("(in-microtheory cs371-Music-Suggestion)\n")

for s in song_list:
    s_title = s['title'].replace(" ", "").replace("'", "").replace("(", "-").replace(")", "").replace(":", "").replace(",", "").replace(".", "")
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
        f.write("(BeatOfSong {} {})\n".format(translateVal(s['beat']), s_title))
        f.write("(PitchOfSong {} {})\n".format(translatePitch(s['avgfreq']), s_title))

        # dances
        #for d in s['dances']:
        #    d_i = d.replace(" ", "").replace("(", "/").replace(")", "")
        #    f.write("(CanBeDancedTo {} {})\n".format(d_i, s_title))

        # tags
        for t in s['tags']:
            s_f = []
            if "/4" in t:
                f.write("(MeterOfSong \"{}\" {})\n".format(t, s_title))
            elif "swing" in t.lower() and "swing" not in s_f:
                s_f.append("swing")
                f.write("(StyleOfSong {} {})\n".format("swing", s_title))
            elif "latin" in t.lower() and "latin" not in s_f:
                s_f.append("latin")
                f.write("(StyleOfSong {} {})\n".format("latin", s_title))
            elif "ballroom" in t.lower() and "ballroom" not in s_f:
                s_f.append("ballroom")
                f.write("(StyleOfSong {} {})\n".format("ballroom", s_title))

    #print("Done with \"{}\".".format(s_title))


print('Finished parsing {} to knowledge base.'.format(len(song_list)))

f.close()
