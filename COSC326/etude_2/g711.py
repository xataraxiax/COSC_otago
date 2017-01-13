'''
 Etude 2: 7-11
 File name: g711.py
 Author: Stefan Pedersen 1427681
 Date created: 11/01/2017
 Date last modified: 12/01/2017
 Python version: 2.7

 Program for finding four numbers where a <= b <= c <= d && a+b+c+d == abcd,
 and then determining those which present a unique solution.
 Main algorithm inspired by a program written in C at
 http://everything2.com/title/The+7-Eleven+problem (user: efnar, Dec 06/2010)
'''
# import time
# start_time = time.time()

TARGET = 0
solutions = 0
a, b, c, d = 0,0,0,0

# Function to return numbers in monetary format without using floating points.
def asMoney(m):
    return("$%d" % (m/100))+(".%02d" % (m%100))

# Main loop iterates through range, taking the divisors for each successive
# target and calculating whether they meet the requirement of a+b+c+d == abcd
for i in range(100, 1000):
    TARGET = i
    aInd, bInd, cInd = 0, 0, 0,
    counter = 0
    divisors = []
    unique = []

    # Loop to generate list of divisors for the current target. To avoid
    # serious problems involved with floating-point division, we express
    # the ammounts of money in cents. The TARGET here is therefore multiplied
    # by 1000000.
    for x in xrange(1,TARGET):
        if (TARGET*1000000) % x == 0:
            divisors.append(x)

    # Nested for-loop permeates through the divisors. If the TARGET is found
    # the total and the four components are added to a list and a counter
    # incremented. A second solution will also be added, but the loop will
    # terminate if a third is found. A second solution means that the TARGET
    # is invalid; this is handled below.
    a, b, c = divisors[0], divisors[0], divisors[0]
    for aInd in range(len(divisors)):
        a = divisors[aInd]
        for bInd in xrange(aInd+1):
            b = divisors[bInd]
            if a+b <= TARGET-2:
                for cInd in xrange(bInd+1):
                    c = divisors[cInd]
                    if a+b+c <= TARGET-1:
                        d = TARGET - (a+b+c)
                        if d <= c:
                            if a*b*c*d == TARGET*1000000:
                                if counter == 2:
                                    break
                                else:
                                    unique.append([a+b+c+d, a, b, c, d])
                                    counter += 1

    # Tests the length of the unique list. If exactly one, the solutions
    # variable is increased and the numbers are printed via the asMoney()
    # method.
    if len(unique) == 1:
        solutions += 1
        for i in range(len(unique)):
            print asMoney(unique[0][0]), "=",
            print asMoney(unique[0][4]), "+",
            print asMoney(unique[0][3]), "+",
            print asMoney(unique[0][2]), "+",
            print asMoney(unique[0][1])
print solutions, "solutions"

# print("----%s seconds ---" % (time.time() - start_time))
