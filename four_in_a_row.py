import sys
import tkinter as tk
from game import Game
from communicator import Communicator
from ai import AI
from screen import Screen

ARG_ERROR = "Illegal program arguments."
ARG_PLAYERS = ['human', 'ai']
ARG_PORT_MAX = 65535
NUM_ARGS = 3


class FourInARow:

    PLAYERS = ARG_PLAYERS
    MSG_NOT_TURN = 'Not your turn!'
    MSG_DRAW = 'draw'
    MSG_WIN = 'winner!'
    MSG_LOSE = 'loser :('
    
    def __init__(self, root, player, port, ip):
        """
        :param player:
        :param port:
        :param ip:
        """
        self.__root = root

        if player == self.PLAYERS[1]:
            self.__is_ai = True
        else:
            self.__is_ai = False

        self.__game = Game()
        self.__game.new_board()

        if ip:
            self.__my_color = Game.PLAYER_TWO
            self.__op_color = Game.PLAYER_ONE

        else:
            self.__my_color = Game.PLAYER_ONE
            self.__op_color = Game.PLAYER_TWO

        self.__communicator = Communicator(root, port, ip)
        self.__communicator.connect()
        self.__communicator.bind_action_to_message(self.handle_message)

        if self.__is_ai:
            self.__screen = Screen(root, self.__my_color, lambda y: None)
            self.__ai = AI()
            if self.__my_color == Game.PLAYER_ONE:
                self.ai_find_move()
        else:
            self.__screen = Screen(root, self.__my_color, self.play_my_move)

    def ai_find_move(self):
        """
        :return:
        """
        sim_game = Game()
        board, register, cell_set, counter = self.__game.get_attr_for_sim()
        sim_game.set_attr_for_sim(board, register, cell_set, counter)

        self.__ai.find_legal_move(sim_game, self.play_my_move)

    def play_my_move(self, column):
        """
        :return:
        """
        self.one_turn(column, self.__my_color)
        self.__communicator.send_message(str(column))

    def one_turn(self, column, player):
        """
        :param column:
        :return:
        """
        if self.__game.get_current_player() == player:
            try:
                self.__game.make_move(column)
                row, col = self.__game.get_last_coord()

                if self.__is_ai:
                    self.__screen.update_cell(row, col, player, anim=False)
                else:
                    self.__screen.update_cell(row, col, player, anim=True)

            except:
                self.__screen.print_to_screen(self.__game.ILLEGAL_MOVE_MSG, player)
                return

        else:
            self.__screen.print_to_screen(self.MSG_NOT_TURN, player)
            return

        winner = self.__game.get_winner()
        if winner is not None:
            self.end_game(winner)

    def end_game(self, winner):
        """
        :return:
        """
        win_coord, win_dir = self.__game.get_win_info()
        self.__screen.win(win_coord, win_dir, winner)

        if winner == Game.DRAW:
            self.__screen.print_to_screen(self.MSG_DRAW, self.__my_color)
            self.__screen.print_to_screen(self.MSG_DRAW, self.__op_color)

        elif winner == self.__my_color:
            self.__screen.print_to_screen(self.MSG_WIN, self.__my_color)
            self.__screen.print_to_screen(self.MSG_LOSE, self.__op_color)

        elif winner == self.__op_color:
            self.__screen.print_to_screen(self.MSG_WIN, self.__op_color)
            self.__screen.print_to_screen(self.MSG_LOSE, self.__my_color)

    def handle_message(self, message=None):
        """
        Specifies the event handler for the message getting event in the
        communicator. Prints a message when invoked (and invoked by the
        communicator when a message is received).
        :param message: the text to be printed.
        :return: None.
        """
        if message:
            self.one_turn(int(message[0]), self.__op_color)
            if self.__is_ai:
                if self.__game.get_win_info()[1] is None:
                    self.ai_find_move()


def main(args):
    player = args[1]
    port = int(args[2])
    ip = None
    if len(args) > NUM_ARGS:
        ip = args[NUM_ARGS]

    root = tk.Tk()
    FourInARow(root, player, port, ip)
    root.mainloop()


if __name__ == "__main__":

    if not NUM_ARGS-1 < len(sys.argv) < NUM_ARGS+1:
        print(ARG_ERROR)
        sys.exit()
        
    if sys.argv[1] not in ARG_PLAYERS:
        print(ARG_ERROR)
        sys.exit()

    if int(sys.argv[2]) > ARG_PORT_MAX:
        print(ARG_ERROR)
        sys.exit()

    main(sys.argv)
