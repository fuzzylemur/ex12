###################################################################################
# FILE : ai.py
# WRITERS : Gil Adam, Jonathan Zedaka, giladam, jonathanzd,  200139814, 204620835
# EXERCISE : intro2cs ex12 2017-2018
# DESCRIPTION: AI class for four in a row game
###################################################################################

from random import sample
from game import Game


class Node:
    """
    A simple node Object which includes a score value
    and a dictionary of children where key=column, value=node
    The constructor receives a score(float) value when called.
    Default value for score is 0.
    """

    def __init__(self, score=0):
        """
        The function initialize all node's private values.
        It receives a score and returns nothing
        """
        self.__score = score
        self.__children = dict()

    def get_score(self):
        """
        The function returns the node's score
        """
        return self.__score

    def get_children(self):
        """
        The function returns the node's dict of children
        """
        return self.__children

    def add_score(self, n_score):
        """
        The function receives a n_score value and adds it
        to the current node's score
        """
        self.__score += n_score

    def add_child(self, col, node):
        """
        The function receives a col(int) and a node object
        and adds a child to the node's dictionary of children {[col]: node}
        """
        self.__children[col] = node

    def remove_child(self, col):
        """
        The function receives a column (int) and removes the child in
        the key of the given col from the self.__children dict
        """
        if col in self.__children.keys():
            del self.__children[col]


class AI:
    """
    AI object is responsible for deciding on game moves when 
    game instance is defined to be AI. A move is done by AI when
    the method find_legal_move(game, function) is called, given a Game
    object and a function to be called with the move chosen by the algorithm.
    """

    DRAW = Game.DRAW
    ITERATIONS = 3000
    UPDATE_INTERVAL = 100
    FALLOFF_VALUE = 2
    SCORES = (1, 0, -1)  # (win, draw, lose)
    NO_AI_MOVE = 'No possible AI moves.'

    def __init__(self):
        """
        The function initialize all AI's private values.
        It receives nothing and returns nothing
        """
        self.__cur_node = Node()
        self.__my_color = None
        self.__op_color = None
        self.__next_move = None
        self.__first_time = True

    def find_legal_move(self, g, func, timeout=None):
        """
        The function looks fot the optimal legal ai move
        until the timeout.
        :param g: A simulated game object, identical to the real game.
        :param func: A function which eventually makes the move in the game.
        :param timeout: A time variable (in seconds) which limits the function
        run time.
        :return: None
        """
        if self.__first_time:                           # when running the function for the first time
            self.__my_color = g.get_current_player()    # register player colors inside AI object
            if self.__my_color == g.PLAYER_ONE:
                self.__op_color = g.PLAYER_TWO
            else:
                self.__op_color = g.PLAYER_ONE
            self.__first_time = False

        possible_moves = self.possible_moves(g)             # find possible moves (col is not full)
        self.__next_move = sample(possible_moves, 1)[0]     # and pick one randomly as a default

        if len(possible_moves) == 0:
            raise Exception(self.NO_AI_MOVE)

        try:

            last_col = g.get_last_coord()                   # see what was the last move played
            if last_col is not None:                            # if not the first move and
                if self.__cur_node.get_children() != dict():    # current node not empty
                    children = self.__cur_node.get_children()
                    self.__cur_node = children[last_col[1]]     # update current node accordingly

            self.build_tree(g, self.__cur_node)             # and build a tree from that node

        finally:                                # when function is halted

            self.__cur_node = self.__cur_node.get_children()[self.__next_move]  # update cur node to best move
            func(self.__next_move)                                              # and call func with that move

    def build_tree(self, g, root):
        """
        The function uses the 'helper' func build_branch to build a decision tree
        in order to find the optimal move for find_legal_move.
        The function saves the best move it finds every UPDATE_INTERVAL iterations.
        :param g: A simulated game object, identical to the real game.
        :param root: A certain tree node to start building the tree from.
        :return: None
        """
        for i in range(self.ITERATIONS):                    # build branches in iteratively
            self.build_branch(g, root)

            if i % self.UPDATE_INTERVAL == 0:               # update best move every now and then
                children = self.__cur_node.get_children()
                self.set_next_best_move(children)

    def build_branch(self, g, node):
        """
        A recursive function which build one tree branch for each call.
        The function recursively calls itself until it reaches a leaf
        (A situation of win/loss/draw)
        :param g: A simulated game object, identical to the real game.
        :param node: A node object to build the branch from.
        :return: Base case: The given node score
                 Otherwise: The result from the base case divided by the FALLOFF_VALUE
        """
        winner = g.get_winner()
        if winner is not None:              # base case of recursion, simulated game has ended
                                            # give the leaf a score based on end result
            if winner == self.__my_color:
                score = self.SCORES[0]
            elif winner == self.DRAW:
                score = self.SCORES[1]
            elif winner == self.__op_color:
                score = self.SCORES[2]

            g.set_game_on()                 # turn game object back on (getting a winner has turned it off)
            node.add_score(score)           # add score to node
            return score                    # and return the score upwards in the recursion

        else:                           # else simulated game is still on

            new_moves = self.possible_moves(g)                  # find possible moves from current node
            for col in list(node.get_children().keys())[:]:
                if col not in new_moves:
                    node.remove_child(col)                      # and remove children for illegal moves (col is full)

            chosen_col = sample(new_moves, 1)[0]           # pick the next move randomly
            temp_coord = g.get_last_coord()                # record the last move made (for undoing when backtracking)
            g.make_move(chosen_col)                        # and make that move

            if chosen_col in node.get_children().keys():        # if node already has a child for that move
                next_node = node.get_children()[chosen_col]
                child_score = self.build_branch(g, next_node)
                node.add_score(child_score)

            else:                                               # if child for this move does not exist
                child = Node(0)
                node.add_child(chosen_col, child)
                child_score = self.build_branch(g, child)
                node.add_score(child_score)

            g.unmake_move(chosen_col, temp_coord)               # when exiting recursion undo the move made

        return child_score / self.FALLOFF_VALUE         # return the result from recursion divided by two
                                                        # so that results closer to tree root will have more weight

    def possible_moves(self, g):
        """
        Finds all current possible moves (where the column is not full)
        :param g: A simulated game object, identical to the real game.
        :return: A set of legal moves.
        """
        possible_moves = set()
        for column in range(Game.BOARD_X):
            if not g.is_col_full(column):
                possible_moves.add(column)

        return possible_moves

    def set_next_best_move(self, children):
        """
        The function chose the child with the highest score and
        set its key(column) as self.__next_move
        :param children: A dictionary of children (key=column, value=node) 
        :return: None
        """
        self.__next_move = max(children.keys(), key=lambda k: children[k].get_score())
