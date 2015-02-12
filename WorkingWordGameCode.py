import time
from random import randint
import contains
contains.contains("admission", "admit")
False
contains.contains("admission", "admin")
True

print("Welcome to WordGame!!!\n")

wordsFileName = '/usr/share/dict/words'

fullWordList = []
wordsSevenOrLonger = []
sourceWord = ''
usersWords = []
sourceLetters = []

with open(wordsFileName) as words:
    for word in words:
        fullWordList.append(word.strip())

for word in fullWordList:
    if(len(word.strip()) >= 7 and "'" not in word.strip()):
        wordsSevenOrLonger.append(word)

sourceWord = wordsSevenOrLonger[randint(1, len(wordsSevenOrLonger))]
for letter in sourceWord:
    sourceLetters.append(letter)
print("The source word is: " + sourceWord + "\n")
print("Now make 7 words from the letters of the word above.\nEach must be 3 letters or more and a real word \n")

#Take first timestamp here
start = time.time()

while len(usersWords) != 7:
    usersWords.append(input())

#Take second timestamp here
end = time.time()

print("Checking if words are valid\n")
invalidWordList = []

for word in usersWords:
    problemFound = False
    #check word is made from letters in source word
    if problemFound is False:
        #for letter in word:
            #if letter not in sourceLetters:
                #invalidWordList.append(word)
                #problemFound = True
        if contains.contains(sourceWord, word) == False:
            invalidWordList.append(word)
            '''print("Error")'''
            problemFound = True
    #and uses only the number of each letter that exists
    if problemFound is False:
        #check word has more than 3 letters
        if len(word) < 3:
            invalidWordList.append(word)
            problemFound = True
    if problemFound is False:
        #check if a word is the source word
        if word == sourceWord:
            invalidWordList.append(word)
            problemFound = True
    if problemFound is False:
        #check if word exists
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
        

if len(invalidWordList) == 0:
    print("All word are valid.")
elif len(invalidWordList) > 0:
    if len(invalidWordList) > 1:
        print("You had " + str(len(invalidWordList)) + " invalid words. Here they are: ")
    else :  print("You had 1 invalid word. Here it is: ")
    for word in invalidWordList:
        print(word)
    #print("A child could have done better than you.......")

timeToFinish = end - start

print("It took you " + str(timeToFinish) + " seconds to complete the challenge")
