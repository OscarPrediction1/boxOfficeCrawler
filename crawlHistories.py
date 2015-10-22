import json, requests, db, re, pymongo
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime

client = MongoClient(db.conn_string)
db = client.oscar
non_decimal = re.compile(r'[^\d.]+')

movies = db.boxoffice_movies.find().sort("release", pymongo.DESCENDING)
for movie in movies:

	if movie["release"]:
		print movie["boxOfficeId"], "(" + str(movie["release"].year) + ")"
	else:
		print movie["boxOfficeId"]

	# construct box office url
	url = "http://www.boxofficemojo.com/movies/?page=daily&view=chart&id=" + movie["boxOfficeId"] + ".htm"
	r = requests.get(url)

	# load html file into parser
	soup = BeautifulSoup(r.text, "html.parser")

	# loop all font elements
	for font_el in soup.find_all("font"):

		# test
		if "Domestic Total Gross:" in font_el.get_text():

			domesticTotalGross = int(font_el.get_text().replace("Domestic Total Gross: $", "").replace(",", ""))
			db.boxoffice_movies.update({"boxOfficeId": movie["boxOfficeId"]}, {"$set": {"totalGross": domesticTotalGross}})

	histories = []

	# find table with historic data
	rows = soup.find_all("tr")
	for row in rows:

		if "/daily/chart/?sortdate=" in str(row) and "$" in str(row) and not "JSChart" in str(row):


			cells = row.find_all("td")
			
			# date
			link = cells[1].find("a").get("href")
			link = link.replace("&p=.htm", "").replace("/daily/chart/?sortdate=", "")
			link = link.split("-")

			# gross
			gross = cells[3].get_text().replace("$", "").replace(",", "")
			gross = non_decimal.sub('', gross)

			# theaters
			theaters = cells[6].get_text()

			if "-" in theaters:
				theaters = None
			else:
				theaters = int(non_decimal.sub('', theaters))

			# gross to date
			grossToDate = cells[8].get_text().replace("$", "").replace(",", "")
			grossToDate = non_decimal.sub('', grossToDate)

			if grossToDate:
				grossToDate = int(grossToDate)

			history = {
				"dayOfWeek": cells[0].get_text(),
				"date": datetime(int(link[0]), int(link[1]), int(link[2])),
				"gross": int(gross),
				"theaters": theaters,
				"grossToDate": grossToDate,
				"dayNumber": int(cells[9].get_text())
			}

			histories.append(history)

	# update history of movie in database
	if len(histories) > 0:
		
		# skip same history sizes
		if "histories" in movie:
			if len(histories) == len(movie["history"]):
				continue

		db.boxoffice_movies.update({"_id": movie["_id"]}, {"$set": {"history": histories}})
		print "History updated..."
		print ""
			