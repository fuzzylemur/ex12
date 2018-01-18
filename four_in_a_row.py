import sys
from game import Game
from communicator import Communicator
from ai import AI
import tkinter as tk


ARG_ERROR = "Illegal program arguments."
ARG_PLAYERS = ['human', 'ai']
ARG_PORT_MAX = 65535

class Gui():

    def __init__(self, root, player, port, ip=None):
        """
        :param player:
        :param port:
        :param ip:
        """
        self.__game = Game()
        self.__root = root

        self.frame = tk.Frame(self.__root, width=700, height=700, bg='red')
        self.frame.pack()

        self.top = tk.Frame(self.frame, width=700, height=100, bg='red')
        self.top.pack(side=tk.TOP)

        self.build_gui()
        self.__player = player
        self.__port = port
        self.__ip = ip
        self.__communicator = Communicator(root, port, ip)
        self.__communicator.connect()
        self.__communicator.bind_action_to_message(self.__handle_message)

    def build_gui(self):

        self.button1 = tk.Button(self.top, text='button 1', width=100, height=100)
        self.button1.pack(side=tk.LEFT)
        #self.button1.place(x=0, y=0)


    def update_tk(self, column):
        pass

    def print_to_screen(self, msg):
        pass

    def __make_move(self, column):
        try:
            location = self.__game.make_move(column)
            self.update_tk(location)
        except:
            self.print_to_screen(self.__screen.ILLEGAL_MOVE_MSG)

        winner = self.__game.get_winner()
        if winner is None:
            self.__communicator.send_message(column)
        else:
            self.end_game(winner)
            self.__communicator.send_message(winner, True)



    def __end_game(self):
        """
        :return:
        """
        pass

    def __handle_message(self, text, end_game=False):
        """
        Specifies the event handler for the message getting event in the
        communicator. Prints a message when invoked (and invoked by the
        communicator when a message is received). The message will
        automatically disappear after a fixed interval.
        :param text: the text to be printed.
        :return: None.
        """
        if not end_game:
            self.__game.make_move(text)
            self.update_tk(text)
        else:
            self.__end_game(text)

def main(args):
    """
    :return:
    """
    player = args[1]
    port = args[2]

    if len(args) > 3:
        ip = args[3]

    root = tk.Tk()
    Gui(root, player, port)
    root.mainloop()

if __name__ == "__main__":
    """
    if not 2 < len(sys.argv) < 4:
        print(ARG_ERROR)

    if sys.argv[1] not in ARG_PLAYERS:
        print(ARG_ERROR)

    if sys.argv[2] < ARG_PORT_MAX:
        print(ARG_ERROR)
"""

    args = ['human', 8000, 0]
    main(args)
