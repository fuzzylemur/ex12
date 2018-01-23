
class Game:

    EMPTY_CELL = None
    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2

    BOARD_X = 7
    BOARD_Y = 6
    WIN_LEN = 4
    ILLEGAL_MOVE_MSG = 'Illegal move'

    DIRECTIONS = [[-1,1],[0,1],[1,1],[1,0],[-1,-1],[0,-1],[1,-1],[-1,0]]       # removed UP direction. problems?

    def __init__(self):
        """

        """
        self.__board = {}
        self.__register = {}
        self.__cell_set = None
        self.__counter = 0
        self.__last_coord = None
        self.__win = None

    def new_board(self):
        """
        :return:
        """
        for col in range(self.BOARD_X):
            self.__register[col] = self.BOARD_Y-1
            for row in range(self.BOARD_Y):
                self.__board[row, col] = self.EMPTY_CELL

        self.__cell_set = set(self.__board.keys())

    def make_move(self, column):
        """
        :param column:
        :return:
        """
        row = self.__register[column]

        if row == -1 or self.__win:
            raise Exception(self.ILLEGAL_MOVE_MSG)

        coord = row, column
        if self.__board[coord] == self.EMPTY_CELL:
            self.__board[coord] = self.get_current_player()
            self.__last_coord = coord
            self.__counter += 1
            self.__register[column] -= 1


    def unmake_move(self, col, last_move):
        """
        :param col:
        :param last_move:
        :return:
        """
        for row in range(self.BOARD_Y):
            coord = row, col
            if self.__board[coord] != self.EMPTY_CELL:
                self.__board[coord] = self.EMPTY_CELL
                self.__last_coord = last_move
                self.__counter -= 1
                break

    def get_player_at(self, row, col):
        """
        :param row:
        :param col:
        :return:
        """
        return self.__board[row, col]

    def get_current_player(self):
        """
        :return:
        """
        if self.__counter % 2 == 0:
            return self.PLAYER_ONE
        else:
            return self.PLAYER_TWO

    def is_col_full(self, column):
        """
        :param column:
        :return:
        """
        if self.__register[column] == -1:
            return True
        else:
            return False

    def get_winner(self):
        """
        :return:
        """
        if self.__last_coord is None:
            return None

        row, col = self.__last_coord
        player = self.get_player_at(row, col)

        for direction in self.DIRECTIONS:

            for i in range(1, self.WIN_LEN):
                next_cell = (row+i*direction[0], col+i*direction[1])
                if next_cell not in self.__cell_set or self.__board[next_cell] != player:
                    if i == 3:
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

    def set_game_on(self):
        """"""
        self.__win = None

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

    def sim(self):
        self.__board[5,2] = 0
        self.__board[5,3] = 0
        self.__board[5,4] = 0
        self.__counter = 4