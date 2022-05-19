from collections import namedtuple
import argparse
import copy
import random
import math
import time

State = namedtuple('State',['position','player'])

class Queue:
    def __init__ (self):
        self._data = []
        self._size = 0
    def __len__(self):
        return self._size
    def is_empty(self):
        return self._size == 0
    def enqueue(self, item):
        self._size+=1
        self._data.append(item)
    def dequeue(self):
        self._size-=1
        return self._data.pop(0)
    def info(self):
        return self._data


def initial_state(rows,columns,pieces):
    Size = columns * (pieces)
    rest = (rows - pieces*2) * columns
    X = []
    X2 = []
    Spaces = []
    Spaces2 = []
    O = []
    O2 = []
    Board = []

    for i in range (Size):
        X.append('X')
        O.append('O')
    for i in range ((pieces)):
        X2.append(X[i*columns:(i+1) * columns])
        O2.append(O[i*columns:(i+1) * columns])
    for j in range (rest):
        Spaces.append('.')
    for i in range (rows - pieces*2):
        Spaces2.append(Spaces[i*columns:(i+1) * columns])
    for i in range(pieces):
        Board.append(X2[i])
    for i in range (rows - pieces*2):
        Board.append(Spaces2[i])
    for i in range(pieces):
        Board.append(O2[i])
    starting_state = State(Board,"W")
    return  starting_state

def display_state(state):
    show = ""
    for i in range(len(state[0])):
        temp = ""
        for j in state[0][i]:
            temp +=j
        show+= temp+"\n"
    print("----------------------------")
    return show
        # print(state[0][i])#prints each line as a list

def white_pieces(state):
    white=[]
    black = []
    board = state[0]
    for rows in range (len(board)):
        for cols in range(len(board[0])):
            if board[rows][cols]== 'O':
                piece = []
                piece.append(rows)
                piece.append(cols)
                piece_tuple = tuple(piece)
                white.append(piece_tuple)
    return white#list of tuple locations

def black_pieces(state):
    black = []
    board = state[0]
    for rows in range (len(board)):
        for cols in range(len(board[0])):
            if board[rows][cols]== 'X':
                piece = []
                piece.append(rows)
                piece.append(cols)
                piece_tuple = tuple(piece)
                black.append(piece_tuple)
    return black #list of tuple locations in the board

def game_ending(state):
    count = 0
    Board = state[0]
    for j in range(len(state[0])):
        if Board[0][j-1] == 'O' or Board[(len(state[0])-1)][j-1] == 'X':
            return True

def move_generator(state):
    black = black_pieces(state)
    white = white_pieces(state)
    actions = {}
    if game_ending(state)==True:
        return actions#"The game has ended no further moves to generate"
    if state[1]== "W":
        for pos in white:
            ###can't move
            check = (pos[0]-1, pos[1])
            ck = (pos[0]-1, pos[1]-1)#left diagonal
            ck_2 = (pos[0]-1, pos[1]+1)#right diagonal


            check_2 = pos[1]-1#out of bound to the left
            check_3 = pos[1]+1#out of bound to the right
#             if check in white or ck in white or ck_2 in white or check in black:
#                 continue
            if check_2<0:
                if check in white and ck_2 in white:
                    continue
                elif check in black and ck_2 in white:
                    continue
                elif check in white or check in black:
                    actions[pos]=[(pos[0]-1, pos[1]+1)]
                else:
                    actions[pos]=[(pos[0]-1, pos[1]),(pos[0]-1, pos[1]+1)]

            elif check_3>=len(state[0]):
                if check in white and ck in white:
                    continue
                elif check in black and ck in white:
                    continue
                elif check in white or check in black:
                    actions[pos]=[(pos[0]-1, pos[1]-1)]
                else:
                    actions[pos]=[(pos[0]-1, pos[1]),(pos[0]-1, pos[1]-1)]
            else:
                if check in white and ck in white and ck_2 in white:
                    continue
                elif check in black and ck in white and ck_2 in white:
                    continue

                elif ck in white and ck_2 in white:
                    actions[pos]=[(pos[0]+1, pos[1])]

                elif check in white and ck in white:
                    actions[pos]=[(pos[0]-1, pos[1]+1)]
                elif check in white and ck_2 in white:
                    actions[pos]=[(pos[0]-1, pos[1]-1)]
                elif check in black and ck in white:
                    actions[pos]=[(pos[0]-1, pos[1]+1)]
                elif check in black and ck_2 in white:
                    actions[pos]=[(pos[0]-1, pos[1]-1)]
                #check for two moves
                elif check in white:
                    actions[pos]=[(pos[0]-1, pos[1]-1),(pos[0]-1, pos[1]+1)]
                elif check in black:
                    actions[pos]=[(pos[0]-1, pos[1]-1),(pos[0]-1, pos[1]+1)]
                elif ck in white:
                    actions[pos]=[(pos[0]-1, pos[1]),(pos[0]-1, pos[1]+1)]
                elif ck_2 in white:
                    actions[pos]=[(pos[0]-1, pos[1]),(pos[0]-1, pos[1]-1)]
                else:
                    actions[pos]=[(pos[0]-1, pos[1]),(pos[0]-1, pos[1]-1),(pos[0]-1, pos[1]+1)]



#                 if check not in white
#
    if state[1]== "B":
        for pos in black:
            check = (pos[0]+1, pos[1])
            ck = (pos[0]+1, pos[1]-1)
            ck_2 = (pos[0]+1, pos[1]+1)

            check_2 = pos[1]-1#out of bound to the left
            check_3 = pos[1]+1#out of bound to the right


            if check_2<0:
                if check in black and ck_2 in black:
                    continue
                elif check in white and ck_2 in black:
                    continue
                elif check in black or check in white:
                    actions[pos]=[(pos[0]+1, pos[1]+1)]
                else:
                    actions[pos]=[(pos[0]+1, pos[1]),(pos[0]+1, pos[1]+1)]

            elif check_3>=len(state[0]):
                if check in black and ck in black:
                    continue
                elif check in white and ck in black:
                    continue
                elif check in black or check in white:
                    actions[pos]=[(pos[0]+1, pos[1]-1)]
                else:
                    actions[pos]=[(pos[0]+1, pos[1]),(pos[0]+1, pos[1]-1)]
            else:
                if check in black and ck in black and ck_2 in black:
                    continue
                elif check in white and ck in black and ck_2 in black:
                    continue
                elif ck in black and ck_2 in black:
                    actions[pos]=[(pos[0]+1, pos[1])]
                elif check in black and ck in black:
                    actions[pos]=[(pos[0]+1, pos[1]+1)]
                elif check in black and ck_2 in black:
                    actions[pos]=[(pos[0]+1, pos[1]-1)]
                elif check in white and ck in black:
                    actions[pos]=[(pos[0]+1, pos[1]+1)]
                elif check in white and ck_2 in black:
                    actions[pos]=[(pos[0]+1, pos[1]-1)]
                #check for two moves
                elif check in black:
                    actions[pos]=[(pos[0]+1, pos[1]-1),(pos[0]+1, pos[1]+1)]
                elif check in white:
                    actions[pos]=[(pos[0]+1, pos[1]-1),(pos[0]+1, pos[1]+1)]
                elif ck in black:
                    actions[pos]=[(pos[0]+1, pos[1]),(pos[0]+1, pos[1]+1)]
                elif ck_2 in black:
                    actions[pos]=[(pos[0]+1, pos[1]),(pos[0]+1, pos[1]-1)]
                else:
                    actions[pos]=[(pos[0]+1, pos[1]),(pos[0]+1, pos[1]-1),(pos[0]+1, pos[1]+1)]

    return actions

def transitional(state,piece,action):
    Board = copy.deepcopy(state[0])
    if Board[piece[0]][piece[1]] == 'X' and state[1] =='B':
        if action[0] == piece[0]+1:
            if action[1] == piece[1]-1 or action[1] == piece[1]+1 or action[1] == piece[1]:
                if  Board[action[0]][action[1]] == '.':
                    Board[action[0]][action[1]] = 'X'
                    Board[piece[0]][piece[1]] = '.'

                elif Board[action[0]][action[1]] == 'O':
                    Board[action[0]][action[1]] = 'X'
                    Board[piece[0]][piece[1]] = '.'

        new_state = State(Board,"W")
        return new_state

    elif Board[piece[0]][piece[1]] == 'O' and state[1] == 'W':
        if action[0] == piece[0]-1:
            if action[1] == piece[1]-1 or action[1] == piece[1]+1 or action[1] == piece[1]:
                if  Board[action[0]][action[1]] == '.':
                    Board[action[0]][action[1]] = 'O'
                    Board[piece[0]][piece[1]] = '.'
                elif Board[action[0]][action[1]] == 'X':
                    Board[action[0]][action[1]] = 'O'
                    Board[piece[0]][piece[1]] = '.'
        new_state = State(Board,"B")
        return new_state


class Node:
    def __init__(self,state):
        self.parent = None
        self.child = []
        self.action = None
        self.state = state
        self.utility = None
        self.depth = 0

    def get_parent(self):
        return self.parent
    def get_child(self):
        return self.child
    def get_action(self):
        return self.action
    def get_state(self):
        return self.state
    def get_utility(self):
        return self.utility
    def get_depth(self):
        return self.depth
    def set_parent(self,new_parent):
        self.parent = new_parent
    def set_action(self,new_action):
        self.action = new_action
    def set_depth(self,d):
        self.depth = d
    def set_child(self,list_kids):
        self.child=list_kids
    def set_utility(self, n):
        self.utility = n

Q = Queue()


def create_tree(state, depth, utility):
    curr_node = Node(state)
    Q.enqueue(curr_node)

    while Q.is_empty()==False:#game_ending(state)==False:
        curr_node = Q.dequeue()

        if curr_node.get_depth()==depth:
            if utility == "E":
                val = evasive_utility(curr_node.get_state())
                curr_node.set_utility(val)

                continue
            elif utility == "C":
                val = conqueror_utility(curr_node.get_state())
                curr_node.set_utility(val)

                continue
            elif utility == "K":
                val = karnage_utility(curr_node.get_state())
                curr_node.set_utility(val)

                continue
            elif utility == "F":
                val = fortification_utility(curr_node.get_state())
                curr_node.set_utility(val)

                continue
        possible_actions=move_generator(curr_node.get_state())
        if len(possible_actions)==0:
            continue
        all_keys = list(possible_actions.keys())
        child = []
        keys = 0

        while keys <len(all_keys):
            current_vals = list(possible_actions.values())
            n_kids = len(current_vals[keys])#how many kids are there for a specific key

            for i in range (n_kids):
                new_state = transitional(curr_node.get_state(),all_keys[keys],current_vals[keys][i])
                new_node = Node(new_state)#I need to feed a new state #the index of the children
                new_node.set_parent(curr_node)
                new_node.set_depth(curr_node.get_depth()+1)
                new_node.set_action(current_vals[keys][i])# new_node.set_action(node)
                child.append(new_node)#list comprehension
#                 print("new node_state",new_node.get_state())
                if new_node.get_state() != curr_node.get_state():
                    Q.enqueue(new_node)
            keys+=1
            # if len(child)!=0:
            curr_node.set_child(child)
    return curr_node#last children

def get_root(node):
    while node.get_parent()!=None:
        node = node.get_parent()
    return node#root node of populated tree


def get_leafs(node):
    stack  = []
    leafs = []
    stack.append(node)
    while len(stack)!=0:
        curr = stack.pop()
        if len(curr.get_child())==0:
            leafs.append(curr)
        else:
            list_of_kids = curr.get_child()
            for i in list_of_kids:
                stack.append(i)
    return leafs


#########################################################
def traverse_tree(root,maxplayer):

    if root.get_utility()!= None:
        return (root.get_utility(),root.get_state())

    if maxplayer == True:
        max_val = -100000000000000000
        max_child = root
        for child in root.get_child():
            util_val,util_child = traverse_tree(child,False)
            if max_val<util_val:
                max_val = util_val
                max_child = child
        root.set_utility(max_val)
        return (max_val, max_child.get_state())
    else:
        min_val = 100000000000000000
        min_child = root
        for child in root.get_child():
            util_val, util_child = traverse_tree(child,True)
            if util_val< min_val:
                min_val = util_val
                min_child = child
        root.set_utility(min_val)
        return (min_val, min_child.get_state())


def conqueror_utility(state):
    if state[1] == 'W':
        white  = white_pieces(state)
        x = (0 - len(white) + random.random())
    if state[1] == 'B':
        black = black_pieces(state)
        x = (0 - len(black) + random.random())
    return x

def evasive_utility(state):
    if state[1] == 'W':
        white  = white_pieces(state)
        x = len(white) + random.random()
    if state[1] == 'B':
        black = black_pieces(state)
        x = len(black) + random.random()
    return x


def fortification_utility(state):
    if state[1] == 'W':
        white  = white_pieces(state)
        utili = 0
        l=[]
        for i in white:
            l.append(i[0])
        top = white[l.index(min(l))]
        util=len(state[0])-top[0]

    if state[1] == 'B':
        black = black_pieces(state)
        utili = 0
        l=[]
        for i in black:
            l.append(i[0])
        top = black[l.index(min(l))]
        util=len(state[0])-top[0]
    return utili

def karnage_utility(state):
        white  = white_pieces(state)
        black = black_pieces(state)
        if state[1] == 'W':
            x = (len(state[0])-1) - len(white)-len(black)
        if state[1] == 'B':
            x = (len(state[0])-1) - len(black)-len(white)
        x = x+ random.random()
        return  x

def hurdle_utility(state):
    Board = state[0]
    number = [0,1]
    random_ = (random.choice(number))

    if state[1] == 'W':
        value = []
        white  = white_pieces(state)
        for i in white:
            value.append(len(Board)-i[0])
        return (max(value) + random_)

    if state[1] == 'B':
        value = []
        black = black_pieces(state)
        for i in black:
            value.append(len(Board)-i[0])
        return (max(value) + random_)


def play_game(heuristic_white, heuristic_black, board_state):

    new_state = board_state
    count = 0
    while game_ending(new_state) != True or new_state == None:
        count+=1
        if new_state[1] == 'W':
            tree = create_tree(new_state,3,heuristic_white)
            root = get_root(tree)
            val, child = traverse_tree(root,True)
            show = display_state(new_state)
            print(show)
            new_state = State (child[0],'B')

        elif new_state[1] == 'B':
            tree = create_tree(new_state,3,heuristic_black)
            root = get_root(tree)
            val, child = traverse_tree(root,True)
            show = display_state(new_state)
            print(show)
            new_state = State (child[0],'W')
    show = display_state(new_state)
    print(show)
    print("Moves before victory:",count)
    return new_state
def pieces_captured(initial_state, final_state):
    white_initial  = white_pieces(initial_state)
    white_final = white_pieces(final_state)
    black_taken = len(white_initial)-len(white_final)

    black_initial = black_pieces(initial_state)
    black_final = black_pieces(final_state)
    white_taken = len(black_initial)-len(black_final)

    return white_taken, black_taken

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process file.')#Create argument paser object
    parser.add_argument('R1',help='Number of rows for the board (8 recommended)')#Take utility for white
    parser.add_argument('C1',help='Number of columns for the board (8 recommended)')
    parser.add_argument('P1',help='rows of players(2 recommended)')
    parser.add_argument('U1',help='utility value to use choose from C,F,E,K')#Take utility for white
    parser.add_argument('U2',help='utility value to use choose from C,F,E,K')#Take utility for Black
    args = parser.parse_args()

    start = time.time()
    rows  = int(args.R1)
    columns = int(args.C1)
    player = int(args.P1)
    initial_state = initial_state(rows,columns,player)
    tree = create_tree(initial_state,2,args.U2)
    rt = get_root(tree)
    traverse = traverse_tree(rt,True)
    play = play_game(args.U1,args.U2,initial_state)
    display = display_state(play)
    captured_w, captured_b = pieces_captured(initial_state,play)
    print("Board Dimenssions: ", rows, "x", columns, ",",player)
    print("pieces captured by white:",captured_w)
    print("pieces captured by black:",captured_b)
    end = time.time()
    print("Time to run the program:",round(end-start,2),"sec")
