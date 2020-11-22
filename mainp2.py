## mini project 2, CMPUT291

import pymongo

port = input("Please enter the port you'd like to run the database on: ")
client = pymongo.MongoClient("localhost", 27017)
db = client.project


def mainMenu():
	user = input("Enter your user id now or type 'a' to continue anonymously: ")
	if user.lower() != 'a':
		displayReport(user)
	
	menuCondition = True
    task = input("""Select the task you would like to perform. You can also type 0 to exit\n 
    (P): Post a Question\n 
    (S): Search for Question\n""")
    while menuCondition:
        if task.lower() == 'p':  # add a question
            menuCondition = False
            postQuestion(user)
        elif task.lower() == 's':  # search for a post
            menuCondition = False
            searchQuestion(user)
        elif task.lower() == '0':  # exit program
            quit()
        else:
            task = input("You inputted an incorrect choice, please try again: ")
            continue

def specificMenu(user, questionId):
	
	menuCondition = True
    task = input("""Select the task you would like to perform. You can also type 0 to exit\n 
    (A): Post an Answer\n 
    (L): List Answers for the Post\n 
    (V): Vote on this Post\n 
    (R): Return to Main Menu\n""")
    while menuCondition:
        if task.lower() == 'a':  # add an answer
            menuCondition = False
            answerQuestion(user, questionId)
        elif task.lower() == 'l':  # list the answers
            menuCondition = False
            listAnswers(questionId)
        elif task.lower() == 'v':  # vote for the post
            menuCondition = False
            addVote(user, questionId)
        elif task.lower() == 'r':  # return to main menu
            menuCondition = False
            mainMenu(user)
        elif task.lower() == '0':  # exit program
            quit()
        else:
            task = input("You inputted an incorrect choice, please try again: ")
            continue

#If a user id is provided, the user will be shown a report that includes 
#(1) the number of questions owned and the average score for those questions, 
#(2) the number of answers owned and the average score for those answers, and 
#(3) the number of votes registered for the user
def displayReport(user):
	continue

#search for current largest post id and increment by 1
def newPostId():
	continue

def postQuestion(user):
    continue
    
def searchQuestion(user):

	specificMenu(user, questionId)
    continue

def answerQuestion(user, questionId):
	text = input("Enter the text for your answer: ")
	posts = db["posts"]
	newAnswer = {   "Id": newPostId(),
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
    continue
    
def listAnswers(questionId):
    continue

def addVote(user, questionId):
    continue

def main():
    continue 
