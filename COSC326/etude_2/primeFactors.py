import math
import time
start_time = time.time()

TARGET = 711
primeFactors = []
partial = [1, 1, 1, 1]
done = False

def primes(n):
    d=2
    while d*d <= n:
        while (n%d)==0:
            primeFactors.append(d)
            n /= d
        d += 1
    if n > 1:
        primeFactors.append(n)
    return (primeFactors)

# print primes(TARGET * 1000000)
#primeFactors.reverse()
primeFactors = primes(TARGET * 1000000)
num = len(primeFactors)

def calc(x):
    global done
    if x == num:
        sum = 0
        for i in range(4):
            sum += partial[i]
        if sum == TARGET:
            done = True
            partial.sort()
            for i in range(4):

                print "$%.2f" % (partial[i]/float(100)),
    else:
        for i in range(4):
            partial[i] *= primeFactors[x]
            if partial[i] < TARGET:
                calc(x+1)
                if done == True:
                    break

            partial[i] /= primeFactors[x]
            if x == i:
                break
# for i in range(644, 999):
#     TARGET = i
calc(0)
print("----%s seconds ---" % (time.time() - start_time))



# def divisors(n):
#     origNum = n
#     prime_list = primes(n)
#     divisors = [1, n]
#     for i in prime_list:
#         n = origNum
#         while not n % i:
#             divisors.append(i)
#             n = int(n/i)
#     for i in range(len(divisors)-2):
#         for j in range(i+1, len(divisors)-1):
#             if i and j and j != n and not origNum % (i*j):
#                 divisors.append(i*j)
#     divisors = list(set(divisors))
#     divisors.sort()
#     return divisors

# for test in range(100000000, 999900000, 1000000):
#     print test, ": ", divisors(test)

# print primes(711000000)
# divz = []
# for x in range(2,711):
#     if 711000000 % x == 0:
#
#         divz.append(x)
# print len(divz)
