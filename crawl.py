import json, requests
from bs4 import BeautifulSoup

# open movies file with box office ids
with open("movies.json", "r") as movies_file:
    movies_json = movies_file.read()

# parse movies config file
movies = json.loads(movies_json)

for movie in movies:

	# construct box office url
	url = "http://www.boxofficemojo.com/movies/?id=" + movie["boxOfficeId"] +".htm"
	r = requests.get(url)

	# load html file into parser
	soup = BeautifulSoup(r.text, "html.parser")

	# loop all font elements
	for font_el in soup.find_all("font"):

		# test
		if "Domestic Total Gross:" in font_el.get_text():

			movie["domesticTotalGross"] = int(font_el.get_text().replace("Domestic Total Gross: $", "").replace(",", ""))
			print movie["name"] + ": $" + str(movie["domesticTotalGross"])