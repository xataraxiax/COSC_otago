'''
    Etude 8: Harmonious Numbers
    File name: harmoniousNumbers.py
    Authors: Stefan Pedersen 1427681
    Date created: 09/02/2017
    Date last modified: 10/02/2017
    Python Version: 2.7
'''
import math, time
start_time = time.time()
harmonious1 = []
harmonious2 = []

def findHarmonious(n):
    count = 0
    for i in range(2, n):
        a = sumOfDivisors(i)
        b = sumOfDivisors(a)
        if (a not in harmonious1) or (b not in harmonious2):
            if(a != i and i ==b):
                if (a < b):
                    harmonious1.append(a)
                    harmonious2.append(b)
                else:
                    harmonious1.append(b)
                    harmonious2.append(a)

def sumOfDivisors(n):
    sumD = 0
    cand = 2
    while cand * cand < n:
        if n % cand == 0:
            sumD += cand + n/cand
        cand += 1
    if cand * cand == sumD:
        sumD += cand
    return sumD

findHarmonious(2000000)
for i in range(len(harmonious1)):
    print harmonious1[i], harmonious2[i]
#print("----%s seconds ---" % (time.time() - start_time))
