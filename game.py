
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
        self.__cell_set = None
        self.__counter = 0
        self.__last_coord = None
        self.__win = None

    def new_board(self):
        """
        :return:
        """
        self.__board = {}
        for row in range(self.BOARD_Y):
            for col in range(self.BOARD_X):
                self.__board[row, col] = self.EMPTY_CELL

        self.__cell_set = set(self.__board.keys())

    def make_move(self, column):
        """
        :param column:
        :return:
        """
        pl = self.get_current_player()
        if self.is_col_full(column) or self.__win:
            raise Exception(self.ILLEGAL_MOVE_MSG)

        for row in range(self.BOARD_Y-1, -1, -1):
            coord = row, column
            if self.__board[coord] == self.EMPTY_CELL:
                self.__board[coord] = self.get_current_player()
                self.__last_coord = coord
                
                break

        #print('made move on col '+str(column)+' last_coord: '+str(self.__last_coord)+' player: '+str(pl)+' counter: '+str(self.__counter))

    def is_col_full(self, column):
        """
        :param column:
        :return:
        """
        if self.__board[0, column] != self.EMPTY_CELL:
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
                if next_cell not in self.__cell_set:
                    break
                if self.__board[next_cell] != player:
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
                    print('_', end='')
                else:
                    print(self.__board[(i, j)], end='')
            print('\n')

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

    def get_last_coord(self):
        """
        :return:
        """
        return self.__last_coord

    def get_win_info(self):
        """
        :return:
        """
        return self.__last_coord, self.__win

    def get_board(self):
        """"""
        return self.__board

    def set_board(self, board):
        """"""
        self.__board = board

    def unmake_move(self, col, last_move):
        """"""
        for row in range(self.BOARD_X):
            coord = row, col
            if self.__board[coord] != self.EMPTY_CELL:
                self.__board[coord] = self.EMPTY_CELL
                self.__last_coord = last_move
                self.__counter -= 1
                break
    
    def set_game_on(self):
        """"""
        self.__win = None

    def get_counter(self):
        """"""
        return self.__counter

    def set_counter(self, value):
        """"""
        self.__counter = value

    def counter_plus_1(self):
        """"""
        self.__counter += 1
        
    def get_cell_set(self):
        """"""
        return self.__cell_set

    def set_cell_set(self, set):
        """"""
        self.__cell_set = set