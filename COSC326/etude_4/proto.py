'''
 Etude 3: Arithmetic
 File name: arithmetic.py
 Authors:   Jono Sue 4097307, Lorne $$$$$$ #######,
            Ben $$$$$$ ####### Stefan Pedersen 1427681
 Date created: 15/01/2017
 Date last modified: 15/01/2017
 Python version: 2.7
 '''
import fileinput, getopt, sys, re, math, time, itertools
option = ""
strips, indexes, combinations = [], [], []
useStrips = 0

def usage():
    print '\nTakes one flag (-n, -m, or -b), an integer, and an <input file>, '
    print 'representing the number of strips to be used'
    print '-n (no matches wanted)'
    print '-m (as many matches as possible)'
    print '-b (a balance between match/no match)'
    print 'Example: python make_carpet -n 15 <inputfile> '

def main(argv):
    global useStrips, option
    try:
        opts, args = getopt.getopt(argv, 'nmb:', ['file='])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit()

    for o, arg in opts:
        if o in ('-n'):
            print "No matches wanted"
            option = 'n'
        elif o in ('-m'):
            print "Create as many matches as possible"
            option = 'm'
        elif o in ('-b'):
            print "Create the best balance of match/no match"
            option = 'b'
    useStrips = sys.argv[2]

def findCombinationsToTest(indexes, useStrips):

    generator = itertools.permutations(indexes, int(useStrips))
    for i in generator:
        p = list(i)
        seen = False
        for c in combinations:
            # c[:] copies the array so the copy can be reversed + compared
            # to eliminate entire carpet possibilities that have been
            # flipped
            rev = c[:]
            rev.reverse()
            if p == rev:
                seen = True
        if seen == False:
            combinations.append(p)
    return combinations

def matchMaker(permutation):
    matches = 0
    nonMatches = 0
    results = {}

    ''' horizontal checks '''
    for strip in permutation:
        for patch in range(len(strip)-1):
            if strip[patch] == strip[patch+1]:
                matches += 1
            else:
                nonMatches += 1
    ''' vertical checks '''
    for i in range(len(permutation)-1):
        stripA = permutation[i]
        stripB = permutation[i+1]
        for patch in range(len(stripA)):
            if stripA[patch] == stripB[patch]:
                matches += 1
            else:
                nonMatches += 1

    return [matches, nonMatches]

# Takes a list of indexes for the strips of carpet to use
def findPermutations(carpet):
    numPermuationsOfCarpet = pow(2, len(carpet)-1)
    carpetStrips = []
    permutations = []
    matches = 0
    # Initialise the possible carpet with the actual strips
    for i in carpet:
        carpetStrips.append(strips[i])

    # Run through every permutation
    for i in range(numPermuationsOfCarpet):

        # Each item in permutation is a list of two things: the permutation
        # and the match:nonMatch ratio
        permutations.append(list())
        permutations[i].append(list())
        for x in range(len(carpet)):
            if i % pow(2, len(carpet)-x) < pow(2, len(carpet)-x-1):
                # Don't flip
                permutations[i][0].append(carpetStrips[x])
            else:
                # Flip
                temp = carpetStrips[x]
                temp = temp[::-1]
                permutations[i][0].append(temp)

        # Find the number of matches:NonMatches for this permutation
        permutations[i].append(matchMaker(permutations[i][0]))
    return permutations

def noMatches(candidates):
    found = False
    for candidate in candidates:
        if candidate[matchesNonMatchesIndex][0] == 0:
            found = True

            for i in candidate[stripsIndex]:
                print i

            return
    if found == False:
        print '>>No candidate without any matches exists'

def mostMatches(candidates):
    mostMatches = 0
    target = []
    for candidate in candidates:
        if candidate[matchesNonMatchesIndex][0] > mostMatches:
            mostMatches = candidate[matchesNonMatchesIndex][0]
            target = candidate[stripsIndex]

    if target == []:
        target = candidates[0][0]
        print 'No matches so default carpet'
        for i in target:
            print i

        print 'matches:', candidate[matchesNonMatchesIndex][0], \
            'non-matches:', candidate[matchesNonMatchesIndex][1]
    else:
        for i in target:
            print i

        print 'matches:', mostMatches

def bestBalance(candidates):
    # Assumes atleast 1 candidate so can get total possible matches
    difference = candidates[0][matchesNonMatchesIndex][0] + \
                 candidates[0][matchesNonMatchesIndex][1]
    target = []

    matches = 0
    nonMatches = 0

    for candidate in candidates:
        matches = candidate[matchesNonMatchesIndex][0]
        nonMatches = candidate[matchesNonMatchesIndex][1]

        if  matches > nonMatches:
            if matches - nonMatches < difference:
                difference = matches - nonMatches
                target = candidate[stripsIndex]
        else:
            if nonMatches - matches < difference:
                difference = nonMatches - matches
                target = candidate[stripsIndex]

        # Without the return, every following candidate will be
        # considered equally balanced due to difference == 0
        if difference == 0:
            for i in target:
                print i
            print 'matches:', matches, 'non-matches:', nonMatches
            return

    for i in target:
        print i

    print 'matches:', matches, 'non-matches:', nonMatches


main(sys.argv[1:])

##### Main Program #####

candidates = []

with open(sys.argv[3], 'r') as carpet_stock:
    for line in carpet_stock:
        strips.append(line.strip())
start = time.time()
indexes = range(len(strips))

print strips
print indexes
print useStrips

combinations = findCombinationsToTest(indexes, useStrips)

count = 1
for carpet in combinations:
    # Load each permutation for this combination + their match:nonMatches
    # into the candidates
    for i in findPermutations(carpet):
        candidates.append(i)
    count += 1

## Flag handling ##
stripsIndex = 0
matchesNonMatchesIndex = 1

# print candidates

if option == 'n':
    noMatches(candidates)
elif option == 'm':
    mostMatches(candidates)
else:
    bestBalance(candidates)

end = time.time()
print end-start
