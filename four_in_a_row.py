import sys
from copy import deepcopy
from game import Game
from communicator import Communicator
from ai import AI
from screen import Screen
import tkinter as tk

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
        self.__screen = Screen(root, self.one_turn)
        self.__player = player
        
        if ip:
            self.__color = Game.PLAYER_TWO
        else:
            self.__color = Game.PLAYER_ONE
         
        self.__communicator = Communicator(root, port, ip)
        self.__communicator.connect()
        self.__communicator.bind_action_to_message(self.handle_message)

        if self.__player == ARG_PLAYERS[1]:
            self.__ai = AI(self.__color)
            self.__ai_next_move = None
            if self.__color == Game.PLAYER_ONE:
                self.ai_turn()

    def ai_turn(self):
        """
        :return:
        """
        cur_board = deepcopy(self.__game.get_board())

        self.__ai.find_legal_move(self.__game, self.ai_next_move)

        self.__game.set_board(cur_board)

    def ai_next_move(self, move):
        """
        :param move:
        :return:
        """
        if move == -1:
            self.one_turn(self.__ai_next_move)

        else:
            self.__ai_next_move = move

    def one_turn(self, column):
        """
        :param column:
        :return:
        """
        if self.__game.get_current_player() == self.__color:
            try:
                self.__game.make_move(column)
                coord = self.__game.get_last_coord()
                self.__screen.update_cell(coord, self.__color)
                self.__communicator.send_message(str(column))

            except:
                self.__screen.print_to_gui(self.__game.ILLEGAL_MOVE_MSG)
        else:
            self.__screen.print_to_gui(self.NOT_YOUR_TURN_MSG)
            return
            
        winner = self.__game.get_winner()
        self.__screen.print_to_gui('pressed ' + str(column) + '  last coord ' + str(self.__game.get_last_coord())+' winner '+str(winner))

        if winner is not None:
            self.end_game(winner)
            self.__communicator.send_message(str(column)+'end')

    def end_game(self, winner):
        """
        :return:
        """
        win_info = self.__game.get_win_info()
        self.__game.set_game_off()

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

            if 'end' not in text:
                player = self.__game.get_current_player()
                self.__game.make_move(int(text))
                coord = self.__game.get_last_coord()
                self.__screen.update_cell(coord, player)

                if self.__player == ARG_PLAYERS[1]:
                    self.ai_turn()

            else:
                self.__game.make_move(int(text[0]))
                winner = self.__game.get_winner()
                self.end_game(winner)


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
