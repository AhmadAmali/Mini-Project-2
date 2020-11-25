# mini project 2 Phase 1, CMPUT291
import re
from functools import partial

import pymongo
import json
import time


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
    votes = db["Votes"]

    # read json files and insert them into collections
    start = time.time()
    with open('Posts.json') as file:
        read_data = file.read()
        data = json.loads(read_data)
        posts.insert_many(data['posts']['row'])
        end = time.time()
        print("Posts collection created in ", end - start, "seconds")

    with open('Tags.json') as file:
        read_data = file.read()
        data = json.loads(read_data)
        tags.insert_many(data['tags']['row'])
        end = time.time()
        print("Tags collection created in ", end - start, "seconds")

    with open('Votes.json') as file:
        read_data = file.read()
        data = json.loads(read_data)
        votes.insert_many(data['votes']['row'])
        end = time.time()
        print("Votes collection created in ", end - start, "seconds")

        colList = db.list_collection_names()
        if "tags" in colList:
            print("Tags collection created successfully.\n")
        if "posts" in colList:
            print("Posts collection created successfully.\n")
        if "votes" in colList:
            print("Votes collection created successfully.\n")
        createTerms(db)


def createTerms(db):
    start = time.time()

    p1 = '[^a-zA-Z ]'
    p2 = '<.*?>'
    p3 = r'\W*\b\w{1,2}\b'
    pattern = re.compile("(%s|%s|%s)" % (p3, p1, p2))

    for doc in db.Posts.find().sort([("$natural", 1)]):
        raw_terms = ''
        try:
            raw_terms = doc['Title']
        except KeyError:
            # print("no title")
            pass
        try:
            raw_terms = raw_terms + '  ' + doc['Body']
        except KeyError:
            # print("no body")
            pass
        try:
            raw_terms = raw_terms + ' ' + doc["Tags"]
        except KeyError:
            pass
        try:
            print(doc['Id'])
            db.Posts.update({"_id": doc['_id']}, {"$set": {"Terms": list(set(pattern.sub(' ', raw_terms.lower()).split()))}})
        except:
            pass
    end = time.time()
    print("Terms Created in ", end - start, "seconds")


def main():
    port = int(input("Please enter the port you'd like to run the database on: "))
    client = pymongo.MongoClient("localhost", port)
    db = client['291db']
    # createTerms(db)
    createCollections(db)


if __name__ == "__main__":
    main()
