import scrape_mars
import pymongo

################################################
## create a mongo database with mars dasta in it
################################################

# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# set database and collection names
db = client.mars_db
collection = db.marsdata

# add to collection - if the collection does not exist this will create it
collection.insert_one(scrape_mars.scrape())

