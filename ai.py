from random import sample
from game import Game


class Node:

    def __init__(self, score=0):
        self.__score = score
        self.__children = dict()

    def get_score(self):
        """"""
        return self.__score

    def get_children(self):
        return self.__children

    def add_score(self, n_score):
        self.__score += n_score

    def add_child(self, col, node):
        self.__children[col] = node
        
    def remove_child(self, col):
        if col in self.__children.keys():
            del self.__children[col]


class AI:

    DRAW = Game.DRAW
    ITERATIONS = 1000
    UPDATE_INTERVAL = 20
    FALLOFF_VALUE = 2
    SCORES = (1, 0, -1)     # (win, draw, lose)

    def __init__(self):
        self.__my_color = None
        self.__op_color = None
        self.__cur_node = Node()
        self.__next_move = None
        self.__first_time = True

    def find_legal_move(self, g, func, timeout=None):
        """
        :param g:
        :param func:
        :param timeout:
        :return:
        """
        if self.__first_time:                                   # when running the function for the first time
            self.__my_color = g.get_current_player()            # register player colors inside AI object
            if self.__my_color == g.PLAYER_ONE:
                self.__op_color = g.PLAYER_TWO
            else:
                self.__op_color = g.PLAYER_ONE
            self.__first_time = False

        possible_moves = self.possible_moves(g)                 # find possible moves (col is not full)
        self.__next_move = sample(possible_moves, 1)[0]         # and pick one randomly as a default

        try:
            last_col = g.get_last_coord()                       # see what was the last move played
            if last_col is not None:                                    # if not the first move and
                if self.__cur_node.get_children() != dict():            # current node not empty
                    children = self.__cur_node.get_children()
                    self.__cur_node = children[last_col[1]]             # update current node accordingly

            self.build_tree(g, self.__cur_node)                         # and build a tree from that node

        finally:                                                                    # when function is halted

            self.__cur_node = self.__cur_node.get_children()[self.__next_move]      # update cur node to best move
            func(self.__next_move)                                                  # and call func with that move

            print('*********** move number ', g.get_counter(), '***********')
            print('register: ', g.get_register())
            for i, node in self.__cur_node.get_children().items():
                print('col: ', i, '  score: ', node.get_score())

    def build_tree(self, g, root):
        """
        :param g:
        :param root:
        :return:
        """
        for i in range(self.ITERATIONS):                    # build branches in iteratively
            self.build_branch(g, root)

            if i % self.UPDATE_INTERVAL == 0:               # update best move every now and then
                children = self.__cur_node.get_children()
                self.set_next_best_move(children)

    def build_branch(self, g, node):
        """
        :param g:
        :param node:
        :return:
        """
        winner = g.get_winner()
        if winner is not None:                   # base case of recursion, simulated game has ended
                                                    # give the leaf a score based on end result
            if winner == self.__my_color:
                score = self.SCORES[0]
            elif winner == self.DRAW:
                score = self.SCORES[1]
            elif winner == self.__op_color:
                score = self.SCORES[2]

            g.set_game_on()                         # turn game object back on (getting a winner has turned it off)
            node.add_score(score)                   # add score to node
            return score                            # and return the score upwards in the recursion

        else:                                    # else simulated game is still on

            new_moves = self.possible_moves(g)      # find possible moves from current node
            for col in list(node.get_children().keys())[:]:
                if col not in new_moves:
                    node.remove_child(col)          # and remove children for illegal moves (col is full)

            chosen_col = sample(new_moves, 1)[0]    # pick the next move randomly
            temp_coord = g.get_last_coord()         # record the last move made (for undoing when backtracking)
            g.make_move(chosen_col)                 # and make that move

            if chosen_col in node.get_children().keys():            # if node already has a child for that move
                next_node = node.get_children()[chosen_col]                  # go to that child node
                child_score = self.build_branch(g, next_node)     # continue building the branch from it
                node.add_score(child_score)                                  # and update the node score

            else:                                                   # if child for this move does not exist
                child = Node(0)                                              # create a node for it
                node.add_child(chosen_col, child)                            # link it to parent node
                child_score = self.build_branch(g, child)         # continue building the branch from it
                node.add_score(child_score)                                  # and update the node score

            g.unmake_move(chosen_col, temp_coord)                 # when exiting recursion undo the move made

        return child_score/self.FALLOFF_VALUE           # return the result from recursion divided by two
                                                        # so that results closer to tree root will have more weight
    def possible_moves(self, g):
        """
        Finds all current possible moves (column not full)
        :param g:
        :return:
        """
        possible_moves = set()
        for column in range(Game.BOARD_X):
            if not g.is_col_full(column):
                possible_moves.add(column)

        return possible_moves

    def set_next_best_move(self, children):
        """
        :param children:
        :return:
        """
        self.__next_move = max(children.keys(), key=lambda k: children[k].get_score())


if __name__ == "__main__":

    ai = AI()
    g1 = Game()

    ai.find_legal_move(g1,lambda x:x)