# mini project 2 Phase 1, CMPUT291
import re
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
        # createTerms(db)


def createTerms(db):
    for doc in db.Posts.find():
        postID = doc['Id']
        print(postID)
        raw_terms = ''
        try:
            raw_terms = doc['Title']
        except:
            # print("no title")
            pass
        try:
            raw_terms = raw_terms + doc['Body']
        except:
            # print("no body")
            pass
        terms = parseTerms(raw_terms)
        print(terms)
        db.Posts.update({"Id": postID}, {"$set": {"Terms": terms}})


def parseTerms(doc):
    removeNonletter = re.compile('[^a-zA-Z ]')
    remmoveHtml = re.compile('<.*?>')
    smallWords = re.compile(r'\W*\b\w{1,2}\b')

    terms = doc.lower()
    terms = re.sub(remmoveHtml, '', terms)
    terms = smallWords.sub('', terms)
    terms = removeNonletter.sub('', terms)
    terms = terms.split()
    terms = list(dict.fromkeys(terms))

    return terms


def main():
    # port = input("Please enter the port you'd like to run the database on: ")
    client = pymongo.MongoClient("localhost", 27018)
    db = client['291db']
    # createTerms(db)
    createCollections(db)


if __name__ == "__main__":
    main()
