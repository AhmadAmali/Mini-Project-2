## mini project 2, CMPUT291

import pymongo


def mainMenu():
    user = input("Enter your user id now or type 'a' to continue anonymously: ")
    if user.lower() != 'a':
        displayReport(user)
    menuCondition = True
    task = input("""Select the task you would like to perform. You can also type E to exit\n 
    (P): Post a Question\n 
    (S): Search for Question\n
    (0): Exit Program\n""")
    while menuCondition:
        if task.lower() == 'p':  # add a question
            menuCondition = False
            postQuestion(user)
        elif task.lower() == 's':  # search for a post
            menuCondition = False
            searchQuestion(user)
        elif task.lower() == 'e':  # exit program
            quit()
        else:
            task = input("You inputted an incorrect choice, please try again: ")
            continue

def specificMenu(user, questionId):

    menuCondition = True
    task = input("""Select the task you would like to perform. You can also type E to exit\n 
    (A): Post an Answer\n 
    (L): List Answers for the Post\n
    (R): Return to Main Menu\n""")
    while menuCondition:
        if task.lower() == 'a':  # add an answer
            menuCondition = False
            answerQuestion(user, questionId)
        elif task.lower() == 'l':  # list the answers
            menuCondition = False
            listAnswers(user, questionId)
        elif task.lower() == 'r':  # return to main menu
            menuCondition = False
            mainMenu(user)
        elif task.lower() == 'e':  # exit program
            quit()
        else:
            task = input("You inputted an incorrect choice, please try again: ")
            continue

#If a user id is provided, the user will be shown a report that includes 
#(1) the number of questions owned and the average score for those questions, 
#(2) the number of answers owned and the average score for those answers, and 
#(3) the number of votes registered for the user
def displayReport(user):
    print("User report for " + user + "...\n")
    # questions = all question posts owned by the user
    questions = db.posts.find( $and:[ {"OwnerUserId": user},{"PostTypeId": "1"} ] )
    # count number of questions owned
    countAggr = questions.aggregate( { $count: "qcount" } )
    count = countAggr["qcount"]
    print("Number of questions owned: " + count)
    # find average score for questions
    scoreAggr = questions.aggregate( { average: { $avg: "$score" } } )
    avgScore = scoreAggr["average"]
    print("Average score for questions: " + avgScore)
    # answers = all answer posts owned by the user
    answers = db.posts.find( $and:[ {"OwnerUserId": user},{"PostTypeId": "2"} ] )
    # count number of answers owned
    countAggr = answers.aggregate( { $count: "acount" } )
    count = countAggr["acount"]
    print("Number of answers owned: " + count)
    # find average score for answers
    scoreAggr = answers.aggregate( { average: { $avg: "$score" } } )
    avgScore = scoreAggr["average"]
    print("Average score for answers: " + avgScore)
    # count number of votes where userid = user
    votes = db.votes.find( {"UserId": user} )
    countAggr = votes.aggregate( { $count: "vcount" } )
    count = countAggr["vcount"]
    print("Number of votes: " + count)

#search for current largest post id and increment by 1
def newPostId():
	#returns document: {"Id": max}
    maxDoc = db.posts.aggregate( Id: {$max : "$Id"} )
    maxId = max_doc["Id"]
    return maxId+1

#search for current largest vote id and increment by 1
def newVoteId():
	#returns document: {"Id": max}
    maxDoc = db.votes.aggregate( Id: {$max : "$Id"} )
    maxId = max_doc["Id"]
    return maxId+1

def postQuestion(user):
    title = input("Please enter your question title: ")
    body = input("Please enter your question body: ")
    Tags = input("Please enter the tags associated with the post, if multiple, seperate with comma: ")
    Tags = "".join(Tags.split())
    Tags = Tags.split(",") # returns a list with the seperated tags as such, if the input was: "<question>, <test>" Output would be ['<question>', '<test>']
    posts = db["posts"]
    newQuestion =       {"Id": newPostId(),
                         "PostTypeId": "1",
                         "CreationDate": date('now'),
                         "Score": 0,
                         "ViewCount": 0,
                         "Body": body,
                         "OwnerUserId": "11",
                         "LastActivityDate": date('now'),
                         "Title": title,
                         "Tags": Tags,
                         "AnswerCount": 0,
                         "CommentCount": 0,
                         "FavoriteCount": 0,
                         "ContentLicense": "CC BY-SA 2.5"
                         }
    posts.insert_one(newQuestion)
    print("New question added successfully")
    mainMenu()
    
def searchQuestion(user):
    specificMenu(user, questionId)

def answerQuestion(user, questionId):
    text = input("Enter the text for your answer: ")
    posts = db["posts"]
    newAnswer = 	{"Id": newPostId(),
                    "PostTypeId": "2",
                    "ParentId": questionId,
                    "CreationDate": date('now'),
                    "Score": 0,
                    "Body": text,
                    "OwnerUserId": user,
                    "LastActivityDate": date('now'),
                    "CommentCount": 0,
                    "ContentLicense": "CC BY-SA 2.5"}
    posts.insert_one(newAnswer)
    print("New answer added successfully")
    mainMenu()
    
def listAnswers(user, questionId):
    #return the specific question document
    question = db.posts.find( {"Id": questionId} )
    #find the accepted answer for that question
    accId = question["AcceptedAnswerId"]
    accAnswer = db.posts.find( {"Id": accId} )
    #print the accepted answer
    text = accAnswer["Body"]
    date = accAnswer["CreationDate"]
    score = accAnswer["Score"]
    print("Answer "+ accId + "* Body: " + '%.80s' %  text) #only prints up to 80 characters
    print("Answer "+ accId + "* Creation Date: " + date)
    print("Answer "+ accId + "* Score: " + score)
    #print the rest of the answers
    answers = db.posts.find( {"ParentId": questionId} )
    for answer in answers:
        aid = answer["Id"]
        if aid == accId: #skip printing the accepted answer
            continue
        text = answer["Body"]
        date = answer["CreationDate"]
        score = answer["Score"]
        print("Answer "+aid+" Body: " + '%.80s' % text) #only prints up to 80 characters
        print("Answer "+aid+" Creation Date: " + date)
        print("Answer "+aid+" Score: " + score)
    #allow user to select answer to print full document
    aidSelect = input("Select an answer by typing its id as shown above: ")
    result = db.posts.find({"Id": aidSelect})
    print(result)
    #allow user to vote on the answer or return to main menu
    task = input("""Select an action: 
        (V): Vote on Answer\n 
        (R): Return to Main Menu\n
        (E): Exit Program\n""")
    menuCondition = true
    while menuCondition:
        if task.lower() == 'v':  # add an vote
            menuCondition = False
            addVote(user, aidSelect)
        elif task.lower() == 'r':  # return to main menu
            menuCondition = False
            mainMenu(user)
        elif task.lower() == 'e':  # exit program
            quit()
        else:
            task = input("You inputted an incorrect choice, please try again: ")
            continue


def addVote(user, questionId):
    votes = db["Votes"]
    newVote = {"Id": newPostId(),
               "PostId": questionId,
               "VoteTypeId": "2",
               "UserId": user,
               "CreationDate": date('now')
               }
    Votes.insert_one(newVote)


def main():
    port = input("Please enter the port you'd like to run the database on: ")
    client = pymongo.MongoClient("localhost", 27017)
    db = client['291db']
    mainMenu()

if __name__ == "__main__":
    main()

