'''
 Etude 2: 7-11
 File name: s711.py
 Author: Stefan Pedersen 1427681
 Date created: 11/01/2017
 Date last modified: 12/01/2017
 Python version: 2.7

 Modified python translation of the brute force method for finding four
 numbers where a <= b <= c <= d && a+b+c+d == abcd.
 Originally in c (Joahua Hill 'The 7-11 Problem'
 - www.untruth.org/~josh/math/711.pdf)
'''
import time
start_time = time.time()

a, b, c, d = 1, 2, 3, 4
TARGET = 7.11 * 100000000

for d in range (4, int(TARGET/1000000)):
    if TARGET % d != 0:
        continue
    for c in range (3, d):
        if TARGET % c != 0:
            continue
        for b in range (2, c):
            if TARGET % b != 0:
                continue
            for a in range (1, b):
                if TARGET % a != 0:
                    continue
                if((a+b+c+d)*1000000 == a*b*c*d == TARGET):
                    print '$%.2f:  $%.2f $%.2f $%.2f $%.2f' % ((a+b+c+d)/float(100),
                    a/float(100), b/float(100), c/float(100), d/float(100))

print("----%s seconds ---" % (time.time() - start_time))
