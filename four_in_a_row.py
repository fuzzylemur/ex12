import sys
from game import Game
from communicator import Communicator
from ai import AI
from screen import Screen
import tkinter as tk
from time import sleep

ARG_ERROR = "Illegal program arguments."
ARG_PLAYERS = ['human', 'ai']
ARG_PORT_MAX = 65535


class FourInARow:

    NOT_YOUR_TURN_MSG = 'Not your turn!'
    
    def __init__(self, root, player, port, ip):
        """
        :param player:
        :param port:
        :param ip:
        """
        self.__game = Game()
        self.__game.new_board() #Can't the game init the board?

        self.__screen = Screen(root, self.play_my_move)
        self.__player = player
        
        if ip:
            self.__my_color = Game.PLAYER_TWO
            self.__op_color = Game.PLAYER_ONE

        else:
            self.__my_color = Game.PLAYER_ONE
            self.__op_color = Game.PLAYER_TWO

        self.__communicator = Communicator(root, port, ip)
        self.__communicator.connect()
        self.__communicator.bind_action_to_message(self.handle_message)

        if self.__player == ARG_PLAYERS[1]:
            self.__ai = AI(self.__my_color)
            if self.__my_color == Game.PLAYER_ONE:
                self.ai_find_move()

    def ai_find_move(self):
        """
        :return:
        """
        sim_game = Game()
        sim_game.set_board(self.__game.get_board())
        sim_game.set_counter(self.__game.get_counter())
        sim_game.set_cell_set(self.__game.get_cell_set())          #copy deepcopy?

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
                self.__screen.update_cell(row, col, player)

            except:
                self.__screen.print_to_gui(self.__game.ILLEGAL_MOVE_MSG)
        else:
            self.__screen.print_to_gui(self.NOT_YOUR_TURN_MSG)
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

        if winner == 2:
            self.__screen.print_to_gui('Draw')
        else:
            self.__screen.print_to_gui('winner is '+str(winner))

    def handle_message(self, text=None):
        """
        Specifies the event handler for the message getting event in the
        communicator. Prints a message when invoked (and invoked by the
        communicator when a message is received).
        :param text: the text to be printed.
        :return: None.
        """
        if text:
            self.one_turn(int(text[0]), self.__op_color)
            if self.__player == ARG_PLAYERS[1]:
                if self.__game.get_win_info()[1] is None:
                    self.ai_find_move()

def main(args):
    player = args[1]
    port = int(args[2])
    ip = None
    if len(args) > 3:
        ip = args[3]

    root = tk.Tk()
    FourInARow(root, player, port, ip)
    root.mainloop()

if __name__ == "__main__":

    if not 2 < len(sys.argv) < 5:
        print(ARG_ERROR)
        sys.exit()
        
    if sys.argv[1] not in ARG_PLAYERS:
        print(ARG_ERROR)
        sys.exit()

    if int(sys.argv[2]) > ARG_PORT_MAX:
        print(ARG_ERROR)
        sys.exit()

    main(sys.argv)
