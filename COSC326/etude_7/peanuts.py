'''
 Etude 7: Peanuts and pretzels
 File name: peanuts.py
 Authors:   Jono Sue 4097307, Lorne Brooks 1914321,
            Ben Callander 7814204 Stefan Pedersen 1427681
 Date created: 13/02/2017
 Date last modified: 16/02/2017
 Python version: 2.7
 '''
import fileinput, time

#Find legal moves from the rules given
def findLegalMoves(peanuts, pretzels, rules):
    pp = [peanuts, pretzels]
    legalMoves = [[0,1], [1,0]]
    for rule in rules:
        options = []
        for spec in range(len(rule)):
            options.append(list())
            operator = rule[spec][0]
            num = int(rule[spec][1:])
            if operator == '=':
                options[spec].append(num)
            if operator == '<':
                for i in range(0, num):
                    options[spec].append(i)
            if operator == '>':
                for i in range(num+1, pp[spec]+1):
                    options[spec].append(i)
        moves = []
        for numPeanuts in options[0]:
            for numPretzels in options[1]:
                move = [numPeanuts, numPretzels]
                moves.append(move)
        # Don't add repeats
        for m in moves:
            if m == [0, 0]:
                continue
            elif m not in legalMoves:
                legalMoves.append(m)
    return legalMoves

#Function governing player 1's behaviour
#Dictionary used to record visited states (memoisation)
def protagonist(legalMoves, peanuts, pretzels):
    if (peanuts, pretzels) in stateDictionaryA:
        return True
    else:
        stateDictionaryA[(peanuts, pretzels)] = 0
    for move in legalMoves:
        if move[0] > peanuts or move[1] > pretzels:
            continue
        if peanuts - move[0] == 0 and pretzels - move[1] == 0:
            return True
        elif enemy(legalMoves, peanuts-move[0], pretzels-move[1]) == True:
            return True
    return False

#Function governing player 2's behaviour
#Dictionary used to record visited states (memoisation)
def enemy(legalMoves, peanuts, pretzels):
    if (peanuts, pretzels) in stateDictionaryB:
        return False
    else:
        stateDictionaryB[(peanuts, pretzels)] = 0
    for move in legalMoves:
        if move[0] > peanuts or move[1] > pretzels:
            continue
        if peanuts - move[0] == 0 and pretzels - move[1] == 0:
            return False
        elif protagonist(legalMoves, peanuts-move[0], pretzels-move[1]):
            return False
    return True

#initiates snack taking functions by calling the protagonist()
def takeSnack(legalMoves, pnts, pretz, depth, moveList):
    for move in legalMoves:
        if move[0] > pnts or move[1] > pretz:
            continue
        if not protagonist(legalMoves, pnts-move[0], pretz-move[1]):
            print move[0], move[1]
            return True
    return False

# Main - handles input and initiates game#
peanuts = 0
pretzels = 0
rules = []
first = True
for line in fileinput.input():
    stateDictionaryA = {}
    stateDictionaryB = {}
    if line == '\n':
        # start program then continue
        legalMoves = findLegalMoves(peanuts, pretzels, rules)
        if [1,0] not in legalMoves:
            legalMoves.append([1,0])
        if [0,1] not in legalMoves:
            legalMoves.append([0,1])
        legalMoves = sorted(legalMoves, key=sum, reverse=True)

        # Initiates the game
        if not takeSnack(legalMoves, peanuts, pretzels, 0, []):
            print '0 0'
        peanuts = pretzels = 0
        rules = []
        first = True
        continue
    if first:
        first = False
        peanuts = int(line.split()[0])
        pretzels = int(line.split()[1])
        continue
    rules.append(line.split())
else:
    legalMoves = findLegalMoves(peanuts, pretzels, rules)
    if [1,0] not in legalMoves:
        legalMoves.append([1,0])
    if [0,1] not in legalMoves:
        legalMoves.append([0,1])
    legalMoves = sorted(legalMoves, key=sum, reverse=True)
    if not takeSnack(legalMoves, peanuts, pretzels, 0, []):
        print '0 0'
