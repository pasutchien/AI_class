import random
import copy
import time
last_id = 0 
def generate_grass():
    grid = [['.' for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            if random.random() < 0.5:  # Adjust the probability as needed
                grid[i][j] = 'G'  # 'G' represents grass
    #-------------------------------EXTRA--------------------------------------------------------
            if random.random() < 0.2:
                grid[i][j] = 'D' # 'D' means dogs
    
    grid[0][0] = 'X'

    return grid

def print_grass(grass):
    for row in grass:
        print(' '.join(row))
    print("----------------------------------")
# Example usage:

#node = (ID, state, (position_row,position_column), parent_ID)
def available_moves(node):
    pos_row = node[2][0]
    pos_column = node[2][1]
    moves = ["up","down","left","right","cut"]
    if pos_row == 0:
        moves.remove("up")
    if pos_row == 3:
        moves.remove("down")
    if pos_column == 0:
        moves.remove("left")
    if pos_column == 3:
        moves.remove("right")
    if node[1][pos_row][pos_column] != 'XG':
        moves.remove("cut")
    #-------------------------EXTRA----------------------------------
    if 'up' in moves:
        if node[1][node[2][0]-1][node[2][1]] == 'D': # have dog in upper box
            moves.remove("up")
    if 'down' in moves:
        if node[1][node[2][0]+1][node[2][1]] == 'D': # have dog in lower box
            moves.remove("down")
    if 'left' in moves:
        if node[1][node[2][0]][node[2][1]-1] == 'D':
            moves.remove("left")
    if 'right' in moves:
        if node[1][node[2][0]][node[2][1] + 1] == 'D':
            moves.remove("right")
    return moves
def gen_successors(node):
    global last_id
    moves = available_moves(node)
    result = []
    for move in moves:
        last_id += 1
        if move != "cut":
            if move == "up":
                new_position_row = node[2][0] - 1
                new_position_col = node[2][1]
            if move == "down":
                new_position_row = node[2][0] + 1
                new_position_col = node[2][1]
            if move == 'left':
                new_position_row = node[2][0]
                new_position_col = node[2][1] - 1
            if move == 'right':
                new_position_row = node[2][0]
                new_position_col = node[2][1] + 1
            new_state = copy.deepcopy(node[1])
            if new_state[node[2][0]][node[2][1]] == 'X':
                new_state[node[2][0]][node[2][1]] = '.'
            elif new_state[node[2][0]][node[2][1]] == 'XG':
                new_state[node[2][0]][node[2][1]] = 'G'
            if new_state[new_position_row][new_position_col] == '.':
                new_state[new_position_row][new_position_col] = 'X'
            elif new_state[new_position_row][new_position_col] == 'G':
                new_state[new_position_row][new_position_col] = 'XG'
            new_node = (last_id,new_state,(new_position_row,new_position_col), node[0])
            result.append(new_node)
        else:
            new_state = copy.deepcopy(node[1])
            new_state[node[2][0]][node[2][1]] = 'X'
            new_node = (last_id,new_state,(node[2][0],node[2][1]), node[0])
            result.append(new_node)
    return result
def find_node_from_id(visited,id):
    for v in visited:
        if v[0] == id:
            return v 
def print_best_result(node,visited):
    while(node[3] != -1):
        print_grass(node[1])
        node = find_node_from_id(visited,node[3])
    return None
def is_goal(node):
    for row in node[1]:
        for col in row:
            if col == "G" or col == "XG":
                return False
    return True
def has_visited(node,visited):
    for v in visited:
        if node[1] == v[1]:
            return True
    return False
def BFS(initial):
    successors = []
    fringe = []
    visited = []
    fringe.append(initial)
    while fringe:
        # for f in fringe:
        #     print_grass(f[1])
        if is_goal(fringe[0]):
            print_best_result(fringe[0],visited)
            return
        if not (has_visited(fringe[0],visited)):
            successors = gen_successors(fringe[0])
        else:
            successors = []
        visited.append(fringe[0])

        fringe = fringe + successors
        fringe = fringe[1:]
        # print("----------------------------------")
        # time.sleep(5)
initial_state = generate_grass()
initial_node = (last_id,initial_state,(0,0),-1)

print_grass(initial_state)
print("-----------------------------------------------------------")
BFS(initial_node)