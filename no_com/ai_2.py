from random import sample, seed
from copy import deepcopy
from game import Game
#import time

class Node:

    def __init__(self, data=0,depth=0):
        self.__data = data
        self.__depth = depth
        self.__children = dict()

    def get_data(self):
        return self.__data

    def get_children(self):
        return self.__children
        
    def get_depth(self):
        return self.__depth

    def set_data(self, n_data):
        self.__data += n_data

    def add_child(self, col, node):
        self.__children[col] = node

class AI:

    DRAW = Game.DRAW
    ITER = 5000
    #PLAYER_ONE = Game.PLAYER_ONE
    #PLAYER_TWO = Game.PLAYER_TWO

    def __init__(self, player):
        self.__player = player
        self.__cur_node = Node()
        self.__next_move = None
        self.__moves = set([0,1,2,3,4,5,6])
        self.histo = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0}

    def find_legal_move(self, g, func, timeout=None):
        """"""
        #timer = time.time()
        # Saves random move as our move 
        # and then improves it until the timeout

        self.__next_move = sample(self.__moves, 1)[0]

        try:
            last_col = g.get_last_coord()
            if last_col is not None and self.__cur_node.get_children() != dict():
                children = self.__cur_node.get_children()
                self.__cur_node = children[last_col[1]]
            # Build tree and improve current decision
            self.build_tree(g, self.__cur_node, 0)

        finally:
            # Update the cur node and returns the best move we found so far
            self.__cur_node = self.__cur_node.get_children()[self.__next_move]
            print('move is '+str(self.__next_move))
            func(self.__next_move)
    
    def set_next_best_move(self, children):
        """"""
        self.__next_move = max(children.keys(), key=lambda
                                    k: children[k].get_data())

    def build_tree(self, g, root, depth):
        """"""
        for i in range(self.ITER): # Can be while true / according to timeout
            self.build_branch(g, root, self.__moves, depth)
            # Save the best choice every 20 branches
            if i % 20 == 0: # ask Gil about the exact number
                children = self.__cur_node.get_children()
                self.set_next_best_move(children)

        for ind, child in root.get_children().items():
            print('index: '+str(ind)+'   score: '+str(child.get_data()))
        print(self.histo)

    def build_branch(self, g, node, legal_moves, depth):
        """"""
        winner = g.get_winner()
        if winner is not None:

            if winner == self.__player:
                node.set_data(1)
            elif winner == self.DRAW:
                node.set_data(0)
            else:
                node.set_data(-1)
                
            g.set_game_on()
            print('******************************')
            return node.get_data()
        else:
            chosen_col = sample(legal_moves, 1)[0]
            self.histo[chosen_col] += 1
            temp = g.get_last_coord()
            if not g.is_col_full(chosen_col):
                g.make_move(chosen_col)
            else:
                return 0

            if chosen_col in node.get_children().keys():
                next_node = node.get_children()[chosen_col]
                result = self.build_branch(g, next_node, legal_moves, node.get_depth()+1)
                node.set_data(result)

            else:
                child = Node(0, depth=depth+1)
                node.add_child(chosen_col, child)
                result = self.build_branch(g, child, legal_moves, node.get_depth()+1)
                node.set_data(result)
            #Undo all changes
            g.unmake_move(chosen_col, temp)

        #print('depth: '+str(node.get_depth())+'  data: '+str(node.get_data()))
        return result/2
    
    def get_next_move(self):
        """"""
        return self.__next_move
        
if __name__ == "__main__":

    ai = AI(0)
    g = Game()
    g.new_board()
    g.sim()
    root = Node()
    ai.find_legal_move(g,lambda x:x)