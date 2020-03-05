from Data_Collection.collect import getSongs

def translateVal(v):
    if v <= (1/3):
        return "low"
    elif v <= (2/3):
        return "medium"
    else:
        return "high"

# run scraper -> dictionary
song_list = getSongs()

# initialize file
f = open("KRR-SongsFacts.krf", "w")
f.write("(in-microtheory cs371-Music-Suggestion)\n")

for s in song_list:
    if s['beat'] == None or s['energy'] == None or s['mood'] == None or s['tempo'] == None:
        continue
    else: 
        # write stuff to file as ISAs
        s_title = s['title'].replace(" ", "")
        s_artist = s['artist'].replace(" ", "")

        f.write("\n(isa {} Song-CW)\n".format(s_title))
        f.write("(composerOfMusicalCW {} {})\n".format(s_artist, s_title))
        f.write("(TempoOfSong {} {})\n".format(s['tempo'], s_title))
        f.write("(EnergyOfSong {} {})\n".format(translateVal(s['energy']), s_title))
        #f.write("(MoodOfSong {} {})\n".format(translateVal(s['mood']), s_title))
        f.write("(BeatOfSong {} {})\n".format(translateVal(s['beat']), s_title))

        # dances
        for d in s['dances']:
            f.write("(CanBeDancedTo {} {})\n".format(d.replace(" ", ""), s_title))
   

        

f.close()
