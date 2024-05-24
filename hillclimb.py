#N Queen game
#              [2,1,3,0] means 
#               ^ ^ ^ ^
#        column 0 1 2 3
#  queen on row 2 1 3 0
import random
def sum(v):
    if v == 0:
        return 0
    return v + sum(v-1)
def heuristic(x):
    #number of paired queens
    #row
    r = {}
    count = 0
    for i in x:
        if i in r:
            r[i] += 1
        else:
            r[i] = 1
    for v in r.values():
        if v>= 2:
            count += sum(v-1)
    for i in range(len(x)):
        k = i+1
        for j in range(k,len(x)):
            if x[i] == (x[j] - abs(j-i)) or x[i] == (x[j] + abs(j-i)):
                count += 1
    return count

def gen_successors(x):
    successors = []
    for i in range(len(x)):
        y = list(x)
        if y[i] == 0:
            #only move down
            y[i] += 1
            successors.append(list(y))
        elif y[i] == len(x)-1:
            #only move up
            y[i] -= 1
            successors.append(list(y))
        else:
            y[i] += 1
            successors.append(list(y))
            y[i] -= 2
            successors.append(list(y))
    return successors
def find_best_successors(successors):
    d = {}
    for successor in successors:
        h = heuristic(successor)
        d[h] = successor
    d2 = dict(sorted(d.items()))
    return list(d2.values())[0]
def hillclimb(n):
    result = False
    for i in range(5000):
        l = range(n)
        s = []
        last3 = []
        for i in l:
            s.append(random.choice(l))
        while True:
            if(heuristic(s) == 0):
                print("Found: ", s)
                print(heuristic(s))
                result = True
                return
            successors = gen_successors(s)
            y = find_best_successors(successors)
            if(heuristic(y) > heuristic(s)):
                #local max
                print("Local Max: ", s)
                break
            last3.append(s)
            if len(last3) > 3:
                last3.pop(0)
            if y in last3:
                print("Same Heuristic", s)
                break
            s = y
    print("Goal Not Found")
hillclimb(4)
