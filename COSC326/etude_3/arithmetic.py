'''
 Etude 3: Arithmetic
 File name: arithmetic.py
 Author: Stefan Pedersen 1427681
 Date created: 12/01/2017
 Date last modified: 13/01/2017
 Python version: 2.7

 Brute-force algorithm for finding a combination of + or * operators which
 when applied to a list of numbers will attempt to find a given target.

 (N)ormal and (L)eft-to-right evaluation are addressed.

 61 LOC

 Finds solution for:
 10 numbers: 0.003 seconds
 15 numbers: 0.18 seconds
 20 numbers: 8.13 seconds
 21 numbers: 17.0 seconds
 22 numbers: 35.8 seconds
 23 numbers: 75.9 seconds
 24 numbers: 161.5 seconds
 25 numbers: 404.3 seconds
  '''
import fileinput, re, math, time
start_time = time.time()

nums = []
constraints = []

for line in fileinput.input():
    combinations = []
    if not re.search('[NL]', line):
        nums = line.split()
    else:
        constraints = line.split()
        target = int(constraints[0])
        numOps = len(nums)-1 #number of operators
        numSolutions = int(math.pow(2, (numOps))) #number of permutations poss
        ops = []
        # Append operators in the correct order
        for i in range(numSolutions):
            for j in reversed(range(numOps)):
                if (i%math.pow(2,j+1)) < (math.pow(2, j)):
                    ops.append('+'); #0 == '+'
                else:
                    ops.append('*'); #1 == '*'

        # Proceedure for (L)eft to Right arithmetic
        if constraints[1] == 'L':
            # Generate a list of the operators for the given scenario
            # (essentially a truth-table).
            # Each scenario has 2^n-1 combinations (where n is the numbers
            # provided). This means that there are n-1 operators needed for
            # each combination. For a scenario with three numbers, the first
            # operator in a combination will be '+' if n%(2^3)<2^2, where
            # n = the iteration of the combination starting with 0; it will
            # be * otherwise. The second operator will be '+' if n%(2^2)<2^1,
            # and so on.

            # Group operators per combination (if there is more than 1 number)
            if ops:
                opGroups = [ops[x:x+numOps] for x in range(0, len(ops), numOps)]
                # Generate each combination by iterating over the numbers
                # avaliable and the operator groups
                for i in range(numSolutions):
                    combL = int(nums[0])
                    for j in range(numOps):
                        if opGroups[i][j] == '+':
                            combL += int(nums[j+1])
                        else:
                            combL *= int(nums[j+1])
                    # If a target found, append to the combinations list
                    # (for testing purposes), and print out the equation.
                    if combL == target:
                        combinations.append(combL)
                        print "L", nums[0],
                        for k in range(numOps):
                            print opGroups[i][k], nums[k+1],
                        print "\r" #needed for new line, but adds a space?
                        break # stop finding multiple solutions

            # Take care of a single number with no operators which is
            # equal to the target
            if len(nums) == 1 and int(nums[0]) == target:
                print 'L', nums[0]
            elif not combinations:
                print 'L', 'impossible'

        # Proceedure for (N)ormal arithmetic
        else:
            # Group operators per combination (if there is more than 1 number)
            if ops:
                opGroups = [ops[x:x+numOps] for x in range(0, len(ops), numOps)]
                # Generate each combination by iterating over the numbers
                # avaliable and the operator groups
                for i in range(numSolutions):
                    combN = []
                    combN = (nums[0])
                    for j in range(numOps):
                        combN += (opGroups[i][j])
                        combN += (nums[j+1])

                    # Evaluate the string (employs normal order operations).
                    # If a target found, append to the combinations list
                    # (for testing purposes), and print out the equation.
                    if eval(combN) == target:
                        combinations.append(combN)
                        print "N", nums[0],
                        for k in range(numOps):
                            print opGroups[i][k], nums[k+1],
                        print "\r" #needed for new line, but adds a space?
                        break # stop finding multiple solutions

            # Take care of a single number with no operators which is
            # equal to the target
            if len(nums) == 1 and int(nums[0]) == target:
                print 'N', nums[0]
            # Note impossible combinations
            elif not combinations:
                print 'N', 'impossible'
print("----%s seconds ---" % (time.time() - start_time))
