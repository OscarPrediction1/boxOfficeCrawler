import json, requests, re, db
from bs4 import BeautifulSoup
from string import ascii_uppercase
from pymongo import MongoClient

client = MongoClient(db.conn_string)
db = client.oscars

non_decimal = re.compile(r'[^\d.]+')
major_sites = ["NUM"]
movies = []

# feed alphabet into major_site crawl
for c in ascii_uppercase:
	major_sites.append(c)

# loop major sites
for site in major_sites:

	page = 1
	while True:

		# fetch table
		url = "http://www.boxofficemojo.com/movies/alphabetical.htm?letter=" + site + "&p=.htm&page=" + str(page)
		r = requests.get(url)

		print url

		# load html file into parser
		soup = BeautifulSoup(r.text, "html.parser")

		# crawl rows
		rows = soup.find_all("tr")

		parsedCounter = 0

		for row in rows:
			if "<a href=\"/movies/?id=" in str(row) and "$" in str(row):

				cells = row.find_all("td")
				parsedCounter += 1

				# total gross
				totalGross = cells[2].get_text().replace("$", "").replace(",", "")
				totalGross = non_decimal.sub('', totalGross)

				if totalGross:
					totalGross = int(totalGross)

				# start date
				startDate = cells[6].get_text()

				if startDate and "/" in startDate:
					startDate = startDate.split("/")

					if len(startDate) == 3:
						year = int(startDate[2])
						month = int(startDate[0])
						day = int(startDate[1])

				# box office if
				link = cells[0].find("a").get("href")
				if link:
					link = link.replace("/movies/?id=", "").replace(".htm", "")

				movie = {
					"name": cells[0].get_text(),
					"boxOfficeId": link,
					"totalGross": totalGross,
					"release": {
						"year": year,
						"month": month,
						"day": day
					}
				}
				
				db.boxOfficeMovies.replace_one({"boxOfficeId": movie["boxOfficeId"]}, movie, upsert=True)

		page += 1

		if site == "NUM" or parsedCounter == 0:
			break

print "done"
