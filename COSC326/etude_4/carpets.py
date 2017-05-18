'''
 Etude 4: Carpets
 File name: carpets.py
 Authors:   Jono Sue 4097307, Lorne Brooks 1914321,
            Ben Callander 7814204 Stefan Pedersen 1427681
 Date created: 15/01/2017
 Date last modified: 03/02/2017
 Python version: 2.7
 '''
import getopt, sys, re, time, itertools
option = ""
strips, indexes, combinations = [], [], []
useStrips = 0
matches = 0
matchesNon = 0
baseline = 0
startIndex = 0
maxMatches = 0
maxCarpet = []
balancedMatches = 1000 #arbitrary minimum deviation for balanced match
balancedCarpet = []

def usage():
    print '\nTakes one flag (-n, -m, or -b), an integer representing the'
    print 'number of strips to be used, and an <input file>:'
    print '-n (no matches wanted)'
    print '-m (as many matches as possible)'
    print '-b (a balance between match/no match)'
    print 'Example: python carpets -n 15 < input.file'

# change getopt to argparse
def setOptions(argv):
    global useStrips, option
    try:
        opts, args = getopt.getopt(argv, 'nmb:', ['file='])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit()
    for o, arg in opts:
        if o in ('-n'):
            #print "No matches wanted"
            option = 'n'
        elif o in ('-m'):
            #print "Create as many matches as possible"
            option = 'm'
        elif o in ('-b'):
            #print "Create the best balance of match/no match"
            option = 'b'
    useStrips = int(sys.argv[2])

'''
The tree
'''
class Node:
    def __init__(self, key):
        self.key = key
        self.children = []

    def fill_tree(self, indexes):
        if len(indexes) == 0:
            return
        for i in indexes:
            self.children.append(Node(i))
            temp = indexes[:]
            temp.remove(i)
            z = indexes.index(i)
            self.children[z].fill_tree(temp)

    # matchFound + testNoMatches work in conjunction to find no matches
    # @return: 0 normal, 1 flip, 2 don't include
    def matchFound(self, stripAIndex, stripBIndex):
        stripA = strips[stripAIndex]
        stripB = strips[stripBIndex]
        # check flip first
        matches = 0
        for i in range(len(stripA)):
            if stripA[i] == stripB[len(stripA)-i-1]:
                matches += 1
        if matches == 0:
            return [stripAIndex, 1]
        # check non-flipped
        matches = 0
        for i in range(len(stripA)):
            if stripA[i] == stripB[i]:
                matches += 1
        if matches == 0:
            return [stripAIndex, 0]
        return [stripAIndex, 2]

    def testNoMatches(self):
        if self.children == []:
            return [self.key, 0]
        for child in self.children:
            results = []
            if self.key != None:
                results = self.matchFound(self.key, child.key)
            results.extend(child.testNoMatches())
            return results

    # findMatches creates complete carpets and sends them to the testMatches
    # function to determine how many matches/nonMatches occur
    def findMatches(self, completeCarpet, sorted):
        if self.key != None:
            trueMax = 0
            completeCarpet.append(sorted[self.key])
        if self.children == []:
            if len(completeCarpet) == useStrips:
                testMatches(completeCarpet)
            return
        for child in self.children:
            child.findMatches(completeCarpet, sorted)
            completeCarpet = []
            if self.key != None:
                completeCarpet = [sorted[self.key]]

    # findBalanced creates complete carpets and sends them to the testBalanced
    # function to determine whether balanced carpet can be found. This is
    # repeated code, and there must be a way to send the result on to a
    # specific function based on which function called it to avoid This
    # repetition
    def findBalanced(self, completeCarpet, sorted):
        if self.key != None:
            trueMax = 0
            completeCarpet.append(sorted[self.key])
        if self.children == []:
            if len(completeCarpet) == useStrips:
                testBalance(completeCarpet)
            return
        for child in self.children:
            child.findBalanced(completeCarpet, sorted)
            completeCarpet = []
            if self.key != None:
                completeCarpet = [sorted[self.key]]

'''
Functions for noMatch
'''
def noMatch():
    indexes = range(len(strips))
    combinations = itertools.combinations(indexes, int(useStrips))
    treeCounter = 0
    for i in combinations:
        treeCounter+=1
        c = list(i)
        tree = Node(None)
        tree.fill_tree(c)
        results = tree.testNoMatches()
        #print results
        orientationFlags = results[1::2]
        if 2 in orientationFlags:
            continue
        if len(results) == int(useStrips) * 2:
            # Flip correction: every strip behind a flipped strip is flipped
            # so that the orientation is preserved
            for o in range(1, len(results), 2):
                if results[o] == 1:
                    x = o - 2
                    while(x > 0):
                        if results[x] == 0:
                            results[x] = 1
                        else:
                            results[x] = 0
                        x -= 2
            #print 'corrected results:', results
            for i in range(0, len(results), 2):
                strip = results[i]
                if results[i+1] == 0:
                    print strips[strip]
                else:
                    print strips[strip][::-1]
            # returns the first no match
            #print "Trees explored:", treeCounter
            break
'''
Functions for maxMatch
'''
def maxMatch():
    sorted = selectWorkingCarpet()
    # print sorted
    #print "Baseline (minimum matches to accept)", baseline, "\n"
    indexes = range(len(strips))
    combinations = itertools.combinations(indexes, int(useStrips))
    treeCounter = 0
    for i in combinations:
        treeCounter+=1
        c = list(i)
        tree = Node(None)
        tree.fill_tree(c)
        tree.findMatches([], sorted)
    for i in range(len(maxCarpet)):
        print maxCarpet[i]

    print "Max Matches:", maxMatches
    #print "Trees explored: ", treeCounter
    # print startIndex
    # print useStrips
    # print option

# From the entire carpet_stock, select the initial set of carpet strips
# to test for candidacy. We are trying to reach the greatest number
# of matches as early as possible in order to raise the baseline (and thereby
# prune our search tree). If the carpet size selection is less than
# that of carpet_stock, iterate over blocks of carpet strips in that size
# checking for the group which has the greatest number of matches. This is
# simply an in place search with no permutations.
# @return sorted carpet strips (initial set to be guided by startIndex)

def selectWorkingCarpet():
    global strips
    global baseline
    global startIndex
    workingCarpet = []
    tryCarpet = []
    bestMatch = 0
    startIndex = 0
    if useStrips <= len(strips):
        sorted = sortStrips(strips)
        # print sorted
        for i in range(len(strips)):
            for j in range(useStrips):
                tryCarpet.append(sorted[i])
                i = (i+1) % len(strips)
            # print tryCarpet
            matches = verticalMatch(tryCarpet)
            if matches > bestMatch:
                bestMatch = matches
                workingCarpet = tryCarpet
                startIndex = sorted.index(workingCarpet[0])
            tryCarpet = []
        # print "\nCarpet strips sorted: ", sorted
    else:
        print "You do not have enough strips for your chosen carpet"
        exit()
    baseline = bestMatch
    # print "Start index for iterations on sorted list", startIndex
    return sorted

# Insertion sort to sort carpet strips in carpet_stock into order of
# match frequency (re: horizontalMatch).
# @return sorted list of entire carpet stock.
def sortStrips(strips):
    stripsSorted = []
    for i in range (1, len(strips)):
        tmp = horizontalMatch(strips[i])
        tmpStr = strips[i]
        k = i
        while k > 0 and tmp < horizontalMatch(strips[i-1]):
            strips[k] = strips[k-1]
            k = k - 1
        strips[k] = tmpStr
    stripsSorted = strips[::-1]
    # print stripsSorted
    return stripsSorted

# Horizontal matches function to return the total number of matches found in an
# individual strip. This was more valuable when the brief assumed that
# horizontal matches counted to the total, but should still provide some
# efficiency boost by increasing the chance of a match overlap between two
# strips early on in the DFS of the tree.
# @return number of matches to the sortStrips() function

def horizontalMatch(strip):
    matches = 0
    for patch in range(len(strip)-1):
        if strip[patch] == strip[patch+1]:
            matches += 1
    return matches

# Vertical matches function to return total number of (vertical) matches in
# given carpet or sub-carpet.
def verticalMatch(carpet):
    matches = 0
    for i in range(len(carpet)-1):
        stripA = carpet[i]
        stripB = carpet[i+1]
        for patch in range(len(stripA)):
            if stripA[patch] == stripB[patch]:
                matches += 1
    return matches

# testMatches checks each combination of a full carpet for matches/nonMatches
# and stores the best value in globals: maxMatches, maxCarpet, balancedMatches,
# balancedCarpet
def testMatches(completeCarpet):
    global maxMatches, maxCarpet
    matches = 0
    revMatches = 0
    workingTotal = 0
    for i in range(len(completeCarpet)-1):
        stripA = completeCarpet[i]
        stripB = completeCarpet[i+1]
        for patch in range(len(stripA)):
            if stripA[patch] == stripB[patch]:
                matches += 1

            if stripA[patch] == stripB[len(stripA)-patch-1]:
                revMatches += 1
                
        if revMatches > matches:
            workingTotal += revMatches
            x = i
            while(x >= 0):
                completeCarpet[x] = completeCarpet[x][::-1]
                x -= 1
        else:
            workingTotal += matches

        matches  = revMatches  = 0
            
    if workingTotal > maxMatches:
        maxMatches = workingTotal
        maxCarpet = completeCarpet
    # print completeCarpet

'''
Functions for balancedMatch
'''
def balancedMatch():
    sorted = selectWorkingCarpet()
    # print sorted
    indexes = range(len(strips))
    combinations = itertools.combinations(indexes, int(useStrips))
    treeCounter = 0
    for i in combinations:
        treeCounter+=1
        c = list(i)
        tree = Node(None)
        tree.fill_tree(c)
        tree.findBalanced([], sorted)
    
    for i in range(len(balancedCarpet)):
        print balancedCarpet[i]
    #print "Trees explored: ", treeCounter
    print "Balance:", balancedMatches

# testMatches checks each combination of a full carpet for matches/nonMatches
# and stores the best value in globals: maxMatches, maxCarpet, balancedMatches,
# balancedCarpet
def testBalance(completeCarpet):
    global balancedMatches, balancedCarpet
    matches = 0
    nonMatches = 0
    revMatches = 0
    revNonMatches = 0
    workingTotal = 0

    for i in range(len(completeCarpet)-1):
        stripA = completeCarpet[i]
        stripB = completeCarpet[i+1]
        for patch in range(len(stripA)):
            if stripA[patch] == stripB[patch]:
                matches += 1
            else:
                nonMatches += 1
                
            if stripA[patch] == stripB[len(stripA)-patch-1]:
                revMatches += 1
            else:
                revNonMatches += 1

        if abs(revMatches - revNonMatches) < abs(matches - nonMatches):
            workingTotal += revMatches - revNonMatches
            x = i
            while(x >= 0):
                completeCarpet[x] = completeCarpet[x][::-1]
                x -= 1
        else:
            workingTotal += matches - nonMatches

        matches = nonMatches = revMatches = revNonMatches = 0

    if abs(workingTotal) < balancedMatches:
        balancedMatches = abs(workingTotal)
        balancedCarpet = completeCarpet
    if balancedMatches == 0:
        for i in range(len(balancedCarpet)):
            print balancedCarpet[i]
        print "Balance:", balancedMatches
        exit()

'''
Main
'''
def main():
    #start = time.time()
    setOptions(sys.argv[1:])
    for line in sys.stdin:
        strips.append(line.strip())
    if option == "n":
        noMatch()
    if option == "m":
        maxMatch()
    if option == "b":
        balancedMatch()
    #end = time.time()
    #print end-start

if __name__ == '__main__':
    main()
