from bs4 import BeautifulSoup
from requests import get as getHTML

soup = BeautifulSoup(getHTML("https://www.music4dance.net/song").text, features="html.parser")

print(soup)
