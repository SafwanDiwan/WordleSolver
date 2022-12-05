import time
from game import *
import random

WORDLEN = 5 # The length of the correct answer and guessed words
INITGUESS = "TARES" # The first guess

stateSpace = {} # Global value to demonstrate the state space

def resetStateSpace(): # Function to reset state space. Is run after every game play. Keys are letters, and
                            # values are a list where the first value is if the letter was previously guessed.
    global stateSpace
    stateSpace = {
    "a" : [0, 1, 1, 1, 1, 1], "b" : [0, 1, 1, 1, 1, 1], "c" : [0, 1, 1, 1, 1, 1], "d" : [0, 1, 1, 1, 1, 1], "e" : [0, 1, 1, 1, 1, 1], "f" : [0, 1, 1, 1, 1, 1], "g" : [0, 1, 1, 1, 1, 1], "h" : [0, 1, 1, 1, 1, 1],
    "i" : [0, 1, 1, 1, 1, 1], "j" : [0, 1, 1, 1, 1, 1], "k" : [0, 1, 1, 1, 1, 1], "l" : [0, 1, 1, 1, 1, 1], "m" : [0, 1, 1, 1, 1, 1], "n" : [0, 1, 1, 1, 1, 1], "o" : [0, 1, 1, 1, 1, 1], "p" : [0, 1, 1, 1, 1, 1],
    "q" : [0, 1, 1, 1, 1, 1], "r" : [0, 1, 1, 1, 1, 1], "s" : [0, 1, 1, 1, 1, 1], "t" : [0, 1, 1, 1, 1, 1], "u" : [0, 1, 1, 1, 1, 1], "v" : [0, 1, 1, 1, 1, 1], "w" : [0, 1, 1, 1, 1, 1], "x" : [0, 1, 1, 1, 1, 1],
    "y" : [0, 1, 1, 1, 1, 1], "z" : [0, 1, 1, 1, 1, 1]
}

def updateStateSpace(guess, result): # Update state space as a result of each guess.
    global stateSpace
    count = 0
    for letter in guess:
        placement = stateSpace.get(letter)
        if result[count] == '*': # If letter is in word and in correct position
            for value in stateSpace: # Loop through state space and update all values to 0
                if value != letter: # Makes sure that the value that we are looking at isn't changed to 0
                    holder = stateSpace.get(value)
                    holder[count+1] = 0
                    stateSpace.update({value : holder})
            placement[count+1] = 2
        elif result[count] == '-': # If letter in word but not in correct position
            placement[count+1] = 0
        elif result[count] == "_": # If letter is not in word
            compareString = guess[:count] # This line and next line accounts for duplicate letter edge case
            if letter in compareString:
                placement[count+1] = 0
            else:
                placement = [0, 0, 0, 0, 0, 0]
        placement[0] = 1
        stateSpace.update({letter : placement})
        count += 1
    return

def convertToRanking(wordList): # Convert generated list of words to dictionary so that rankings can also be included
    wordDict = {}
    for word in wordList:
        wordDict.update({word : 0})
    return wordDict

def playGame(wordGen):
    resetStateSpace()
    firstGuess = True
    # load the wordlist that we will select words from for the wordle game
    GAMEWORD_WORDLIST = create_wordlist(
        GAMEWORD_LIST_FNAME, length=WORDLEN)

    # select a random word to start with
    WORD = random.choice(GAMEWORD_WORDLIST)
    # WORD = "WHARF"
    # GAME_WORD_LENGTH = len(WORD)

    # keep track of some game state
    NUM_GUESSES = 0

    # A * character means a letter was guessed correctly
    # in the correct position.
    # A - character means a letter was guessed correctly,
    # but in the incorrect position.

    # start of the user name interaction
    # print("_ " * GAME_WORD_LENGTH)
    # we use a continuous loop, since there could be a number of different exit conditions from the game if we want to spruce it up.
    wordDict = convertToRanking(create_wordlist(GUESSWORD_LIST_FNAME, length=WORDLEN))
    try:
        while True:
            # get the user to guess something
            if firstGuess:
                firstGuess = False
                GUESS = INITGUESS
            else:
                wordDict, GUESS = wordGen(wordDict, NUM_GUESSES)
            NUM_GUESSES += 1
            # display the guess when compared against the game word
            result = compare(expected=WORD, guess=GUESS)
            updateStateSpace(GUESS.lower(), result)
            wordDict = updateRanking(wordDict)
            # print(" ".join(result))

            if WORD == GUESS:
                # print(f"You won! It took you {NUM_GUESSES} guesses.")
                break
    except KeyboardInterrupt:
        print(f"""
    You quit - the correct answer was {WORD.upper()}
    and you took {NUM_GUESSES} guesses
    """)
    return NUM_GUESSES

def updateRanking(wordDict): # Update ranking (0 if letter not in word, 1 if in word but in incorrect position, 2 if in word and correct position)
    global stateSpace
    for word in wordDict:
        ranking = 0
        position = 1
        for letter in word:
            letterState = stateSpace.get(letter.lower())
            ranking += letterState[position]
        position += 1
        wordDict.update({word : ranking})
    return wordDict

def isValid(word):
    global stateSpace
    position = 1
    for letter in word: # Iterate through each letter in the word, check if this is a possible word
        state = stateSpace.get(letter)
        if state[position] == 0:
            return False
        position += 1
    return True


def randomGuesser(wordDict, guessNum):
    global stateSpace
    wordList = list(wordDict.keys()) # Get list of keys (words)
    random.shuffle(wordList) # Shuffle list for random aspect of search
    for word in wordList:
        word = word.lower()
        if isValid(word): # Check if word is valid according to state space
            del wordDict[word.upper()]
            return wordDict, word.upper()
        else:
            del wordDict[word.upper()]            

def useLowestScore2and3Guess(wordDict, guessNum):      
    wordList = sorted(wordDict.items(), key=lambda x:x[1]) # Sort the dictionary (converts it to a list)
    if guessNum == 1 or guessNum == 2: # If the second or the third guess...
        for wordTuple in wordList:
            wordList.remove(wordTuple) # Remove this word from the list
            if isValid(wordTuple[0].lower()):
                return dict(wordList), wordTuple[0] # Cast the sorted list to a dictionary and also return the next guess
    else: 
        for wordTuple in reversed(wordList):
            wordList.remove(wordTuple)
            if isValid(wordTuple[0].lower()):
                return dict(wordList), wordTuple[0]

def useAverageScore2and3Guess(wordDict, guessNum):      
    wordList = sorted(wordDict.items(), key=lambda x:x[1]) # Sort the dictionary (converts it to a list)
    if guessNum == 1 or guessNum == 2: # If the second or the third guess...
        while True:
            word = wordList[int(len(wordList) / 2)][0] # Get the word with the lowest score
            wordList.pop(int(len(wordList) / 2)) # Remove this word from the list
            if isValid(word.lower()):
                return dict(wordList), word # Cast the sorted list to a dictionary and also return the next guess
    else: 
        for wordTuple in reversed(wordList):
            wordList.remove(wordTuple)
            if isValid(wordTuple[0].lower()):
                return dict(wordList), wordTuple[0]

def useWordsNotGuessed(wordDict, guessNum):
    global stateSpace
    wordList = list(wordDict.keys()) # Get list of keys (words)
    random.shuffle(wordList) # Shuffle list for random aspect of search
    if guessNum == 1 or guessNum == 2:
        for word in wordList:
            notGuessed = True
            for letter in word:
                state = stateSpace.get(letter.lower())
                if state[0] == 2:
                    notGuessed = False
                    break
            if notGuessed and isValid(word.lower()):
                del wordDict[word.upper()]
                return wordDict, word
    else:
        wordList = sorted(wordDict.items(), key=lambda x:x[1]) # Sort the dictionary (converts it to a list)
        for wordTuple in reversed(wordList):
            wordList.remove(wordTuple)
            if isValid(wordTuple[0].lower()):
                return dict(wordList), wordTuple[0]
        return


def runStrategy (strategy, strategyName, iterations):
    print("Running", strategyName, "Algorithm with", iterations, "game iterations. This may take a while...")
    tries = 0
    startTime = time.perf_counter()
    for x in range (iterations):
        tries += playGame(strategy)
    endTime = time.perf_counter()
    totalTime = endTime - startTime
    print("    Average Guesses for "+ str(strategyName) + ": " + str(tries / iterations))
    print("    Time taken for algorithm to run: " + str(totalTime) + " secs")
    print("    This means each game took, on average, " + str(totalTime / iterations) + " secs to run")

# runStrategy(randomGuesser, "RandomGuesser", 200)
# runStrategy(useLowestScore2and3Guess, "Lowest Score for 2nd & 3rd Guesses", 100)
# runStrategy(useAverageScore2and3Guess, "Average Score for 2nd & 3rd Guesses", 100)
# runStrategy(useWordsNotGuessed, "Guess Words with letters not in correct spot for 2nd & 3rd Guesses", 100)