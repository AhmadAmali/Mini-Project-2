## mini project 2, CMPUT291

import pymongo
import datetime, time
from prettytable import PrettyTable
from pprint import pprint


def mainMenu(db):
    user = input("Enter your user id now or type 'a' to continue anonymously: ")
    if user.lower() != 'a':
        displayReport(user, db)
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
            searchQuestion(db)
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
            mainMenu(db)
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
    posts = db["posts"]
    votes = db["votes"]
    print("User report for " + user + "...\n")
    # questions = all question posts owned by the user
    # questions = posts.row.find({},"$and":[{"OwnerUserId": user},{"PostTypeId": "1"}])
    # count number of questions owned
    countAggr = questions.aggregate({"$count": "qcount"})
    count = countAggr["qcount"]
    print("Number of questions owned: " + count)
    # find average score for questions
    scoreAggr = questions.aggregate({average: {"$avg": "$score"}})
    avgScore = scoreAggr["average"]
    print("Average score for questions: " + avgScore)
    # answers = all answer posts owned by the user
    # answers = posts.row.find("$and":[{"OwnerUserId": user},{"PostTypeId": "2"}])
    # count number of answers owned
    countAggr = answers.aggregate({"$count": "acount"})
    count = countAggr["acount"]
    print("Number of answers owned: " + count)
    # find average score for answers
    scoreAggr = answers.aggregate({average: {"$avg": "$score"}})
    avgScore = scoreAggr["average"]
    print("Average score for answers: " + avgScore)
    # count number of votes where userid = user
    votedoc = votes.row.find({"UserId": user})
    countAggr = votedoc.aggregate({"$count": "vcount"})
    count = countAggr["vcount"]
    print("Number of votes: " + count)


# search for current largest post id and increment by 1
def newPostId(db):
    # returns document: {"Id": max}
    posts = db["posts"]
    maxDoc = db.posts.find().sort("Id", -1).limit(1)
    maxVal = 0
    for x in maxDoc:
        maxVal = x['Id']
    maxVal = int(maxVal) + 1
    return str(maxVal)


# search for current largest vote id and increment by 1
def newVoteId(db):
    # returns document: {"Id": max}
    votes = db["votes"]
    maxObject = votes.find().sort("Id", -1).limit(1)
    maxID = 0
    for x in maxObject:
        maxID = x['Id']
    maxID = int(maxID) + 1
    return str(maxID)


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
    Tags = Tags.split(
        ",")  # returns a list with the seperated tags as such, if the input was: "<question>, <test>" Output would be ['<question>', '<test>']
    posts = db["posts"]
    newQuestion = {"Id": newPostId(db),
                   "PostTypeId": "1",
                   "CreationDate": getCurrentDay(),
                   "Score": 0,
                   "ViewCount": 0,
                   "Body": body,
                   "OwnerUserId": "11",
                   "LastActivityDate": getCurrentDay(),
                   "Title": title,
                   "Tags": Tags,
                   "AnswerCount": 0,
                   "CommentCount": 0,
                   "FavoriteCount": 0,
                   "ContentLicense": "CC BY-SA 2.5"
                   }
    Posts.insert_one(newQuestion)
    print("New question added successfully")
    mainMenu(db)


def searchQuestion(db):  # handles search functionality here
    kw_check = True
    keywords = ''
    while kw_check:
        if not keywords:
            keywords = input("Please enter keywords separated by a comma (press 0 to return to main menu): ")
        else:
            kw_check = False
    if keywords.lower() == '0':
        mainMenu(db)
    keywords = "".join(keywords.split()).split(",")  # user inputted keywords

    print(keywords)
    # mongodb query to retrieve search results
    posts = db.Posts.find(
        {"$and": [{"PostTypeId": "1"}, {"Terms": {"$in": keywords}}]})

    all_data = []
    # result parsing
    print(posts.count(), "results found")
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
    start = time.time()
    print_search_table(all_data)  # print results in table using print_search_table
    end = time.time()
    print("Search in", end - start, "seconds")


def print_search_table(data):  # handle printing the table here
    table = PrettyTable(['ID', 'Title', 'Creation Date', 'Score', 'Answers'])
    for i in data:  # prints data in table format (prints all results)
        table.add_row(i)
    print(table)


def answerQuestion(user, questionId, db):
    text = input("Enter the text for your answer: ")
    posts = db["posts"]
    newAnswer = {"Id": newPostId(),
                 "PostTypeId": "2",
                 "ParentId": questionId,
                 "CreationDate": getCurrentDay(),
                 "Score": 0,
                 "Body": text,
                 "OwnerUserId": user,
                 "LastActivityDate": getCurrentDay(),
                 "CommentCount": 0,
                 "ContentLicense": "CC BY-SA 2.5"}
    posts.insert_one(newAnswer)
    print("New answer added successfully")
    mainMenu(db)


def listAnswers(user, questionId, db):
    posts = db["posts"]
    votes = db["votes"]
    # return the specific question document
    question = posts.find_one({"Id": questionId})
    # find the accepted answer for that question
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
    for answer in answers:
        aid = answer["Id"]
        if aid == accId:  # skip printing the accepted answer
            continue
        text = answer["Body"]
        date = answer["CreationDate"]
        score = answer["Score"]
        print("Answer " + aid + " Body: " + '%.80s' % text)  # only prints up to 80 characters
        print("Answer " + aid + " Creation Date: " + date)
        print("Answer " + aid + " Score: " + str(score))
    # allow user to select answer to print full document
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
            mainMenu(db)
        elif task.lower() == 'e':  # exit program
            quit()
        else:
            task = input("You inputted an incorrect choice, please try again: ")
            continue


def addVote(user, questionId, db):
    votes = db["Votes"]
    if user.lower() == "a":
        newVote = {"Id": newVoteId(db),
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
        mainMenu(db)
    voteObject = db.Votes.find({"UserId": user, "PostId": questionId})
    splicedDay = getCurrentDay()
    for x in voteObject:
        if x["CreationDate"][:9] == splicedDay[:9]:
            print("user has already voted today!")
            mainMenu(db)
        else:
            continue
    newVote = {"Id": newVoteId(db),
               "PostId": postId,
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
    mainMenu(db)


def main():
    port = int(input("Please enter the port you'd like to run the database on: "))
    client = pymongo.MongoClient("localhost", port)
    db = client['291db']
    mainMenu(db)


if __name__ == "__main__":
    main()
