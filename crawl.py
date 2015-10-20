import json

# open movies file with box office ids
with open("movies.json", "r") as movies_file:
    movies_json = movies_file.read()

# parse movies config file
movies = json.loads(movies_json)

for movie in movies:

	# construct box office url
	url = "http://www.boxofficemojo.com/movies/?id=" + movie["boxOfficeId"] +".htm"
	print url