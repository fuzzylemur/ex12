from random import choice
from copy import deepcopy
from game import Game

class Node:
    
    def __init__(self, data=None,depth=0):
        self.__data = data
        self.__depth = depth
        self.__children = dict()

    def get_data(self):
        return self.__data
    
    def get_depth(self):
        return self__depth

    def set_data(self, n_data):
        self.__data += n_data

    def add_child(self, col, node):
        self.__children[col] = node
        
        
class AI:

    DRAW = Game.DRAW
    #PLAYER_ONE = Game.PLAYER_ONE
    #PLAYER_TWO = Game.PLAYER_TWO


    def __init__(self, g, player):
        #self.__game = g
        self.__player = player

    def find_legal_move(self, g, func, timeout=None):
        legal_moves = set([move for move in range(7) if not g.is_col_full(move)])

    def build_tree(self, g):
        """"""
        root = Node()
        while True:
            build_branch(g, root, legal_moves, depth)

    def build_branch(self, g, node, legal_moves, depth):
        """"""
        winner = self.get_winner()
        if winner is not None:

            if winner == self.__player:
                node.set_data(1) 
            elif winner == self.DRAW:
                node.set_data(0)
            else:
                node.set_data(-1)
                
            return node.get_data
        else:
            chosen_col = choice(legal_moves)

            temp = g.get_coord()
            g.make_move(chosen_col)
            if g.is_col_full(chosen_col):
                legal_moves.remove(chosen_col)

            if chosen_col in node.children.keys():
                node.set_data(build_branch(g, node, legal_moves, depth+1))
            else:
                child = Node(None, node.get_depth()+1)
                n_node.add_child(chosen_col, child)
                child.set_data(build_branch(g, child, legal_moves, depth+1))
            #Undo all changes
            g.unmake_move(chosen_col, temp)
            legal_moves.add(chosen_col)
