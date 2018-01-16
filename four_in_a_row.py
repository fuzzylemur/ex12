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
        """
        self.__player = player
        self.__port = port
        self.__ip = ip
        self.__communicator = Communicator(root, port, ip)
        self.__communicator.connect()
        self.__communicator.bind_action_to_message(self.make_move)"""



    def build_gui(self):

        self.button1 = tk.Button(self.top, text='button 1', width=100, height=100)
        self.button1.pack(side=tk.LEFT)
        #self.button1.place(x=0, y=0)



    def update_tk(self, column):
        pass

    def make_move(self, column):

        self.__game.make_move(column)
        self.update_tk(column)
        self.__communicator.send_message(column)

        winner = self.__game.get_winner()
        if winner is None:
            pass



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
