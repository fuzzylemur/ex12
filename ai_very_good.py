from random import sample
from copy import deepcopy
from game2 import Game

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
    #PLAYER_ONE = Game.PLAYER_ONE
    #PLAYER_TWO = Game.PLAYER_TWO


    def __init__(self, player):
        #self.__game = g
        self.__player = player

    def find_legal_move(self, g, func, timeout=None):
        legal_moves = set([move for move in range(7) if not g.is_col_full(move)])
        
    def build_tree(self, g, root):
        """"""
        legal_moves = set([move for move in range(7) if not g.is_col_full(move)])
        for i in range(3000):
            self.build_branch(g, root, legal_moves, root.get_depth())
        for child, score in root.get_children().items():
            print(child, score.get_data())
            
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
                
            return node.get_data()
        else:
            chosen_col = sample(legal_moves, 1)[0]
            temp = g.get_coord()
            g.make_move(chosen_col)
            if g.is_col_full(chosen_col):
                legal_moves.remove(chosen_col)

            if chosen_col in node.get_children().keys():
                next_node = node.get_children()[chosen_col]
                result = self.build_branch(g, next_node, legal_moves, node.get_depth() + 1)
                node.set_data(result)
            else:
                child = Node(0, node.get_depth()+1)
                node.add_child(chosen_col, child)
                result = self.build_branch(g, child, legal_moves, node.get_depth()+1)
                node.set_data(result)
            #Undo all changes
            g.unmake_move(chosen_col, temp)
            legal_moves.add(chosen_col)

        return result

ai = AI(0)
g = Game()
root = Node()
ai.build_tree(g, root)