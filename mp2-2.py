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
    with open('Posts.json') as file:
        read_data = file.read()
        data = json.loads(read_data)
        posts.insert_many(data['posts']['row'])
        print("Done Posts")

    with open('Tags.json') as file:
        read_data = file.read()
        data = json.loads(read_data)
        tags.insert_many(data['tags']['row'])
        print("Done Tags")

    with open('Votes.json') as file:
        read_data = file.read()
        data = json.loads(read_data)
        votes.insert_many(data['votes']['row'])
        print("Done Votes")

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
    removeNonletter = re.compile('[^a-zA-Z ]')
    remmoveHtml = re.compile('<.*?>')
    smallWords = re.compile(r'\W*\b\w{1,2}\b')

    for doc in db.Posts.find().sort([("$natural", 1)]):
        raw_terms = ''
        try:
            raw_terms = doc['Title']
        except KeyError:
            # print("no title")
            pass
        try:
            raw_terms = raw_terms + ' ' + doc['Body']
        except KeyError:
            # print("no body")
            pass
        try:
            # print(raw_terms)
            print(doc['Id'])
            db.Posts.update({"Id": doc['Id']}, {"$set": {"Terms": list(dict.fromkeys((removeNonletter.sub('', smallWords.sub('', re.sub(remmoveHtml, '', raw_terms.lower())))).split()))}})
        except:
            pass
    end = time.time()
    print("TIME: ", end - start)

# def parseTerms(doc):  // not required delete later
    # removeNonletter = re.compile('[^a-zA-Z ]')
    # remmoveHtml = re.compile('<.*?>')
    # smallWords = re.compile(r'\W*\b\w{1,2}\b')

    # terms = doc.lower()
    # terms = re.sub(remmoveHtml, '', terms)
    # terms = smallWords.sub('', terms)
    # terms = removeNonletter.sub('', terms)
    # terms = terms.split()
    # terms = list(dict.fromkeys(terms))

    # return terms


def main():
    # port = input("Please enter the port you'd like to run the database on: ")
    client = pymongo.MongoClient("localhost", 27017)
    db = client['291db']
    createTerms(db)
    # createCollections(db)


if __name__ == "__main__":
    main()
