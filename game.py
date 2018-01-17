
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

    DIRECTIONS = [[-1,1],[0,1],[1,1],[1,0]]

    def __init__(self):
        """

        """
        self.__board = []
        for row in range(self.BOARD_Y):
            temp_row = []
            for col in range(self.BOARD_X):
                temp_row.append(self.EMPTY_CELL)
            self.__board.append(temp_row)

        self.__counter = 0
        self.__game_on = 1

    def make_move(self, column):
        """
        :param column:
        :return:
        """
        if column < 0 or column > 6 or self.is_col_full(column) or not self.__game_on:
            raise Exception(self.ILLEGAL_MOVE_MSG)

        for row in range(self.BOARD_Y-1, -1, -1):
            if self.__board[row][column] == self.EMPTY_CELL:
                self.__board[row][column] = self.get_current_player()
                self.__counter += 1
                return row, column

        #self.print_board()

    def is_col_full(self, column):
        """
        :param column:
        :return:
        """
        if self.__board[0][column] != self.EMPTY_CELL:
            return True
        else:
            return False

    def get_winner(self):                           #TODO make it check from bottom up
        """
        :return:
        """
        for i, row in enumerate(self.__board):
            for j, cell in enumerate(row):
                if cell == self.EMPTY_CELL:
                    continue
                cell_color = cell
                for direction in self.DIRECTIONS:
                    for k in range(1,4):
                        next_cell = (i+k*direction[0], j+k*direction[1])
                        if next_cell[0] not in range(0, self.BOARD_Y) or next_cell[1] not in range(0, self.BOARD_X):
                            break

                        if self.__board[next_cell[0]][next_cell[1]] != cell_color:
                            break
                    else:
                        self.__game_on = 0
                        return cell_color, (i,j), direction           #TODO check returns

        if self.__counter == self.BOARD_X*self.BOARD_Y:
            self.__game_on = 0
            return self.DRAW, (0,0), (0,0)                  #TODO this is ugly

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
        return self.__board[row][col]

    def get_current_player(self):
        """
        :return:
        """
        if self.__counter % 2 == 0:
            return self.PLAYER_ONE
        else:
            return self.PLAYER_TWO

    def get_board(self):
        """
        :return:
        """
        return self.__board
