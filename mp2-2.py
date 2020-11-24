## mini project 2 Phase 1, CMPUT291
from functools import partial

import pymongo
import json
import ijson


def createCollections(db):
    # check if collections exist and drop if they do
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
    # create new collections
    posts = db["Posts"]
    tags = db["Tags"]
    votes = db["Customers"]

    # read json files and insert them into collections
    with open('Posts.json') as file:
        data = ijson.items(file, 'posts.row.item')
        for i in data:
            print(i)
            posts.insert_one(json.loads(json.dumps(i)))

    with open('Tags.json') as file:
        data = ijson.items(file, 'tags.row.item')
        for i in data:
            print(i)
            tags.insert_one(json.loads(json.dumps(i)))

    with open('Votes.json') as file:
        data = ijson.items(file, 'votes.row.item')
        for i in data:
            print(i)
            votes.insert_one(json.loads(json.dumps(i)))

    # with open('Posts.json') as file:
    # 	file_data = json.load(file)
    # posts.insert_one(file_data['posts'])
    # with open('Tags.json') as file:
    # 	file_data = json.load(file)
    # # print(file_data['tags'])
    # tags.insert_one(file_data['tags'])
    # with open('Votes.json') as file:
    # 	file_data = json.load(file)
    # votes.insert_one(file_data['votes'])


def main():
    # port = input("Please enter the port you'd like to run the database on: ")
    client = pymongo.MongoClient("localhost", 27017)
    db = client['291db']
    createCollections(db)


if __name__ == "__main__":
    main()
