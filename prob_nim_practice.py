#state = [4,3,4,4] 4 stacks
import copy
import random
def tossdice():
    return random.randint(1,6)
def prob(action):
    return 1 - (action[1]-1)/6
def available_moves(state,dice = 6):
    #moves will be (0,3) first stack, takeout 3
    moves = []
    for i in range(len(state)):
        for j in range(1,state[i]+1):
            if j > dice:
                break
            moves.append((i,j))
    return moves
def result(state,action):
    position = action[0]
    new_state = copy.deepcopy(state)
    new_state[position] = new_state[position] - action[1]
    return new_state
def terminal(state):
    for num in state:
        if num > 0 :
            return False
    return True
def utility(turn):
    if turn == 'max':
        return -1
    else:
        return 1
def chance(state,turn):
    if terminal(state) == True:
        return utility(turn)
    if turn == 'max':
        turn = 'min'
    else:
        turn = 'max'
    v = 0
    moves = available_moves(state)
    for move in moves:
        v = v + (prob(move)*chance(result(state,move),turn))
    return v/len(moves)

def maxvalue(state,dice):
    if terminal(state):
        return utility('max')
    v = -999
    moves = available_moves(state,dice)
    for move in moves:
        v = max(v,chance(result(state,move),'min'))
    return v
def minvalue(state,dice):
    if terminal(state):
        return utility('min')
    v = 999
    moves = available_moves(state,dice)
    for move in moves:
        v = min(v,chance(result(state,move),'max'))
    return v
def minimax(state,turn,dice):
    if terminal(state):
        return None
    if turn == 'max':
        v = maxvalue(state,dice)
        moves = available_moves(state,dice)
        for move in moves:
            if chance(result(state,move),'min') == v:
                return move
    else:
        v = minvalue(state,dice)
        moves = available_moves(state,dice)
        for move in moves:
            if chance(result(state,move), 'max') == v:
                return move
turn = 'min'
initial = input("Enter initial stack: ")
state = list(map(int, initial.split()))
while (terminal(state) == False):
    dice = tossdice()
    print("dice =" +str(dice))
    if turn == 'max':
        while True:
            ask = input("Enter your action")
            action = tuple(map(int, ask.split()))
            if action in available_moves(state,dice):
                break
            else:
                print("move invalid")
        state = result(state,action)
        turn = 'min'
    else:
        action = minimax(state,turn,dice)
        state = result(state,action)
        turn = 'max'
    print(state)
if utility(turn) == 1:
    print('player wins')
else:
    print('bot wins')

