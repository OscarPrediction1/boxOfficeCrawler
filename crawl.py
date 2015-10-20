import json

# open movies file with box office ids
with open("movies.json", "r") as movies_file:
    movies_json = movies_file.read()

# parse movies config file
movies = json.loads(movies_json)

