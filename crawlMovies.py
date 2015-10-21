import json, requests
from bs4 import BeautifulSoup
from string import ascii_uppercase

major_sites = ["NUM"]

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

		print "parsed"

		# crawl table
		tbl = soup.find_all("table")[3]
		print tbl
		cells = tbl.find_all("td")

		# loop over cells
		i = 0
		for cell in cells:
			i = i % 7
			
			# first cell
			if i == 0:
				print cell.get_text()

			i += 1

		print "---"

		page += 1

		if site == "NUM":
			break

	break
