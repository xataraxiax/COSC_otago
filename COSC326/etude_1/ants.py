'''
    Etude 1: Ants on a Plane
    File name: ants.py
    Authors: Stefan Pedersen 1427681, Jono Sue 4097307
    Date created: 09/01/2017
    Date last modified: 10/01/2017
    Python Version: 2.7
'''

import re, fileinput, time
#start_time = time.time()

dnaList, visited, cardinal = [], [], ["N", "E", "S", "W"]
direction = "N"
steps = 0
x, y = 0, 0
found = False

# Moves the ant one step based on its DNA, and its position on the plane.
# Checks to see whether the current tile has been visited, if so it
# checks for it's current state. Reverse search is used to improve efficiency,
# as the most recently added are more likely to be visited sooner.
# If not, it assumes that the tile has the default initial state. The new state
# of the tile is recorded and adeded to the visited list.
def move():
    global found, direction, x, y
    for row in reversed(visited):
        if row[0] == x and row[1] == y:
            found = True
            for dna in dnaList:
                if row[2] == dna[0]:
                    d = cardinal.index(direction)
                    nextStep = dna[1][d]
                    visited[visited.index(row)] = [x, y, dna[2][d]]
                    direction = nextStep
                    if nextStep == "N":
                        y+=1
                    elif nextStep == 'E':
                        x+=1
                    elif nextStep == 'S':
                        y-=1
                    elif nextStep == 'W':
                        x-=1
                    return

    if found == False:
        d = cardinal.index(direction)
        nextStep = dnaList[0][1][d]
        visited.append([x, y, dnaList[0][2][d]])
        direction = nextStep
        if nextStep == 'N':
            y+=1
        elif nextStep == 'E':
            x+=1
        elif nextStep == 'S':
            y-=1
        elif nextStep == 'W':
            x-=1

# Loop controlling the number of moves the ant makes based on the step input
def begin():
    global steps, found
    while steps > 0:
        move()
        found = False
        steps -= 1

# Reads scenarios input from text file. If a number is not found, a regex
# checks for appropriate format of ant DNA, then appends the line to dnaList.
# When a number is found this is added to steps, and the begin() method is
# called initiating the scenario. The scenario and final coordinates are then
# printed, and relevant variables are reset.
for line in fileinput.input():
    if not line.startswith("#"):
        if line == "\n":
            print line,
            continue
        try:
            steps = int(line)
            totalSteps = steps
            if not dnaList:
                print "There are no (valid) DNA scenarios in this iteration"
                exit()
            begin()
            print(line),
            print "#", x, y
            x, y = 0, 0
            visited, dnaList = [], []
            direction = "N"
            #print("----%s seconds ---" % (time.time() - start_time))
        except ValueError:
            if not re.match('(.)(\s)([NSEW]{4})(\s)(.{4})$', line):
                print "Invalid DNA line"
            else:
                dnaList.append(line.split())
                print line,
