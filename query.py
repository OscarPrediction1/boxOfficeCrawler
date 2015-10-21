import db
from pymongo import MongoClient

client = MongoClient(db.conn_string)
db = client.oscars

print "Movies in 2014:", db.boxOfficeMovies.count({"release.year": 2014})
print "Movies in 2015:", db.boxOfficeMovies.count({"release.year": 2015})