import json, requests, re, db
from bs4 import BeautifulSoup
from string import ascii_uppercase
from pymongo import MongoClient
from datetime import datetime

client = MongoClient(db.conn_string)
db = client.oscar

nominees = db.oscar_nominations.distinct("boxOfficeId")

for nominee in nominees:

	# fetch director
	dir_url = "http://www.boxofficemojo.com/movies/?id=" + nominee + ".htm"
	dir_r = requests.get(dir_url)

	# load html file into parser
	dir_soup = BeautifulSoup(dir_r.text, "html.parser")

	directors = []
	for a in dir_soup.find_all("a"):
		if "/people/chart/?view=Director" in a.get("href"):
			directors.append(a.get_text())

	print nominee

	movie = {
		"boxOfficeId": nominee,
		"directors": directors
	}
	
	db.boxoffice_movies.replace_one({"boxOfficeId": movie["boxOfficeId"]}, movie, upsert=True)