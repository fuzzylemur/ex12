import sys
from game import Game
from communicator import Communicator
from ai import AI
import tkinter as tk


ARG_ERROR = "Illegal program arguments."
ARG_PLAYERS = ['human', 'ai']
ARG_PORT_MAX = 65535
COLOR_ONE = 'blue'
COLOR_TWO = 'red'


class FourInARow:

    def __init__(self, root, player, port, ip=None):
        """
        :param player:
        :param port:
        :param ip:
        """
        self.__game = Game()
        self.__root = root
        self.__player = player

        self.__communicator = Communicator(self.__root, port, ip)
        self.__communicator.connect()
        self.__communicator.bind_action_to_message(self.handle_message)

        self.build_gui()

    def build_gui(self):
        """
        :return:
        """
        self.__canvas = tk.Canvas(self.__root, width=700, height=700, bg='black')
        self.__canvas.pack()

        self.__circles = []
        for j in range(Game.BOARD_Y):
            temp_row = []
            for i in range(Game.BOARD_X):
                temp_row.append(self.__canvas.create_oval(5+100*i, 100*j+50, 100*i+95, 100*j+140, fill="white"))
            self.__circles.append(temp_row)

        for i in range(7):
            temp_button = tk.Button(self.__canvas, text='button '+str(i), command=lambda col=i: self.one_turn(col))
            temp_button.place(x=i*100, y=0)

        self.__msg_box = tk.Label(self.__canvas, text='Yo yo yo...', fg='red', bg='black')
        self.__msg_box.place(x=10, y=670)

    def update_cell(self, coordinate):
        """
        :param coordinate:
        :return:
        """
        row, col = coordinate[0], coordinate[1]
        player = self.__game.get_player_at(row, col)

        if player == Game.PLAYER_ONE:
            self.__canvas.itemconfig(self.__circles[row][col], fill=COLOR_ONE)

        if player == Game.PLAYER_TWO:
            self.__canvas.itemconfig(self.__circles[row][col], fill=COLOR_TWO)

    def print_to_screen(self, msg):
        """
        :param msg:
        :return:
        """
        self.__msg_box.config(text=msg)
        self.__msg_box.place(x=10, y=670)

    def one_turn(self, column):
        """
        :param column:
        :return:
        """
        self.print_to_screen('pressed' + str(column))

        try:
            coord = self.__game.make_move(column)
            self.update_cell(coord)
        except:
            self.print_to_screen(self.__game.ILLEGAL_MOVE_MSG)

        winner = self.__game.get_winner()
        if winner is None:
            self.__communicator.send_message(str(column))
        else:
            self.end_game(winner)
            self.__communicator.send_message('end'+str(winner[0]))

    def end_game(self, winner):
        """
        :return:
        """
        self.print_to_screen('winner is '+str(winner[0]))

    def handle_message(self, text):
        """
        Specifies the event handler for the message getting event in the
        communicator. Prints a message when invoked (and invoked by the
        communicator when a message is received).
        :param text: the text to be printed.
        :return: None.
        """
        if 'end' not in text:
            coord = self.__game.make_move(text)
            self.update_cell(coord)
        else:
            self.end_game(text[3])


def main(args):
    """
    :return:
    """
    player = args[1]
    port = args[2]

    if len(args) > 3:
        ip = args[3]

    root = tk.Tk()
    FourInARow(root, player, port)
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

    args = [0, 'human', 8000]
    main(args)
