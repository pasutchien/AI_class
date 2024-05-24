#state = [1,3,2,4,4,5,6,8] (1,3) location of sheep1 /(2,4) location of sheep2/(4,5) location of sheep3/ (6,8) location of wolf
#Assume fixed dimension 8*8
import random
import copy

def is_ontop(state):
    s = set()
    l = list()
    for i in range(0,len(state),2):
        s.add((state[i],state[i+1]))
        l.append((state[i],state[i+1]))
    if len(s) == len(l):
        return False
    else:
        return True
def get_neighboring_blocks(location, dimension):
    row, col = location
    neighboring_blocks = []
    
    # Iterate through neighboring rows
    for i in range(row - 1, row + 2):
        # Check if the row is within the boundaries
        if 0 <= i < dimension:
            # Iterate through neighboring columns
            for j in range(col - 1, col + 2):
                # Check if the column is within the boundaries
                if 0 <= j < dimension:
                    # Exclude the sheep's current location
                    if (i, j) != location:
                        neighboring_blocks.append((i, j))
    
    return neighboring_blocks
def heuristic(state,sheep):
    count = 0
    sheeps = state[:(sheep*2)]
    wolf = state[(sheep*2):]
    all_animal = []
    for i in range(0,len(state),2):
        all_animal.append((state[i],state[i+1]))
    for i in range(0,len(sheeps),2):
        grass = []
        for j in range(0,len(wolf),2):
            eat_row = range(wolf[j]-2, wolf[j]+3)
            eat_col = range(wolf[j+1]-2,wolf[j+1]+3)
            if sheeps[i] in eat_row and sheeps[i+1] in eat_col:
                count += 3
                break
        grass = get_neighboring_blocks((sheeps[i],sheeps[i+1]),8)
        if grass in all_animal:
            count += 1
    return count
def mutation(state1,state2):
    all_animal_1 = []
    for i in range(0,len(state1),2):
        all_animal_1.append((state1[i],state1[i+1]))
    index1 = random.randint(0,len(state1)-1)
    available1 = list(range(8))
    if index1 % 2 == 0:
        for i in range(len(all_animal_1)):
            if i == index1/2:
                continue
            if all_animal_1[i][1] == state1[index1+1]:
                if all_animal_1[i][0] in available1:
                    available1.remove(all_animal_1[i][0])
    else:
        for i in range(len(all_animal_1)):
            if i == (index1-1)/2:
                continue
            if all_animal_1[i][0] == state1[index1-1]:
                if all_animal_1[i][1] in available1:
                    available1.remove(all_animal_1[i][1])
    value1 = random.choice(available1)
    all_animal_2 = []
    for j in range(0,len(state2),2):
        all_animal_2.append((state2[j],state2[j+1]))
    index2 = random.randint(0,len(state2)-1)
    available2 = list(range(8))
    if index2 % 2 == 0:
        for i in range(len(all_animal_2)):
            if i == index2/2:
                continue
            if all_animal_2[i][1] == state2[index2+1]:
                if all_animal_2[i][0] in available2:
                    available2.remove(all_animal_2[i][0])
    
    else:
        for i in range(len(all_animal_2)):
            if i == (index2-1)/2:
                continue
            if all_animal_2[i][0] == state2[index2-1]:
                if all_animal_2[i][1] in available2:
                    available2.remove(all_animal_2[i][1])
    value2 = random.choice(available2)
    new1 = copy.deepcopy(state1)
    new2 = copy.deepcopy(state2)
    new1[index1] = value1
    new2[index2] = value2
    return [new1,new2]
def crossover(state1,state2):
    available = []
    for i in range(1,len(state1)):
        for j in range(4):
            available.append((i,j))
    while True:
        if not available:
            return None
        cut = random.choice(available)
        available.remove(cut)
        first = copy.deepcopy(state1[:cut[0]])
        second = copy.deepcopy(state1[cut[0]:])
        third = copy.deepcopy(state2[:cut[0]])
        forth = copy.deepcopy(state2[cut[0]:])
        if cut[1] == 0:
            new_state_1 = first+forth
            new_state_2 = third+second
        elif cut[1] == 1:
            new_state_1 = forth+first
            new_state_2 = third+second
        elif cut[1] == 2:
            new_state_1 = first+forth
            new_state_2 = second+third
        else:
            new_state_1 = forth+first
            new_state_2 = second+third
        if is_ontop(new_state_1) == False and is_ontop(new_state_2)== False:
            break
    return [new_state_1,new_state_2]
def findbesttwo(all6,sheep):
    r = []
    for state in all6:
        r.append((state,heuristic(state,sheep)))
    sorted_list = sorted(r, key=lambda x: x[1])
    return [tup[0] for tup in sorted_list[:2]]
def draw_board(state,sheep, dimension=8):
    board = [['_' for _ in range(dimension)] for _ in range(dimension)]
    
    # Fill the board with sheep and wolves
    for i in range(0, len(state), 2):
        row, col = state[i], state[i + 1]
        if i < (sheep*2):
            board[row][col] = 'S'
        else:
            board[row][col] = 'W'
    
    # Draw the board
    for row in board:
        print(' '.join(row))

def GA(wolf,sheep):
    for k in range(100):
        available1 = []
        available2 = []
        st1 = []
        st2 = []
        for i in range(8):
            for j in range(8):
                available1.append((i,j))
                available2.append((i,j))
        for i in range(wolf+sheep):
            location1 = random.choice(available1)
            available1.remove(location1)
            st1.append(location1[0])
            st1.append(location1[1])
            location2 = random.choice(available2)
            available2.remove(location2)
            st2.append(location2[0])
            st2.append(location2[1])
        print(st1,st2)
        for i in range(10000):
            if heuristic(st1,sheep) == 0:
                print(f"answer found at generation{i}:")
                print(f"sheep at: {st1[:(sheep*2)]}, wolves at: {st1[(sheep*2):]}")
                draw_board(st1,sheep)
                return st1
            if heuristic(st2,sheep) == 0:
                print(f"answer found at generation{i}:")
                print(f"sheep at: {st2[:(sheep*2)]}, wolves at: {st2[(sheep*2):]}")
                draw_board(st2,sheep)
                return st2
            new1,new2 = mutation(st1,st2)
            if is_ontop(new1) == True or is_ontop(new2) == True:
                print("Wrong")
                return
            new = crossover(st1,st2)
            if new == None:
                break
            all6 = [st1,st2,new1,new2,new[0],new[1]]
            st1,st2 = findbesttwo(all6,sheep)
            if i % 1000 == 0:
                print(f"sheep at: {st1[:(sheep*2)]}, wolves at: {st1[(sheep*2):]}, heuristic = {heuristic(st1,sheep)}")
                print(f"sheep at: {st2[:(sheep*2)]}, wolves at: {st2[(sheep*2):]}, heuristic = {heuristic(st2,sheep)}")

answer =GA(3,20)
print(is_ontop(answer))