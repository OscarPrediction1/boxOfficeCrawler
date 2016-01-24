from pymongo import MongoClient
import db

client = MongoClient(db.conn_string)
db = client.oscar

print "boxOfficeId;total_gross;gross_per_day"

for data in db.boxoffice_movies.find():

	total_gross = -1
	days = -1
	if data.has_key("history"):
		total_gross = data["history"][-1]["grossToDate"]
		days = data["history"][-1]["dayNumber"]

	print data["boxOfficeId"] + ";" + str(total_gross) + ";" + str(total_gross / days)