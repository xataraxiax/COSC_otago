

import fileinput, re, math

nums = []
constraints = []



for line in fileinput.input():
    solutions = []
    rule = True
    if not re.search('[NL]', line):
        nums = line.split()        
    else:
        constraints = line.split()
        target = constraints[0]
        if constraints[1] == 'L':
            rule = False

        ops = len(nums)-1
        numSolutions = int(math.pow(2, (ops)))
        print "num solutions", numSolutions
        
        # Generate a list of the operators for the given scenario. Each
        # scenario has 2^n-1 combinations (where n is the numbers provided).
        # This means that there are n-1 operators needed for each combination.
        # For a scenario with three numbers, the first operator in a
        # combination will be '+' if n%(2^3)<2^2, where n = the iteration of
        # the combination starting with 0; it will be * otherwise. The second
        # operator will be '+' if n%(2^2)<2^1, and so on.
        operators = [] 
        for i in range(numSolutions):               
            for j in reversed(range(ops)): 
                if (i%math.pow(2,j+1)) < (math.pow(2, j)):
                    operators.append('+');                    
                else:
                    operators.append('*');
        # Group operators per combination
        if operators:
            opGroups = [operators[x:x+ops] for x in range(0, len(operators), ops)]

            solutions = [nums[0]]

        print opGroups
        print solutions



                    
                    
        # print 0%math.pow(2, ops)
        # print math.pow(2, 2)
            

        print "numbers:", nums, "\n"

 #        print "operators:", operators
 #        print "target:", target
 #        print "rule:", rule, "\n"


    


        

    


