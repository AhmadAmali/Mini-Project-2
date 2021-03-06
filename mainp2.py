## mini project 2, CMPUT291

import pymongo
import datetime, time
from prettytable import PrettyTable
from pprint import pprint
import random
import string


def login(db):
    user = input("Enter your user id now or type 'a' to continue anonymously: ")
    user = user.lower()
    if user.lower() != 'a':
        displayReport(user, db)
    mainMenu(user, db)


def mainMenu(user, db):
    menuCondition = True
    task = input("""Select the task you would like to perform. You can also type E to exit\n 
    (P): Post a Question\n 
    (S): Search for Question\n
    (E): Exit Program\n""")
    while menuCondition:
        if task.lower() == 'p':  # add a question
            menuCondition = False
            postQuestion(user, db)
        elif task.lower() == 's':  # search for a post
            menuCondition = False
            searchQuestion(user, db)
        elif task.lower() == 'e':  # exit program
            quit()
        else:
            task = input("You inputted an incorrect choice, please try again: ")
            continue

def specificMenu(user, questionId, db):
    menuCondition = True
    task = input("""Select the task you would like to perform. You can also type E to exit\n 
    (A): Post an Answer\n 
    (L): List Answers for the Post\n
    (V): Vote on Selected Post\n
    (E): Exit Program\n
    (R): Return to Main Menu\n""")
    while menuCondition:
        if task.lower() == 'a':  # add an answer
            menuCondition = False
            answerQuestion(user, questionId, db)
        elif task.lower() == 'l':  # list the answers
            menuCondition = False
            listAnswers(user, questionId, db)
        elif task.lower() == 'r':  # return to main menu
            menuCondition = False
            mainMenu(user, db)
        elif task.lower() == 'v':  # add a vote to the question
            addVote(user, questionId, db)
        elif task.lower() == 'e':  # exit program
            quit()
        else:
            task = input("You inputted an incorrect choice, please try again: ")
            continue


# If a user id is provided, the user will be shown a report that includes
# (1) the number of questions owned and the average score for those questions,
# (2) the number of answers owned and the average score for those answers, and
# (3) the number of votes registered for the user
def displayReport(user, db):
    posts = db["Posts"]
    votes = db["Votes"]
    print("User report for " + user + "...\n")
    # questions = all question posts owned by the user
    questions = posts.find({"OwnerUserId": user})
    # count number of questions owned
    count = 0
    for ques in questions:
        if ques["PostTypeId"] == "1":
            count += 1
    print("Number of questions owned: " + str(count))
    # find average score for questions
    questions = posts.find({"OwnerUserId": user})
    scoreSum = 0
    for ques in questions:
        if ques["PostTypeId"] == "1":
            scoreSum += ques["Score"]
    avg = 0
    if count != 0:
        avg = scoreSum / count
    print("Average score for questions: " + str(avg))
    # answers = all answer posts owned by the user
    answers = posts.find({"OwnerUserId": user})
    # count number of answers owned
    count = 0
    for ans in answers:
        if ans["PostTypeId"] == "2":
            count += 1
    print("Number of answers owned: " + str(count))
    # find average score for answers
    answers = posts.find({"OwnerUserId": user})
    scoreSum = 0
    for ans in answers:
        if ans["PostTypeId"] == "2":
            scoreSum += ans["Score"]
    avg = 0
    if count != 0:
        avg = scoreSum / count
    print("Average score for answers: " + str(avg))
    # count number of votes where userid = user
    vs = votes.find({"UserId": user})
    count = 0
    for v in vs:
        count += 1
    print("Number of votes: " + str(count))


# search for current largest post id and increment by 1
def newPostId(db):
    newId = ''.join(random.choice(string.digits) for i in range(
        8))  # method for generating alphanumeric strings used from this source, all credit goes to the creator: https://pythonexamples.org/python-generate-random-string-of-specific-length/
    newId = 'p' + newId
    return str(newId)


# returns the current day in the same format as the date in the provided json files
def getCurrentDay():
    current = datetime.datetime.now()
    current = str(current)
    new_current = current.replace(" ", "T")
    return new_current


def postQuestion(user, db):
    title = input("Please enter your question title: ")
    body = input("Please enter your question body: ")
    Tags = input("Please enter the tags associated with the post, if multiple, seperate with comma: ")
    Tags = "".join(Tags.split())
    Tags = Tags.split(",")  # returns a list with the seperated tags as such, if the input was: "<question>, <test>" Output would be ['<question>', '<test>']
    tagStr = ''
    for tag in Tags:
        tagStr += '<' + tag + '>'
    posts = db["Posts"]
    newid = newPostId(db)
    newQuestion =       {"Id": newid,
                         "PostTypeId": "1",
                         "CreationDate": getCurrentDay(),
                         "Score": 0,
                         "ViewCount": 0,
                         "Body": body,
                         "LastActivityDate": getCurrentDay(),
                         "Title": title,
                         "Tags": tagStr,
                         "AnswerCount": 0,
                         "CommentCount": 0,
                         "FavoriteCount": 0,
                         "ContentLicense": "CC BY-SA 2.5"
                         }
    posts.insert_one(newQuestion)
    if user != "a":
        oldValue = {"Id": newid}
        newValue = {"$set": {"OwnerUserId": user}}
        posts.update_one(oldValue, newValue)
    print("New question added successfully")
    mainMenu(user, db)


def searchQuestion(user, db):

    kw_check = True
    keywords = ''
    while kw_check:
        if not keywords:
            keywords = input("Please enter keywords separated by a comma (press 0 to return to main menu): ")
        else:
            kw_check = False
    if keywords.lower() == '0':
        mainMenu(user, db)
    keywords = "".join(keywords.split()).split(",")  # user inputted keywords

    # mongodb query to retrieve search results
    posts = db.Posts.find(
        {"$and": [{"PostTypeId": "1"}, {"Terms": {"$in": keywords}}]})

    all_data = []
    # result parsing
    p_count = posts.count()
    print(p_count, "results found")
    for post in posts:
        data = []
        try:
            data.append(post["Id"])
        except:
            data.append("N/A")
        try:
            data.append(post["Title"])
        except:
            data.append("N/A")
        try:
            data.append(post["CreationDate"])
        except:
            data.append("N/A")
        try:
            data.append(post["Score"])
        except:
            data.append("N/A")
        try:
            data.append(post["AnswerCount"])
        except:
            data.append("N/A")
        all_data.append(data)
    #start = time.time()
    print_search_table(all_data)  # print results in table using print_search_table
    #end = time.time()
    #print("Search in", end - start, "seconds")

    if p_count == 0:
        mainMenu(user, db)

    valid_input = True
    while valid_input:
        questionID = input("Enter post ID to select or '0' to return to main menu: ")
        if questionID == '0':
            valid_input = False
            mainMenu(user, db)
        else:
            if checkExists(questionID, db) is not False:
                valid_input = False
                for doc in db.Posts.find({"Id": questionID}):
                    pprint(doc)
                    v_count = doc["ViewCount"] + 1
                    db.Posts.update_one({"Id": questionID}, {"$set": {"ViewCount": v_count}})
                specificMenu(user, questionID, db)


def checkExists(postid, db):
    if db.Posts.find({"Id": postid}).count() > 0:
        return True
    else:
        print("Invalid Input. Please Try again")
        return False

def print_search_table(data):  # handle printing the table here
    table = PrettyTable(['ID', 'Title', 'Creation Date', 'Score', 'Answers'])
    for i in data:  # prints data in table format (prints all results)
        table.add_row(i)
    print(table)


def answerQuestion(user, questionId, db):
    text = input("Enter the text for your answer: ")
    posts = db["Posts"]
    newid = newPostId(db)
    newAnswer = {"Id": newid,
                 "PostTypeId": "2",
                 "ParentId": questionId,
                 "CreationDate": getCurrentDay(),
                 "Score": 0,
                 "Body": text,
                 "LastActivityDate": getCurrentDay(),
                 "CommentCount": 0,
                 "ContentLicense": "CC BY-SA 2.5"}
    posts.insert_one(newAnswer)
    if user != "a":
        oldValue = {"Id": newid}
        newValue = {"$set": {"OwnerUserId": user}}
        posts.update_one(oldValue, newValue)
    print("New answer added successfully")
    mainMenu(user, db)


def listAnswers(user, questionId, db):
    posts = db["Posts"]
    votes = db["Votes"]
    # return the specific question document
    question = posts.find_one({"Id": questionId})
    # find the accepted answer for that question if there is one
    if hasattr(question, "AcceptedAnswerId"):
        accId = question["AcceptedAnswerId"]
        accAnswer = posts.find_one({"Id": accId})
        # print the accepted answer
        text = accAnswer["Body"]
        date = accAnswer["CreationDate"]
        score = accAnswer["Score"]
        print("Answer " + accId + "* Body: " + '%.80s' % text)  # only prints up to 80 characters
        print("Answer " + accId + "* Creation Date: " + date)
        print("Answer " + accId + "* Score: " + str(score))
    # print the rest of the answers
    answers = posts.find({"ParentId": questionId})
    # if no answers in the list
    if not answers:
        print("No Answers for this Question\n")
    for answer in answers:
        aid = answer["Id"]
        if hasattr(question, "AcceptedAnswerId"):
            if aid == accId:  # skip printing the accepted answer
                continue
        text = answer["Body"]
        date = answer["CreationDate"]
        score = answer["Score"]
        print("Answer " + aid + " Body: " + '%.80s' % text)  # only prints up to 80 characters
        print("Answer " + aid + " Creation Date: " + date)
        print("Answer " + aid + " Score: " + str(score))
    # allow user to select answer to print full document
    if not answers:
        mainMenu(user, db)
    else:
        aidSelect = input("Select an answer by typing its id as shown above: ")
        result = posts.find_one({"Id": aidSelect})
        pprint(result)
        # allow user to vote on the answer or return to main menu
        task = input("""Select an action: 
			(V): Vote on Answer\n 
			(R): Return to Main Menu\n
			(E): Exit Program\n""")
        menuCondition = True
        while menuCondition:
            if task.lower() == 'v':  # add an vote
                menuCondition = False
                addVote(user, aidSelect, db)
            elif task.lower() == 'r':  # return to main menu
                menuCondition = False
                mainMenu(user, db)
            elif task.lower() == 'e':  # exit program
                quit()
            else:
                task = input("You inputted an incorrect choice, please try again: ")
                continue


def addVote(user, questionId, db):
    votes = db["Votes"]
    if user.lower() == "a":
        newVote = {"Id": newPostId(db),
                   "PostId": questionId,
                   "VoteTypeId": "2",
                   "CreationDate": getCurrentDay()
                   }
        votes.insert_one(newVote)
        posts = db["Posts"]
        score = posts.find_one({"Id": questionId})
        x = score["Score"]
        newScore = x + 1
        oldValue = {"Id": questionId}
        newValue = {"$set": {"Score": newScore}}
        db.Posts.update_one(oldValue, newValue)
        print("vote added succesfully")
        mainMenu(user, db)
    voteObject = db.Votes.find({"UserId": user, "PostId": questionId})
    splicedDay = getCurrentDay()
    for x in voteObject:
        if x["CreationDate"][:9] == splicedDay[:9]:
            print("user has already voted today!")
            mainMenu(user, db)
        else:
            continue
    newVote = {"Id": newPostId(db),
               "PostId": questionId,
               "VoteTypeId": "2",
               "UserId": user,
               "CreationDate": getCurrentDay()
               }
    votes.insert_one(newVote)
    posts = db["Posts"]
    score = posts.find_one({"Id": questionId})
    x = score["Score"]
    newScore = x + 1
    oldValue = {"Id": questionId}
    newValue = {"$set": {"Score": newScore}}
    db.Posts.update_one(oldValue, newValue)
    print("vote added succesfully")
    mainMenu(user, db)


def main():
    port = int(input("Please enter the port you'd like to run the database on: "))
    client = pymongo.MongoClient("localhost", port)
    db = client['291db']
    login(db)
    # searchQuestion(user,db)


if __name__ == "__main__":
    main()
