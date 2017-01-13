'''
 Etude 2: 7-11
 File name: s711.py
 Author: Stefan Pedersen 1427681
 Date created: 11/01/2017
 Date last modified: 12/01/2017
 Python version: 2.7

 Program for finding four numbers where a <= b <= c <= d && a+b+c+d == abcd,
 totalling exactly 7.11.
 Main algorithm inspired by a program written in C at
 http://everything2.com/title/The+7-Eleven+problem (user: efnar, Dec 06/2010)
'''
# import time
# start_time = time.time()

TARGET = 711
solutions = 0
a, b, c, d = 0,0,0,0

aInd, bInd, cInd = 0, 0, 0,
divisors = []

# Function to return numbers in monetary format without using floating points.
def asMoney(m):
    return("$%d" % (m/100))+(".%02d" % (m%100))

# Loop to generate list of divisors for the current target. To avoid
# serious problems involved with floating-point division, we express
# the ammount of money in cents. The TARGET here is therefore multiplied
# by 1000000.
for x in xrange(1,TARGET):
    if (TARGET*1000000) % x == 0:
        divisors.append(x)

# Nested for-loop permeates through the divisors. We are told that there is
# exactly one solution to this problem, so as soon the target is reached the
# the four component numbers are printed out.
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
                            print asMoney(d),asMoney(c),asMoney(b),asMoney(a)
                            # break

# print("----%s seconds ---" % (time.time() - start_time))
