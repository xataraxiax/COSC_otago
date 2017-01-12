'''
    Etude 1: Ants on a Plane
    File name: ants.py
    Authors: Stefan Pedersen 1427681, Jono Sue 4097307
    Date created: 09/01/2017
    Date last modified: 11/01/2017
    Python Version: 2.7
'''

import re, fileinput, time

dnaList, cardinal = [], ["N", "E", "S", "W"]
visited = {}
direction = "N"
steps = 0
x, y = 0, 0

# Moves the ant one step based on its DNA, and its position on the plane.
# Checks a dictionary to see whether the current tile has been visited, if so it
# checks for it's current state.
# If not, it assumes that the tile has the default initial state. The new state
# of the tile is recorded and adeded to the visited dictionary. The ensuing
# direction is determined by the state of the current tile.
def move():
    global direction, x, y
    if visited.has_key((x,y)):
        for dna in dnaList:
            if visited[x, y] == dna[0]:
                d = cardinal.index(direction)
                nextStep = dna[1][d]
                visited[x, y] = dna[2][d]
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
    else:
        d = cardinal.index(direction)
        nextStep = dnaList[0][1][d]
        visited[x, y] = dnaList[0][2][d]
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
    global steps
    while steps > 0:
        move()
        steps -= 1

# Reads scenarios input from text file. Comment lines are ignored. If a number
# is not found, a regex checks for appropriate format of ant DNA, then appends
# the line to dnaList.
# When a line consists exclusively of a digit it is assigned to steps, and the
# begin() method is called initiating the scenario. The scenario and final
# coordinates are then printed, and relevant variables are reset.
# NOTE: Exceptions for invalid DNA halt the program.
for line in fileinput.input():
    #start_time = time.time()
    if not line.startswith("#"):
	if line == "\n":
            print line,
            continue
        if line.strip('\n').isdigit():
            steps = int(line)
            if not dnaList:
                print "There are no (valid) DNA scenarios in this iteration"
                exit()
            begin()
            print(line),
            print "#", x, y
            x, y = 0, 0
            visited, dnaList = {}, []
            direction = "N"
            #print("----%s seconds ---" % (time.time() - start_time))
        else:
            if not re.match('(.)(\s)([NSEW]{4})(\s)(.{4})$', line):
                print "the dna to be matched is: ", line
                print "Invalid DNA line"
            else:
                dnaList.append([line[0], line[2:6], line[7:11]])
                print line,
