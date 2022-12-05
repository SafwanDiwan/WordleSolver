import time
from game import *
import random

# the game word is 5 letters
WORDLEN = 5
INITGUESS = "TARES"

stateSpace = {}

def resetStateSpace():
    global stateSpace
    stateSpace = {
    "a" : [0, 1, 1, 1, 1, 1], "b" : [0, 1, 1, 1, 1, 1], "c" : [0, 1, 1, 1, 1, 1], "d" : [0, 1, 1, 1, 1, 1], "e" : [0, 1, 1, 1, 1, 1], "f" : [0, 1, 1, 1, 1, 1], "g" : [0, 1, 1, 1, 1, 1], "h" : [0, 1, 1, 1, 1, 1],
    "i" : [0, 1, 1, 1, 1, 1], "j" : [0, 1, 1, 1, 1, 1], "k" : [0, 1, 1, 1, 1, 1], "l" : [0, 1, 1, 1, 1, 1], "m" : [0, 1, 1, 1, 1, 1], "n" : [0, 1, 1, 1, 1, 1], "o" : [0, 1, 1, 1, 1, 1], "p" : [0, 1, 1, 1, 1, 1],
    "q" : [0, 1, 1, 1, 1, 1], "r" : [0, 1, 1, 1, 1, 1], "s" : [0, 1, 1, 1, 1, 1], "t" : [0, 1, 1, 1, 1, 1], "u" : [0, 1, 1, 1, 1, 1], "v" : [0, 1, 1, 1, 1, 1], "w" : [0, 1, 1, 1, 1, 1], "x" : [0, 1, 1, 1, 1, 1],
    "y" : [0, 1, 1, 1, 1, 1], "z" : [0, 1, 1, 1, 1, 1]
}

def updateStateSpace(guess, result):
    global stateSpace
    # print(guess, result)
    count = 0
    for letter in guess:
        placement = stateSpace.get(letter)
        if result[count] == '*':
            for value in stateSpace: # Loop through state space and update all values to 0
                if value != letter:
                    holder = stateSpace.get(value)
                    holder[count+1] = 0
                    stateSpace.update({value : holder})
            placement[count+1] = 2
        elif result[count] == '-':
            placement[count+1] = 0
        elif result[count] == "_":
            compareString = guess[:count]
            if letter in compareString:
                placement[count+1] = 0
            else:
                placement = [0, 0, 0, 0, 0, 0]
        placement[0] = 1
        stateSpace.update({letter : placement})
        count += 1
    return

def playGame(wordGen):
    resetStateSpace()
    firstGuess = True
    # load the wordlist that we will select words from for the wordle game
    GAMEWORD_WORDLIST = create_wordlist(
        GAMEWORD_LIST_FNAME, length=WORDLEN)

    # select a random word to start with
    WORD = random.choice(GAMEWORD_WORDLIST)
    # WORD = "WHARF"
    GAME_WORD_LENGTH = len(WORD)

    # keep track of some game state
    NUM_GUESSES = 0

    # A * character means a letter was guessed correctly
    # in the correct position.
    # A - character means a letter was guessed correctly,
    # but in the incorrect position.

    # start of the user name interaction
    # print("_ " * GAME_WORD_LENGTH)
    # we use a continuous loop, since there could be a number of different exit conditions from the game if we want to spruce it up.
    wordList = create_wordlist(GUESSWORD_LIST_FNAME, length=WORDLEN)
    try:
        while True:
            # get the user to guess something
            if firstGuess:
                firstGuess = False
                GUESS = INITGUESS
            else:
                updatedWordList, GUESS = wordGen(wordList)
                wordList = updatedWordList
            NUM_GUESSES += 1

            # display the guess when compared against the game word
            result = compare(expected=WORD, guess=GUESS)
            updateStateSpace(GUESS.lower(), result)
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

def randomGuesserIsValid(word):
    global stateSpace
    position = 1
    for letter in word:
        state = stateSpace.get(letter)
        # print(word, letter, state)
        if state[position] == 0:
            return False
        position += 1
    return True


def randomGuesser(wordList):
    global stateSpace
    random.shuffle(wordList)
    updatedWordList = wordList.copy()
    count = 0
    for word in wordList:
        word = word.lower()
        if randomGuesserIsValid(word):
            updatedWordList.remove(word.upper())
            return updatedWordList, word.upper()
        else:
            updatedWordList.remove(word.upper())            
        count += 1


# guesser = randomGuesser
iterations = 1000
print("Running RandomGuesser Algorithm with", iterations, "game iterations. This may take a while...")
tries = 0
startTime = time.perf_counter()
for x in range (iterations):
    tries += playGame(randomGuesser)
endTime = time.perf_counter()
totalTime = endTime - startTime
print("    Average Guesses for RandomGuesser:", (tries / iterations))
print("    Time taken for algorithm to run:", totalTime, "secs")
print("    This means each game took, on average,", totalTime / iterations, "secs to run")
# resetStateSpace()
# updateStateSpace("apale", ['*', '_', '_', '-', '_'])
# print()
# updateStateSpace("ampel", ['*', '_', '_', '_', '-'])
# randomGuesser()