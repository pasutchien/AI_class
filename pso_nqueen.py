import numpy as np
import random
def sum(v):
    if v == 0:
        return 0
    return v + sum(v-1)
def fitness(x):
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


bee_id = 0
all_best = {}
def find_global_best():
    global all_best
    x = {}
    for k,v in all_best.items():
        x[k] = fitness(v)
    y = sorted(x.items(), key = lambda a: a[1])
    return all_best[y[0][0]]

class bee:
    def __init__(self,x,v):
        global bee_id
        global all_best
        self.x = np.copy(x)
        self.v = np.copy(v)
        self.p = np.copy(x)
        self.x_f = fitness(x)
        self.p_f = fitness(x)
        self.id = bee_id
        bee_id += 1
        all_best[self.id] = self.p
    def calculate_v(self): #g is global best
        w=1
        c1=0.1
        c2=0.1
        g = find_global_best()
        v2 = np.copy((w*self.v) + c1*random.random()*(self.p-self.x) + c2*random.random()*(g-self.x))
        return v2
    def move(self):
        global all_best
        self.x = self.x + np.int64(self.v)
        self.x = np.clip(self.x,0,len(self.x)-1)

        if fitness(self.x) < fitness(self.p): #if we find better local max
            self.p = np.copy(self.x)
            self.p_f = fitness(self.x)
            all_best[self.id] = np.copy(self.p)
        self.x_f = fitness(self.x)
        self.v = self.calculate_v()
def pso(n):
    bees=[]
    for i in range(n*2):
        x = np.random.randint(low = 0, high = n, size=n)
        v = np.random.randint(low = -1, high = 1, size = n)
        b = bee(x,v)
        bees.append(b)
    for i in range(200000):
        g = find_global_best()
        if fitness(g) == 0:
            print(f"Answer found at iteration {i}: {g}")
            return
        for b in bees:
            b.move()
        if i  %1000 == 0:
            print(f"iteration: {i}")
            for b in bees:
                print(b.x,fitness(b.x))
            
                #print("v=", b.v)
    g = find_global_best()
    print(f"Best location found at {g}, {fitness(g)}")
pso(8)