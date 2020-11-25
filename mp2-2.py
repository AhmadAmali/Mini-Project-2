# mini project 2 Phase 1, CMPUT291
import re, string
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

        colList = db.list_collection_names()
        if "tags" in colList:
            print("Tags collection created successfully.\n")
        if "posts" in colList:
            print("Posts collection created successfully.\n")
        if "votes" in colList:
            print("Votes collection created successfully.\n")
        createTerms(db)


def createTerms(db):
    # posts = db.posts.find("")
    # data = ijson.items(file, 'posts.row.item')
    # for i in data:
    #     print(i)
    remmoveHtml = re.compile('<.*?>')
    smallWords = re.compile(r'\W*\b\w{1,3}\b')
    i = 0
    for doc in db.Posts.find():
        if i != 50:
            try:
                # pass
                # title = doc['Title']
                # title = re.sub(remmoveHtml, '', doc['Title'])
                # title = re.sub(remmoveHtml, '', doc['Title']).strip(string.punctuation)
                # title = smallWords.sub('', re.sub(remmoveHtml, '', doc['Title']).strip(string.punctuation))
                title = smallWords.sub('', re.sub(remmoveHtml, '', doc['Title']).strip(string.punctuation)).split()
                print("TITLE", title)
            except:
                # print("no title")
                pass
            try:
                # pass
                # body = doc['Body']
                # body = re.sub(remmoveHtml, '', doc['Body'])
                # body = re.sub(remmoveHtml, '', doc['Body']).strip(string.punctuation)
                # body = smallWords.sub('', re.sub(remmoveHtml, '', doc['Body']).strip(string.punctuation))
                body = smallWords.sub('', re.sub(remmoveHtml, '', doc['Body']).strip(string.punctuation)).split()
                print("BODY", body)
            except:
                # print("no body")
                pass
            i += 1
        else:
            return

    # for post in posts:
    #     body = post["Body"].split()
    #     title = post["Title"].split()
    #     for word in body:
    #         if len(word) >= 3:
    #             terms.insert(0, word)  # add to array
    #         # do indexing here as you add to array
    #     for word in title:
    #         if len(word) >= 3:
    #             terms.insert(0, word)  # add to array
    # do indexing here as you add to array


def main():
    # port = input("Please enter the port you'd like to run the database on: ")
    client = pymongo.MongoClient("localhost", 27017)
    db = client['291db']
    createTerms(db)
    # createCollections(db)


if __name__ == "__main__":
    main()
