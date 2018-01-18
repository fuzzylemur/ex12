
class Game:

    EMPTY_CELL = None
    PLAYER_ONE = 0
    PLAYER_TWO = 1
    WIN_ONE = str(PLAYER_ONE)*4
    WIN_TWO = str(PLAYER_TWO)*4
    DRAW = 2
    BOARD_X = 7
    BOARD_Y = 6
    ILLEGAL_MOVE_MSG = 'Illegal move'

    DIRECTIONS = [[-1,1],[0,1],[1,1],[1,0],[-1,-1],[0,-1],[1,-1],[-1,0]]

    def __init__(self):
        """

        """
        self.__board = {}
        for row in range(self.BOARD_Y):
            for col in range(self.BOARD_X):
                self.__board[row,col] = self.EMPTY_CELL

        self.__counter = 0
        self.__game_on = 1
        self.__last_coord = None
        self.__win_direction = None

    def make_move(self, column):
        """
        :param column:
        :return:
        """
        if column < 0 or column > 6 or self.is_col_full(column) or not self.__game_on:
            raise Exception(self.ILLEGAL_MOVE_MSG)

        for row in range(self.BOARD_Y-1, -1, -1):
            coord = row, column
            if self.__board[coord] == self.EMPTY_CELL:
                self.__board[coord] = self.get_current_player()
                self.__last_coord = coord
                self.__counter += 1
                break

        #self.print_board()

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
            for i in range(1,4):
                next_cell = (row+i*direction[0], col+i*direction[1])
                if next_cell not in self.__board.keys():
                    break
                if self.__board[next_cell] != player:
                    break

            else:
                self.__game_on = 0
                self.__win_direction = direction
                return player

        if self.__counter == self.BOARD_X*self.BOARD_Y:
            self.__game_on = 0
            return self.DRAW

    def print_board(self):
        for row in self.__board:
            print(row, '\n')
        print('*  '*20)

    def get_player_at(self, row, col):
        """
        :param row:
        :param col:
        :return:
        """
        return self.__board[row,col]

    def get_current_player(self):
        """
        :return:
        """
        if self.__counter % 2 == 0:
            return self.PLAYER_ONE
        else:
            return self.PLAYER_TWO

    def get_coord(self):
        """
        :return:
        """
        return self.__last_coord

    def get_win_info(self):
        """
        :return:
        """
        return self.__last_coord, self.__win_direction