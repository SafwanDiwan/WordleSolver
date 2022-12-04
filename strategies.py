from game import *

stateSpace = {
    "a" : [0, 1, 1, 1, 1, 1], "b" : [0, 1, 1, 1, 1, 1], "c" : [0, 1, 1, 1, 1, 1], "d" : [0, 1, 1, 1, 1, 1], "e" : [0, 1, 1, 1, 1, 1], "f" : [0, 1, 1, 1, 1, 1], "g" : [0, 1, 1, 1, 1, 1], "h" : [0, 1, 1, 1, 1, 1],
    "i" : [0, 1, 1, 1, 1, 1], "j" : [0, 1, 1, 1, 1, 1], "k" : [0, 1, 1, 1, 1, 1], "l" : [0, 1, 1, 1, 1, 1], "m" : [0, 1, 1, 1, 1, 1], "n" : [0, 1, 1, 1, 1, 1], "o" : [0, 1, 1, 1, 1, 1], "p" : [0, 1, 1, 1, 1, 1],
    "q" : [0, 1, 1, 1, 1, 1], "r" : [0, 1, 1, 1, 1, 1], "s" : [0, 1, 1, 1, 1, 1], "t" : [0, 1, 1, 1, 1, 1], "u" : [0, 1, 1, 1, 1, 1], "v" : [0, 1, 1, 1, 1, 1], "w" : [0, 1, 1, 1, 1, 1], "x" : [0, 1, 1, 1, 1, 1],
    "y" : [0, 1, 1, 1, 1, 1], "z" : [0, 1, 1, 1, 1, 1]
}

def updateStateSpace(guess, result):
    global stateSpace
    count = 0
    for letter in guess:
        placement = stateSpace.get(letter)
        if result[count] == '*':
            for value in stateSpace: # Loop through state space and update all values to 0
                holder = stateSpace.get(value)
                holder[count+1] = 0
                stateSpace.update({value : holder})
            placement = [0, 1, 1, 1, 1, 1]
            placement[count+1] = 2
        elif result[count] == '-':
            placement[count+1] = 0
        elif result[count] == "_":
            placement = [0, 0, 0, 0, 0, 0]
        placement[0] = 1
        stateSpace.update({letter : placement})
        count += 1
        print(letter, stateSpace.get(letter))
    return


def randomGuesser():
    
    return
# playGame()
updateStateSpace("apale", ['*', '_', '_', '-', '_'])
print()
updateStateSpace("ampel", ['*', '_', '_', '_', '-'])