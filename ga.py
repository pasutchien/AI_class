import random
import copy
#8 queen solver

#state = [0,3,2,4] index is column, value is row
def heuristic(state): #number of paired queens
    count = 0
    for i in range(len(state)):
        for j in range(i+1,len(state)):
            if state[i] == state[j]:
                count += 1
                continue
            if abs(state[i]- state[j]) == abs(i-j):
                count += 1
                continue
    return count

def crossover(state1,state2):
    cut = random.randint(1,len(state1)-1)
    new1 = state1[:cut].copy()
    new2 = state1[cut:].copy()
    new3 = state2[:cut].copy()
    new4 = state2[cut:].copy()
    new_state1 = new1 + new4
    new_state2 = new3 + new2
    return [new_state1,new_state2]
def mutation(state1,state2):
    index1 = random.randint(0,len(state1)-1)
    index2 = random.randint(0,len(state2)-1)
    value1 = random.randint(0,len(state1)-1)
    value2 = random.randint(0,len(state2)-1)
    new_state1 = copy.deepcopy(state1)
    new_state2 = copy.deepcopy(state2)
    new_state1[index1] = value1
    new_state2[index2] = value2
    return [new_state1,new_state2]
def find_best_two(all_state):
    d = dict()
    for state in all_state:
        d[heuristic(state)] = state
    
    sorted_d = dict(sorted(d.items(), key=lambda item: item[0]))
    return list(sorted_d.values())[:2]
def GA(n):
    st1 = []
    st2 = []
    for i in range(n): 
        num1 = random.randint(0,n-1)
        num2 = random.randint(0,n-1)
        st1.append(num1)
        st2.append(num2)
    for i in range(10000):
        if heuristic(st1) == 0:
            print(f"Found at Generation {i}: {st1}")
            return st1
        if heuristic(st2) == 0:
            print(f"Found at Generation {i}: {st2}")
            return st2
        co1,co2 = crossover(st1,st2)
        mu1,mu2 = mutation(st1,st2)
        new_children = [st1,st2,co1,co2,mu1,mu2]
        st1,st2 = find_best_two(new_children)
        if i % 1000 == 0:
            print(f"{st1}, heuristic = {heuristic(st1)} → Found at Generation {i}")
            print(f"{st2}, heuristic = {heuristic(st2)} → Found at Generation {i}")
    print(f"Not Found, End at {st1},{heuristic(st1)}/ {st2},{heuristic(st2)}")
    return 
n = 8
answer = GA(n)

class Solution:
   def solve(self, matrix):
      n = len(matrix)

      rows = set()
      cols = set()
      diags = set()
      rev_diags = set()

      for i in range(n):
         for j in range(n):
            if matrix[i][j]:
               rows.add(i)
               cols.add(j)
               diags.add(i - j)
               rev_diags.add(i + j)

      return len(rows) == len(cols) == len(diags) == len(rev_diags) == n

ob = Solution()

matrix = [[0 for _ in range(n)] for _ in range(n)]

for c in range(len(answer)):
    matrix[answer[c]][c] = 1
for row in matrix:
    print(row)
                
print(ob.solve(matrix))