import time
from game import *
import random

WORDLEN = 5 # The length of the correct answer and guessed words
INITGUESS = "TARES" # The first guess

stateSpace = {} # Global value to demonstrate the state space
letterFreq = {} # Global value to count letter frequencies

rankingType = 0

def resetStateSpace(): # Function to reset state space. Is run after every game play. Keys are letters, and
                            # values are a list where the first value is if the letter was previously guessed.
    global stateSpace
    stateSpace = {
    "a" : [0, 1, 1, 1, 1, 1], "b" : [0, 1, 1, 1, 1, 1], "c" : [0, 1, 1, 1, 1, 1], "d" : [0, 1, 1, 1, 1, 1], "e" : [0, 1, 1, 1, 1, 1], "f" : [0, 1, 1, 1, 1, 1], "g" : [0, 1, 1, 1, 1, 1], "h" : [0, 1, 1, 1, 1, 1],
    "i" : [0, 1, 1, 1, 1, 1], "j" : [0, 1, 1, 1, 1, 1], "k" : [0, 1, 1, 1, 1, 1], "l" : [0, 1, 1, 1, 1, 1], "m" : [0, 1, 1, 1, 1, 1], "n" : [0, 1, 1, 1, 1, 1], "o" : [0, 1, 1, 1, 1, 1], "p" : [0, 1, 1, 1, 1, 1],
    "q" : [0, 1, 1, 1, 1, 1], "r" : [0, 1, 1, 1, 1, 1], "s" : [0, 1, 1, 1, 1, 1], "t" : [0, 1, 1, 1, 1, 1], "u" : [0, 1, 1, 1, 1, 1], "v" : [0, 1, 1, 1, 1, 1], "w" : [0, 1, 1, 1, 1, 1], "x" : [0, 1, 1, 1, 1, 1],
    "y" : [0, 1, 1, 1, 1, 1], "z" : [0, 1, 1, 1, 1, 1]
}

def resetLetterFreq(): # Function to reset letter frequency count. Is run after every game play. Keys are letters, and
                            # frequency values are a list.
    global letterFreq
    letterFreq = {
    "a" : [0, 0, 0, 0, 0], "b" : [0, 0, 0, 0, 0], "c" : [0, 0, 0, 0, 0], "d" : [0, 0, 0, 0, 0], "e" : [0, 0, 0, 0, 0], "f" : [0, 0, 0, 0, 0], "g" : [0, 0, 0, 0, 0], "h" : [0, 0, 0, 0, 0],
    "i" : [0, 0, 0, 0, 0], "j" : [0, 0, 0, 0, 0], "k" : [0, 0, 0, 0, 0], "l" : [0, 0, 0, 0, 0], "m" : [0, 0, 0, 0, 0], "n" : [0, 0, 0, 0, 0], "o" : [0, 0, 0, 0, 0], "p" : [0, 0, 0, 0, 0],
    "q" : [0, 0, 0, 0, 0], "r" : [0, 0, 0, 0, 0], "s" : [0, 0, 0, 0, 0], "t" : [0, 0, 0, 0, 0], "u" : [0, 0, 0, 0, 0], "v" : [0, 0, 0, 0, 0], "w" : [0, 0, 0, 0, 0], "x" : [0, 0, 0, 0, 0],
    "y" : [0, 0, 0, 0, 0], "z" : [0, 0, 0, 0, 0]
}

def updateStateSpace(guess, result): # Update state space as a result of each guess.
    global stateSpace
    index = 0 # Stores index we are at in the result string
    for letter in guess:
        possibleLetterLoc = stateSpace.get(letter)
        if result[index] == '*': # If letter is in word and in correct position
            for value in stateSpace: # Loop through state space and update all values to 0
                if value != letter: # Makes sure that the value that we are looking at isn't changed to 0
                    holder = stateSpace.get(value)
                    holder[index+1] = 0
                    stateSpace.update({value : holder})
            possibleLetterLoc[index+1] = 2
        elif result[index] == '-': # If letter in word but not in correct position
            possibleLetterLoc[index+1] = 0
        elif result[index] == "_": # If letter is not in word
            compareString = guess[:index] # This line and next line accounts for duplicate letter edge case
            if letter in compareString:
                possibleLetterLoc[index+1] = 0
            else:
                possibleLetterLoc = [0, 0, 0, 0, 0, 0]
        possibleLetterLoc[0] = 1 # Set the first index in the possibleLetterLoc array to 1 to indicate this letter has been guessed
        stateSpace.update({letter : possibleLetterLoc})
        index += 1
    return

def createRankingDict(wordList): # Convert generated list of words to dictionary so that rankings can also be included
    wordDict = {}
    for word in wordList:
        wordDict.update({word : 0})
    return wordDict

def playGame(wordGen):
    resetStateSpace()
    firstGuess = True
    # load the wordlist that we will select words from for the wordle game
    GAMEWORD_WORDLIST = create_wordlist(GAMEWORD_LIST_FNAME, length=WORDLEN)

    # select a random word to be the Wordle!
    WORD = random.choice(GAMEWORD_WORDLIST)
    # WORD = "WHARF"
    # GAME_WORD_LENGTH = len(WORD)

    # keep track of some game state
    NUM_GUESSES = 0

    # A * character means a letter was guessed correctly in the correct position.
    # A - character means a letter was guessed correctly, but in the incorrect position.
    # A _ character means a letter was guessed incorrectly.

    # start of the user name interaction
    # print("_ " * GAME_WORD_LENGTH)
    # we use a continuous loop, since there could be a number of different exit conditions from the game if we want to spruce it up.
    wordDict = createRankingDict(create_wordlist(GUESSWORD_LIST_FNAME, length=WORDLEN))
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
            # print(f"Guess for step {NUM_GUESSES}: {GUESS}")
            updateStateSpace(GUESS.lower(), result)
            wordDict = updateRanking(wordDict)
            # print(" ".join(result))

            if WORD == GUESS:
                # print(f"You won! It took you {NUM_GUESSES} guesses. The word was {WORD.upper()}")
                break
    except KeyboardInterrupt:
        print(f"""
    You quit - the correct answer was {WORD.upper()}
    and you took {NUM_GUESSES} guesses
    """)
    return NUM_GUESSES

def updateRanking(wordDict): # Function to call the correct ranking function
    global rankingType
    wordDict = updateWordDict(wordDict)
    if (rankingType == 0):
        return wordDict
    if (rankingType == 1):
        return updateStateSpaceRanking(wordDict)
    if (rankingType == 2):
        return updateFrequencyRanking(wordDict)
    if (rankingType == 3):
        return updateEntropyRanking(wordDict)
    if (rankingType == 4):
        return updateStateSpaceAndEntropyRanking(wordDict)
    if (rankingType == 5):
        return wordDict

def updateWordDict(wordDict): # Delete words from the word dictionary with letters that are in invalid spots
    dict_copy = wordDict.copy()
    for word in dict_copy.keys():
        wordIndex = 1
        for letter in word:
            if stateSpace.get(letter.lower())[wordIndex] == 0:
                del wordDict[word]
                break
            wordIndex += 1
    return wordDict

def updateStateSpaceRanking(wordDict): # Update ranking (0 if letter not in word or not guessed yet, 1 if in word but in incorrect position, 2 if in word and correct position)
    global stateSpace
    for word in wordDict:
        ranking = 0
        position = 1
        for letter in word:
            dupStr = word.split(letter)
            if letter not in dupStr:
                letterState = stateSpace.get(letter.lower())
                if letterState[0] == 1:
                    ranking += letterState[position]
            position += 1
        wordDict.update({word : (ranking / 10)})
    return wordDict

def updateLetterFreq(wordDict):
    global letterFreq
    for word in wordDict: # Updates the letterFreq dictionary with updated frequency values
        position = 0
        for letter in word:
            letter = letter.lower()
            frequencyList = letterFreq.get(letter)
            dupStr = word.split(letter)
            if frequencyList != None and not (letter in dupStr):
                frequency = frequencyList[position] + 1
                frequencyList[position] = frequency
                letterFreq.update({letter : frequencyList})
            position += 1
    return

def updateFrequencyRanking(wordDict):
    global letterFreq
    resetLetterFreq()
    updateLetterFreq(wordDict)
    for word in wordDict:
        ranking = 0
        position = 0
        for letter in word:
            letter = letter.lower()
            frequencyList = letterFreq.get(letter)
            ranking += frequencyList[position]
        wordDict.update({word : ranking})
    return wordDict

def updateEntropyRanking(wordDict):
    global letterFreq # Use letterFreq dictionary for entropy too!
    resetLetterFreq()
    updateLetterFreq(wordDict)
    for letter in letterFreq:
        frequencyList = letterFreq.get(letter)
        frequencyList[:] = [x / (len(wordDict) + 1) for x in frequencyList]
    for word in wordDict:
        ranking = 0
        position = 0
        for letter in word:
            letter = letter.lower()
            frequencyList = letterFreq.get(letter)
            ranking += frequencyList[position] * (1 - frequencyList[position])
        wordDict.update({word : ranking})
    # print(letterFreq)
    return wordDict

def updateStateSpaceAndEntropyRanking(wordDict):
    wordDict2 = wordDict.copy()
    stateSpaceWordDict = updateStateSpaceRanking(wordDict)
    entropyWordDict = updateEntropyRanking(wordDict2)
    newDict = {}
    for word in stateSpaceWordDict:
        ranking1 = stateSpaceWordDict.get(word)
        ranking2 = entropyWordDict.get(word)
        if ranking2 != None:
            avgRanking = (ranking1 + ranking2) / 2
            newDict.update({word : avgRanking})
        else:
            newDict.update({word : ranking1})
    for word in entropyWordDict:
        if word not in stateSpaceWordDict:
            newDict.update({word : entropyWordDict.get(word)})
    return newDict

def isValid(word): # Check if word is valid (Wordle hard mode verification)
    global stateSpace
    position = 1
    for letter in word: # Iterate through each letter in the word, check if this is a possible word
        state = stateSpace.get(letter)
        if state[position] == 0:
            return False
        position += 1
    return True

def randomGuesser(wordDict, guessNum): # Guess random words that are valid based on previous guess info
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

def getHighestRanking(wordDict):
    wordList = sorted(wordDict.items(), key=lambda x:x[1]) # Sort the dictionary (converts it to a list)
    updatedWordList = wordList.copy()
    i = 0
    # for word in reversed(updatedWordList):
    #     if i == 10:
    #         break
    #     print(word)
    #     i += 1
    for wordTuple in reversed(wordList): # Get highest score words
        updatedWordList.remove(wordTuple)
        if isValid(wordTuple[0].lower()):
            return dict(updatedWordList), wordTuple[0]

def getAverageRanking(wordDict):
    wordList = sorted(wordDict.items(), key=lambda x:x[1]) # Sort the dictionary (converts it to a list)
    while True:
        word = wordList[int(len(wordList) / 2)][0] # Get the word with the average score
        wordList.pop(int(len(wordList) / 2)) # Remove this word from the list
        if isValid(word.lower()):
            return dict(wordList), word # Cast the sorted list to a dictionary and also return the next guess

def getLowestRanking(wordDict):
    wordList = sorted(wordDict.items(), key=lambda x:x[1]) # Sort the dictionary (converts it to a list)
    updatedWordList = wordList.copy()
    for wordTuple in wordList:
        updatedWordList.remove(wordTuple) # Remove this word from the list
        if isValid(wordTuple[0].lower()): # and not hasRepeatedLetters(wordTuple[0].lower()) and not lettersAlreadyGuessed(wordTuple[0].lower())
            return dict(updatedWordList), wordTuple[0] # Cast the sorted list to a dictionary and also return the next guess

def getWordWithNoGuessedLetters(wordDict): # Gets a word whose letters have not been guessed yet
    wordList = create_wordlist(GUESSWORD_LIST_FNAME, length=WORDLEN)
    for word in wordList:
        if not hasRepeatedLetters(word.lower()) and not lettersAlreadyGuessed(word.lower()):
            if word in wordDict:
                del wordDict[word]
            return wordDict, word

def hasRepeatedLetters(word): # Checks whether the inputted word has repeated letters
    visited = []
    for letter in word:
        if letter in visited:
            return True
        visited.append(letter)
    return False

def lettersAlreadyGuessed(word): # Checks if any of the letters in the inputted word have already been guessed
    global stateSpace
    for letter in word:
        if stateSpace.get(letter)[0] == 1:
            return True
    return False

def useNoKnownLettersForSecondGuess(wordDict, guessNum):
    if guessNum == 1: # If the second guess...
        return getWordWithNoGuessedLetters(wordDict)
    else: 
        return getHighestRanking(wordDict)

def useNoKnownLettersForSecondAndThirdGuess(wordDict, guessNum):
    if guessNum == 1 or guessNum == 2: # If the second or the third guess...
        return getWordWithNoGuessedLetters(wordDict)
    else:
        return getHighestRanking(wordDict)

def useLowestScore2Guess(wordDict, guessNum):  
    if guessNum == 1: # If the second guess...
        return getLowestRanking(wordDict)
    else: 
        return getHighestRanking(wordDict)

def useLowestScore2and3Guess(wordDict, guessNum):  
    if guessNum == 1 or guessNum == 2: # If the second or the third guess...
        return getLowestRanking(wordDict)
    else: 
        return getHighestRanking(wordDict)

def useAverageScore2and3Guess(wordDict, guessNum):      
    if guessNum == 1 or guessNum == 2: # If the second or the third guess...
        return getAverageRanking(wordDict)
    else: 
        return getHighestRanking(wordDict)

def useLettersInIncorrectSpots(wordDict, guessNum):
    global stateSpace
    wordList = list(wordDict.keys()) # Get list of keys (words)
    random.shuffle(wordList) # Shuffle list for random aspect of search
    if guessNum == 1 or guessNum == 2:
        for word in wordList:
            notGuessed = True
            for letter in word:
                state = stateSpace.get(letter.lower())
                if state[0] == 2: # Check for letters in the correct spots
                    notGuessed = False
                    break
            if notGuessed and isValid(word.lower()):
                del wordDict[word.upper()]
                return wordDict, word
    else:
        return getHighestRanking(wordDict)

def useAverageFrequencyToGuess(wordDict, guessNum):
    return getAverageRanking(wordDict)

def useAverageEntropyToGuess(wordDict, guessNum):
    return getAverageRanking(wordDict)

def useHybridEntropyAndStateSpaceRanking(wordDict, guessNum):
    return getHighestRanking(wordDict)

def useHybridEntropyAndNoKnownLettersForSecond(wordDict, guessNum):
    if guessNum == 1:
        return getWordWithNoGuessedLetters(wordDict)
    else:
        return getHighestRanking(wordDict)


def useHighestNumPruned(wordDict, guessNum):
    word = ""
    return wordDict, word


def runStrategy (strategy, strategyName, iterations):
    global rankingType
    if strategy == randomGuesser:
        rankingType = 0
    if strategy == useNoKnownLettersForSecondGuess or strategy == useNoKnownLettersForSecondAndThirdGuess or strategy == useLowestScore2and3Guess or strategy == useAverageScore2and3Guess or strategy == useLettersInIncorrectSpots:
        rankingType = 1
    elif strategy == useAverageFrequencyToGuess:
        rankingType = 2
    elif strategy == useAverageEntropyToGuess:
        rankingType = 3
    elif strategy == useHybridEntropyAndStateSpaceRanking or strategy == useHybridEntropyAndNoKnownLettersForSecond:
        rankingType = 4
    elif strategy == useHighestNumPruned:
        rankingType = 5
    print("Running", strategyName, "Algorithm with", iterations, "game iterations. This may take a while...")
    tries = 0
    startTime = time.perf_counter()
    underOrEqualTo6 = 0
    over6 = 0
    for x in range (iterations):
        guesses = playGame(strategy)
        tries += guesses
        if guesses <= 6:
            underOrEqualTo6 += 1
        else:
            over6 += 1
    endTime = time.perf_counter()
    totalTime = endTime - startTime
    print("    Average Guesses for "+ str(strategyName) + ": " + str(tries / iterations))
    print("    Number of Games with guess count under or equal to 6: "+ str(underOrEqualTo6) + ". With guess count over 6: " + str(over6))
    print("    " + str(strategyName) + " won the game " + str(underOrEqualTo6 / iterations * 100) + "% of the time!")
    print("    Time taken for algorithm to run: " + str(totalTime) + " secs")
    print("    This means each game took, on average, " + str(totalTime / iterations) + " secs to run")

def main():
    # runStrategy(randomGuesser, "RandomGuesser", 100)
    # runStrategy(useNoKnownLettersForSecondGuess, "Word with No Guessed Letters for 2nd Guess", 500)
    # runStrategy(useNoKnownLettersForSecondAndThirdGuess, "Word with No Guessed Letters for 2nd & 3rd Guess", 500)
    # runStrategy(useLowestScore2Guess, "Lowest Score for 2nd Guess", 500)
    # runStrategy(useLowestScore2and3Guess, "Lowest Score for 2nd & 3rd Guesses", 500)
    # runStrategy(useAverageScore2and3Guess, "Average Score for 2nd & 3rd Guesses", 500)
    # runStrategy(useLettersInIncorrectSpots, "Guess Words with letters not in correct spot for 2nd & 3rd Guesses", 500)
    # runStrategy(useAverageFrequencyToGuess, "AverageFrequencyGuesser", 500)
    # runStrategy(useAverageEntropyToGuess, "AverageEntropyGuesser", 500)
    # runStrategy(useHybridEntropyAndStateSpaceRanking, "HybridEntropyAndStateSpaceGuesser", 500)
    # runStrategy(useHybridEntropyAndNoKnownLettersForSecond, "Hybrid Entropy And State Space And No Known Letters For Second Guess", 500)
    runStrategy(useHighestNumPruned, "Guess Words that Prune the Most Other Words", 50)

if __name__ == '__main__':
    main()