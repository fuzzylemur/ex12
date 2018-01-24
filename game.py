
class Game:
    """
    Object of class Game represents the game board, handles current game state, makes moves on the board and
    checks for game end conditions.
    """
    EMPTY_CELL = None
    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2

    BOARD_X = 7
    BOARD_Y = 6
    WIN_LEN = 4
    ILLEGAL_MOVE_MSG = 'Illegal move'

    DIRECTIONS = [[-1,1],[0,1],[1,1],[1,0],[-1,-1],[0,-1],[1,-1],[-1,0]]    # [row change, column change]

    def __init__(self):
        """
        Initialize a new Game object, with proper attributes in starting state.
        """
        self.__board = {}               # dictionary of board cells {(row, col): EMPTY_CELL/PLAYER_ONE/PLAYER_TWO}
        self.__register = {}            # dictionary of next available row in each column {column: row}
        self.__cell_set = None          # set of all cell coordinates ((x,y),...)
        self.__counter = 0              # turn counter
        self.__last_coord = None        # last coordinate played
        self.__win = None               # None if game is on, DRAW if draw, win sequence direction [row,col] if win

        for col in range(self.BOARD_X):                     # initialize start values for board, register, cell_set
            self.__register[col] = self.BOARD_Y-1
            for row in range(self.BOARD_Y):
                self.__board[row, col] = self.EMPTY_CELL

        self.__cell_set = set(self.__board.keys())

    def get_player_at(self, row, col):
        """
        Get player at a certain board coordinate
        :param row: row in board (0 <= int <= 5)
        :param col: column in board (0 <= int <= 6)
        :return: EMPTY_CELL / PLAYER_ONE / PLAYER_TWO
        """
        return self.__board[row, col]

    def get_current_player(self):
        """
        Find out who's turn it is.
        :return: PLAYER_ONE / PLAYER_TWO
        """
        if self.__counter % 2 == 0:
            return self.PLAYER_ONE
        else:
            return self.PLAYER_TWO

    def is_col_full(self, column):
        """
        Find out if a column is full
        :param column: the column to check (0 <= int <= 6)
        :return: True if full, False if not
        """
        if self.__register[column] == -1:
            return True
        else:
            return False

    def make_move(self, column):
        """
        Put a playing stone for current player in the given column.
        Raise exception if move is illegal (full column or game ended).
        :param column: the column to play (0 <= int <= 6)
        :return: None
        """
        row = self.__register[column]

        if row == -1 or self.__win:
            raise Exception(self.ILLEGAL_MOVE_MSG)

        coord = row, column
        self.__board[coord] = self.get_current_player()
        self.__last_coord = coord
        self.__counter += 1
        self.__register[column] -= 1

    def unmake_move(self, column, last_move):
        """
        Unmake a move on the board, given a column and the coordinate of the move made before that move,
        (to keep object attr last_coord updated). Used for example do undo moves done by a backtracking recursion.
        :param column: the column to undo (0 <= int <= 6)
        :param last_move: coordinate of the previous previous move (row, col)
        :return: None
        """
        row = self.__register[column]+1
        coord = row, column

        self.__board[coord] = self.EMPTY_CELL
        self.__last_coord = last_move
        self.__counter -= 1
        self.__register[column] += 1

    def get_winner(self):
        """
        Check to see if game has ended (win or a draw).
        :return: const DRAW if draw, const PLAYER_ONE/PLAYER_TWO if win
        """
        if self.__last_coord is None:               # no stones on board
            return None

        row, col = self.__last_coord                # look at last move played
        player = self.get_player_at(row, col)

        for direction in self.DIRECTIONS:           # and in all directions

            for i in range(1, self.WIN_LEN):
                next_cell = (row+i*direction[0], col+i*direction[1])
                if next_cell not in self.__cell_set or self.__board[next_cell] != player:
                    if i == self.WIN_LEN-1:
                        reverse_cell = (row - direction[0], col - direction[1])
                        if reverse_cell not in self.__cell_set or self.__board[reverse_cell] != player:
                            break
                        else:
                            self.__last_coord = reverse_cell
                    else:
                        break

            else:
                self.__win = direction
                return player

        if self.__counter == self.BOARD_X*self.BOARD_Y:
            self.__win = self.DRAW
            return self.DRAW

    def get_attr_for_sim(self):
        """
        :return:
        """
        return self.__board, self.__register, self.__cell_set, self.__counter

    def set_attr_for_sim(self, board, register, cell_set, counter):
        """
        :param board:
        :param register:
        :param cell_set:
        :param counter:
        :return:
        """
        self.__board = board
        self.__register = register
        self.__cell_set = cell_set
        self.__counter = counter

    def print_board(self):
        """"""
        for i in range(6):
            for j in range(7):
                if self.__board[(i, j)] is None:
                    print('_', end=' ')
                else:
                    print(self.__board[(i, j)], end=' ')
            print('\n')
        print('********************************************')

    def get_win_info(self):
        """
        :return:
        """
        return self.__last_coord, self.__win

    def get_last_coord(self):
        """
        :return:
        """
        return self.__last_coord

    def get_counter(self):
        """
        :return:
        """
        return self.__counter

    def get_register(self):
        """
        :return:
        """
        return self.__register

    def set_game_on(self):
        """"""
        self.__win = None
