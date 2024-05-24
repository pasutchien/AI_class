#state = (7,[0,2,3,4,5,6]) 7 is the dimension 7*7
#let's say 2 sheeps 1 wolves -> coordinate of first sheep(0,2) second sheep(3,4) first wolve (5,6)
import random
import copy
def is_ontop(state): #check if any sheep or wolve is on top of each other
    count = 0
    for i in range(0,len(state[1]),2):
        for j in range(i+2,len(state[1]),2):
            if state[1][i] == state[1][j] and state[1][i+1] == state[1][j+1]:
                count += 2
    if count>0:
        return True
    else:
        return False
def heuristic(state,sheeps): #sheeps is number of sheeps/ wolves is the rest
    #heuristic is number of sheep eaten
    count = 0
    sheeps_location = state[1][:(sheeps*2)]
    wolves_location = state[1][(sheeps*2):]
    for i in range(0,(sheeps*2),2):#for every sheep
        for j in range(0,len(wolves_location),2):#for every wolves
            if sheeps_location[i] == wolves_location[j]: #same row
                count += 1
                break
            if sheeps_location[i+1] == wolves_location[j+1]:#same column
                count += 1
                break
            if abs(sheeps_location[i] - wolves_location[j]) == abs(sheeps_location[i+1] - wolves_location[j+1]):#same diagonal
                count += 1
                break


    return count
def mutation(state1,state2):
    available_1 = []
    available_2 = []
    dimension = state1[0]
    index_1 = random.randint(0,len(state1[1])-1)
    if index_1 % 2 == 0:#row
        for i in range(dimension):
            available_1.append(i)
        for j in range(0,len(state1[1]),2):
            if j == index_1:
                continue
            if state1[1][j+1] == state1[1][index_1+1]:
                if state1[1][j] in available_1:
                    available_1.remove(state1[1][j])
    else: #column
        for i in range(dimension):
            available_1.append(i)
        for j in range(0,len(state1[1]),2):
            if j == index_1-1:
                continue
            if state1[1][j] == state1[1][index_1-1]:
                if state1[1][j+1] in available_1:
                    available_1.remove(state1[1][j+1])
    value_1 = random.choice(available_1)
    
    
    index_2 = random.randint(0,len(state2[1])-1)
    if index_2 % 2 == 0:#row
        for i in range(dimension):
            available_2.append(i)
        for j in range(0,len(state2[1]),2):
            if j == index_2:
                continue
            if state2[1][j+1] == state2[1][index_2+1]:
                if state2[1][j] in available_2:
                    available_2.remove(state2[1][j])
    else: #column
        for i in range(dimension):
            available_2.append(i)
        for j in range(0,len(state2[1]),2):
            if j == index_2-1:
                continue
            if state2[1][j] == state2[1][index_2-1]:
                if state2[1][j+1] in available_2:
                    available_2.remove(state2[1][j+1])
    
    value_2 = random.choice(available_2)
    new_state_1 = copy.deepcopy(state1[1])
    new_state_2 = copy.deepcopy(state2[1])
    new_state_1[index_1] = value_1
    new_state_2[index_2] = value_2
    first = (dimension,new_state_1)
    second = (dimension,new_state_2)
    return [first,second]
def crossover(state1,state2):
    available = []
    for i in range(1,len(state1[1])):
        for j in range(4):
            available.append((i,j))
    while True:
        if not available:
            return None
        cut = random.choice(available)
        available.remove(cut)
        first = copy.deepcopy(state1[1][:cut[0]])
        second = copy.deepcopy(state1[1][cut[0]:])
        third = copy.deepcopy(state2[1][:cut[0]])
        forth = copy.deepcopy(state2[1][cut[0]:])
        if cut[1] == 0:
            new_state_1 = (state1[0], first+forth)
            new_state_2 = (state2[0], third+second)
        elif cut[1] == 1:
            new_state_1 = (state1[0], forth+first)
            new_state_2 = (state2[0], third+second)
        elif cut[1] == 2:
            new_state_1 = (state1[0], first+forth)
            new_state_2 = (state2[0], second+third)
        else:
            new_state_1 = (state1[0], forth+first)
            new_state_2 = (state2[0], second+third)
        if is_ontop(new_state_1) == False and is_ontop(new_state_2)== False:
            break
    return [new_state_1,new_state_2]
def findbesttwo(all6,sheep):
    r = []
    for state in all6:
        r.append((state,heuristic(state,sheep)))
    sorted_list = sorted(r, key=lambda x: x[1])
    return [tup[0] for tup in sorted_list[:2]]
def print_board(state, sheeps, wolves):
    dimension = state[0]
    board = [['-' for _ in range(dimension)] for _ in range(dimension)]

    # Place sheep on the board
    for i in range(sheeps):
        row = state[1][2*i]
        col = state[1][2*i + 1]
        board[row][col] = 'S'

    # Place wolves on the board
    for i in range(wolves):
        row = state[1][2*sheeps + 2*i]
        col = state[1][2*sheeps + 2*i + 1]
        board[row][col] = 'W'

    # Print the board
    for row in board:
        print(" ".join(row))
def GA(dimension,sheeps,wolves):
    
    st1 = []
    st2 = []
    choice_1 = []
    choice_2 = []
    for i in range(dimension):
        for j in range(dimension):
            choice_1.append((i,j))
            choice_2.append((i,j))
    for i in range((sheeps+wolves)):
        r1 = random.choice(choice_1)
        choice_1.remove(r1)
        r2 = random.choice(choice_2)
        choice_2.remove(r2)
        st1.append(r1[0])
        st1.append(r1[1])
        st2.append(r2[0])
        st2.append(r2[1])
    state1 = (dimension,st1)
    state2 = (dimension,st2)
    print(state1,state2)
    if is_ontop(state1) == False and is_ontop(state2) == False:
        print("work")

    for i in range(100000):
        if heuristic(state1,sheeps) == 0:
            print(f"answer found at generation{i}:")
            print(f"dimension = {dimension}x{dimension}, sheep at: {state1[1][:(sheeps*2)]}, wolves at: {state1[1][(sheeps*2):]}")
            return
        if heuristic(state2,sheeps) == 0:
            print(f"answer found at generation{i}:")
            print(f"dimension = {dimension}x{dimension}, sheep at: {state2[1][:(sheeps*2)]}, wolves at: {state2[1][(sheeps*2):]}")
            return
        new1, new2 = mutation(state1,state2)
        new3, new4 = crossover(state1,state2)
        state1,state2 = findbesttwo([state1,state2,new1,new2,new3,new4], sheeps)
        if i % 1000 == 0:
            print(f"At generation{i}")
            print(f"dimension = {dimension}x{dimension}, sheep at: {state1[1][:(sheeps*2)]}, wolves at: {state1[1][(sheeps*2):]}, heuristic = {heuristic(state1,sheeps)}")
            print(f"At generation{i}")
            print(f"dimension = {dimension}x{dimension}, sheep at: {state2[1][:(sheeps*2)]}, wolves at: {state2[1][(sheeps*2):]}, heuristic = {heuristic(state2, sheeps)}")
        
def GA2(dimension,sheeps,wolves):
    for i in range(100):
        st1 = []
        st2 = []
        choice_1 = []
        choice_2 = []
        for i in range(dimension):
            for j in range(dimension):
                choice_1.append((i,j))
                choice_2.append((i,j))
        for i in range((sheeps+wolves)):
            r1 = random.choice(choice_1)
            choice_1.remove(r1)
            r2 = random.choice(choice_2)
            choice_2.remove(r2)
            st1.append(r1[0])
            st1.append(r1[1])
            st2.append(r2[0])
            st2.append(r2[1])
        state1 = (dimension,st1)
        state2 = (dimension,st2)
        print(state1,state2)

        for i in range(10000):
            if heuristic(state1,sheeps) == 0:
                print(f"answer found at generation{i}:")
                print(f"dimension = {dimension}x{dimension}, sheep at: {state1[1][:(sheeps*2)]}, wolves at: {state1[1][(sheeps*2):]}")
                return state1
            if heuristic(state2,sheeps) == 0:
                print(f"answer found at generation{i}:")
                print(f"dimension = {dimension}x{dimension}, sheep at: {state2[1][:(sheeps*2)]}, wolves at: {state2[1][(sheeps*2):]}")
                return state2
            new1, new2 = mutation(state1,state2)
            new = crossover(state1,state2)
            if new == None:
                print(f'break at generation {i}')
                break
            state1,state2 = findbesttwo([state1,state2,new1,new2,new[0],new[1]], sheeps)
            if i % 1000 == 0:
                print(f"At generation{i}")
                print(f"dimension = {dimension}x{dimension}, sheep at: {state1[1][:(sheeps*2)]}, wolves at: {state1[1][(sheeps*2):]}, heuristic = {heuristic(state1,sheeps)}")
                print(f"At generation{i}")
                print(f"dimension = {dimension}x{dimension}, sheep at: {state2[1][:(sheeps*2)]}, wolves at: {state2[1][(sheeps*2):]}, heuristic = {heuristic(state2, sheeps)}")
    return
result = GA2(5,12,1)
print_board(result,12,1)


