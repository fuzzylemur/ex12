from random import sample
from game import Game

class Node:

    def __init__(self, data=0,depth=0):
        self.__data = data
        self.__depth = depth
        self.__children = dict()

    def get_data(self):
        """"""
        return self.__data

    def get_children(self):
        return self.__children
        
    def get_depth(self):
        return self.__depth

    def set_data(self, n_data):
        self.__data += n_data

    def add_child(self, col, node):
        self.__children[col] = node
        
    def remove_child(self, col):
        if col in self.__children.keys():
            del self.__children[col]


class AI:

    DRAW = Game.DRAW
    #PLAYER_ONE = Game.PLAYER_ONE
    #PLAYER_TWO = Game.PLAYER_TWO

    def __init__(self, player):
        self.__player = player
        self.__cur_node = Node()
        self.__next_move = None

    def find_legal_move(self, g, func, timeout=None):
        """"""
        # Saves random move as our move 
        # and then improves it until the timeout
        legal_moves = self.find_legal_moves(g)
        self.__next_move = sample(legal_moves, 1)[0]

        try:
            last_col = g.get_last_coord()
            if last_col is not None and self.__cur_node.get_children() != dict():
                children = self.__cur_node.get_children()
                self.__cur_node = children[last_col[1]]
            # Build tree and improve current decision
            self.build_tree(g, self.__cur_node, legal_moves)

        finally:
            # Update the cur node and returns the best move we found so far
            self.__cur_node = self.__cur_node.get_children()[self.__next_move]
            
            func(self.__next_move)
            
    def find_legal_moves(self, g):
        """Finds all current possible moves and
        deletes illegal moves from the current_node
        children"""
        legal_moves = set()
        for move in range(7):
            if not g.is_col_full(move):
                legal_moves.add(move)
            else:
                self.__cur_node.remove_child(move)
                
        return legal_moves
        
    def set_next_best_move(self, children, legal_moves):
        """"""
        self.__next_move = max(children.keys(), key=lambda
                                    k: children[k].get_data())

    def build_tree(self, g, root, legal_moves):
        """"""
        for i in range(2000): # Can be while true / according to timeout
            self.build_branch(g, root, legal_moves)
            # Save the best choice every 20 branches
            if i % 20 == 0: # ask Gil about the exact number
                children = self.__cur_node.get_children()

                self.set_next_best_move(children, legal_moves)

    def build_branch(self, g, node, legal_moves):
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
            return node.get_data()

        else:
            chosen_col = sample(legal_moves, 1)[0]
            temp = g.get_last_coord()
            g.make_move(chosen_col)
            if g.is_col_full(chosen_col):
                legal_moves.remove(chosen_col)
                
            if chosen_col in node.get_children().keys():
                next_node = node.get_children()[chosen_col]
                result = self.build_branch(g, next_node, legal_moves)
                node.set_data(result/2)
            else:
                child = Node(0, node.get_depth()+1)
                node.add_child(chosen_col, child)
                result = self.build_branch(g, child, legal_moves)
                node.set_data(result/2)
            #Undo all changes
            g.unmake_move(chosen_col, temp)
            legal_moves.add(chosen_col)

        return result

if __name__ == "__main__":

    ai = AI(0)
    g = Game()
    root = Node()
    print(ai.find_legal_move(g,lambda x:x))