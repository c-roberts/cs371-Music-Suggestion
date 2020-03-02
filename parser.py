from keith import scraper

# run scraper -> dictionary
my_dict = scraper.run()

# initialize file
f = open("KRR-SongsFacts.krf", "w")

for s in my_dict:
    # write stuff to file as ISAs



f.close()
