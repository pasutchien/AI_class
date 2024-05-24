#state = [4,3,4,4] 4 stacks
import copy

def available_moves(state):
    #moves will be (0,3) first stack, takeout 3
    moves = []
    for i in range(len(state)):
        for j in range(1,state[i]+1):
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
def maxvalue(state,alpha,beta):
    if terminal(state):
        return utility('max')
    v = -999
    moves = available_moves(state)
    for move in moves:
        v = max(v,minvalue(result(state,move),alpha,beta))
        if v >= alpha:
            alpha = v
        if alpha >= beta:
            return v
    return v
def minvalue(state,alpha,beta):
    if terminal(state):
        return utility('min')
    v = 999
    moves = available_moves(state)
    for move in moves:
        v = min(v,maxvalue(result(state,move),alpha,beta))
        if v <= beta:
            beta = v
        if alpha >= beta:
            return v
    return v
def minimax(state,turn):
    if terminal(state):
        return None
    if turn == 'max':
        alpha = -999
        beta = 999
        v = maxvalue(state,alpha,beta)
        moves = available_moves(state)
        for move in moves:
            x = minvalue(result(state,move),alpha,beta)
            if x == v:
                return move
            if x >= alpha:
                alpha = x
    else:
        alpha = -999
        beta = 999
        v = minvalue(state,alpha,beta)
        moves = available_moves(state)
        # for move in moves:
        #     print(maxvalue(result(state,move)))

        for move in moves:
            x = maxvalue(result(state,move),alpha,beta)
            if x == v:
                return move
            if x <= beta:
                beta = x
turn = 'min'
initial = input("Enter initial stack: ")
state = list(map(int, initial.split()))
while (terminal(state) == False):
    if turn == 'max':
        ask = input("Enter your action")
        action = tuple(map(int, ask.split()))
        state = result(state,action)
        turn = 'min'
    else:
        action = minimax(state,turn)
        state = result(state,action)
        turn = 'max'
    print(state)
if utility(turn) == 1:
    print('player wins')
else:
    print('bot wins')

