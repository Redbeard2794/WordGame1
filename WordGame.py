from flask import Flask, render_template, url_for, request, redirect, flash, session
import time
from datetime import datetime
from threading import Thread
from random import randint
import operator
import contains
contains.contains("admission", "admit")
False
contains.contains("admission", "admin")
True

app = Flask(__name__)

wordsFileName = 'words.txt'
fullWordList = []
wordsSevenOrLonger = []
sourceWord = ''
sourceLetters = []
usersWords = []
invalidWordList = []
start = 0
end = 0
timeToFinish = 0
#display the home page
@app.route('/')
def display_home():
    del usersWords[:]
    return render_template("homePage.html", 
                            the_title="Welcome to the Word Game",
                            play_url=url_for("play"),
                            leaderboard_url=url_for("showleaderboard"),)
#page that the actual game takes place on
@app.route('/play')
def play():
    start = time.time()
    fullWordList = loadAllWords()
    wordsSevenOrLonger = loadSourceWords()
    sourceWord = selectSourceWord()
    sourceLetters = getSourceWordLetters()
    del usersWords[:]
    return render_template("play.html",
                            the_title="You are now playing the wordGame.",
                            the_source = sourceWord,
                            submit_url=url_for('showResults'),
                            the_time = start)
#show the user any invalid words and how long it took them to finish the game. Also requests their name
@app.route('/showResults', methods=["POST"])
def showResults():
    end = time.time()
    del usersWords[:]
    usersWords.append(request.form['user_word1'])
    usersWords.append(request.form['user_word2'])
    usersWords.append(request.form['user_word3'])
    usersWords.append(request.form['user_word4'])
    usersWords.append(request.form['user_word5'])
    usersWords.append(request.form['user_word6'])
    usersWords.append(request.form['user_word7'])

    sourceWord = request.form['source_word']
    checkUsersWords(sourceWord)
    start = float(request.form['start_time'])

    timeToFinish = end - start

    return render_template("showResults.html",
                            the_title="Here are your results.",
                            the_words = invalidWordList,
                            the_time = str(timeToFinish),
                            submit_url=url_for('saveleaderboard'),)
    
#shows the top 10 players on the leaderboard. Alos tells the player where they were placed after they played a game
@app.route('/leaderboard')
def showleaderboard():

    fullBoard = []
    nameList = []
    timeList = []
    leaderDict = {}
    #get full leaderboard
    with open("leaderboard.log") as lines:
        for line in lines:
            fullBoard.append(line.strip())
    #split into list of names and list of times
    count= 0;
    for line in fullBoard:
        for i in line.split(","):
            if(count%2):
                timeList.append(float(i))
            else:
                nameList.append(i)
            count+=1
    #Store names and times in dictionary. names = keys, times = values
    i = 0
    while i is not len(nameList):
        leaderDict[nameList[i]] = timeList[i]
        i+=1
    
    #sort the dictionary into a list(ends up as a list of tuples)    
    sortedLeaders = sorted(leaderDict.items(), key=operator.itemgetter(1))
    #list of leaders in order
    sortedLeaderList = []
    for thing in sortedLeaders:
        sortedLeaderList.append(thing)
    
    index = 0
    for player in sortedLeaderList:
        with open("fullSortedLeaderboard.log", "a") as log:
            print(sortedLeaderList[index], file=log)
        index+=1
    #this was for testing
    findCurr = 0
    
    currPlayer = session.get("the_last_user")

    foundCurr = False
    d = 0
    print(currPlayer)

    print(len(sortedLeaderList))
    #if the player has played a game then do this
    if currPlayer != None:
        #find where the player was placed after they played the wordGame
        index1 = 0
        for line in sortedLeaderList:
            if currPlayer in str(line):
                d = index1+1
            else : index1+=1


    return render_template("leaderboard.html",
                            the_title="Here is the top ten",
                            theTen=sortedLeaderList,
                            currPlayer_name=currPlayer,
                            curr_player_place=d,
                            home_url=url_for('display_home'))

#tell the leaderboard to update. Show invalid words and time
@app.route('/saveleaderboard', methods=["POST"])
def saveleaderboard():
    print(usersWords)
    all_ok = True
    if request.form["user_name"] == "":
        flash("Sorry, you must provide a user name.")
        all_ok = False
    if all_ok:
        t = Thread(target=update_leaderboard, args=(request.form['user_name'], request.form['finish_time']))
        t.start()
        session["the_last_user"] = request.form["user_name"]

        del usersWords[:]
        del invalidWordList[:]
        print(usersWords)
        return redirect(url_for("display_home"))
    else:
        return redirect(url_for("showResults"))

#load all possible words
def loadAllWords():
    with open(wordsFileName) as words:
        for word in words:
            fullWordList.append(word.strip())
        return fullWordList
#load all the possible source words
def loadSourceWords():
    for word in fullWordList:
        if(len(word.strip()) >= 7 and "'" not in word.strip()):
            wordsSevenOrLonger.append(word)
    return wordsSevenOrLonger
#select a source word
def selectSourceWord():
    sourceWord = wordsSevenOrLonger[randint(1, len(wordsSevenOrLonger))]
    return sourceWord
#get the letters in the source word
def getSourceWordLetters():
    for letter in sourceWord:
        sourceLetters.append(letter)
    return sourceLetters


def update_leaderboard(name, time):
    #update the leaderboard
    with open("leaderboard.log", "a") as log:
        print(name,',',time, file=log)

def checkUsersWords(sourceWord):
    for word in usersWords:
        problemFound = False
        #check word is made from letters in source word
        if problemFound is False:
            if contains.contains(sourceWord, word) == False:
                invalidWordList.append(word)
                problemFound = True

        #check word has more than 3 letters
        if problemFound is False:
            if len(word) < 3:
                invalidWordList.append(word)
                problemFound = True

        #check if a word is the source word
        if problemFound is False:
            if word == sourceWord:
                invalidWordList.append(word)
                problemFound = True

        #check if word exists
        if problemFound is False:
            if word not in fullWordList:
                invalidWordList.append(word)
                problemFound = True

        if problemFound is False:
            #check if word is a duplicate
            timesWordOccurs = 0
            for w in usersWords:
                if word == w:
                    timesWordOccurs +=1
            if timesWordOccurs > 1:
                invalidWordList.append(word)
                problemFound = True
                

app.config["SECRET_KEY"] = 'theDarknessWithAdobOf3'
if __name__ == "__main__":
    app.run(debug=True)






                        
        



