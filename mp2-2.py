## mini project 2 Phase 1, CMPUT291

import pymongo
import json

def createCollections(db):
	#check if collections exist and drop if they do
	colList = db.list_collection_names()
	if "Posts" in colList:
		collection = db["Posts"]
		collection.drop()
	if "Tags" in colList:
		collection = db["Tags"]
		collection.drop()
	if "Votes" in colList:
		collection = db["Votes"]
		collection.drop()
	#create new collections
	posts = db["Posts"]
	tags = db["Tags"]
	votes = db["Customers"]
	
	#read json files and insert them into collections
	#with open('Posts.json') as file:
	#	file_data = json.load(file)
	#posts.insert_one(file_data)
	with open('Tags.json') as file:
		file_data = json.load(file)
	tags.insert_one(file_data)
	# with open('Votes.json') as file:
	# 	file_data = json.load(file)
	# votes.insert_one(file_data)

	colList = db.list_collection_names()
	if "Tags" in colList:
		print("Tags collection created successfully.\n")

	createTerms(db)

def createTerms(db):
	posts = db.posts
	for post in posts:
		body = post["Body"].split()
		title = post["Title"].split()
		for word in body:
			if len(word) >= 3:
				terms.insert(0, word) # add to array
				#do indexing here as you add to array
		for word in title:
			if len(word) >= 3:
				terms.insert(0, word) # add to array
				#do indexing here as you add to array

def main():
	# port = input("Please enter the port you'd like to run the database on: ")
	client = pymongo.MongoClient("localhost", 27017)
	db = client['291db']	
	createCollections(db)
	
if __name__ == "__main__":
	main()
