import sys
from game import Game
from communicator import Communicator
from ai import AI
import tkinter as tk


ARG_ERROR = "Illegal program arguments."
ARG_PLAYERS = ['human', 'ai']
ARG_PORT_MAX = 65535

class FourInARow():

    def __init__(self, root, player, port, ip=None):
        """
        :param player:
        :param port:
        :param ip:
        """
        self.__game = Game()
        self.__root = root

        self.__player = player
        self.__port = port
        self.__ip = ip
        self.__communicator = Communicator(self.__root, port, ip)
        self.__communicator.connect()
        self.__communicator.bind_action_to_message(self.__handle_message)

        self.__init_gui()

    def __init_gui(self):

        self.canvas = tk.Canvas(self.__root, width=700, height=700, bg='black')
        self.canvas.pack()

        self.circles = []
        for j in range(6):
            temp_row = []
            for i in range(7):
                temp_row.append(self.canvas.create_oval(100*i, 100*j+50, 100*i+100, 100*j+150, fill="white"))
            self.circles.append(temp_row)

        for i in range(7):
            temp_button = tk.Button(self.canvas, text='button '+str(i), command=lambda col=i: self.__make_move(col))
            temp_button.place(x=i*100, y=0)

        self.msg_box = tk.Label(self.canvas, text='i', fg='red', bg='black')
        self.msg_box.place(x=10, y=670)


    def update_cell(self, coordinate, player):
        row = coordinate[0]
        col = coordinate[1]

        if player == 0:
            self.canvas.itemconfig(self.circles[row][col], fill="blue")

        if player == 1:
            self.canvas.itemconfig(self.circles[row][col], fill="red")

    def print_to_screen(self, msg):
        self.msg_box = tk.Label(self.canvas, text=msg, fg='red', bg='black')
        self.msg_box.place(x=10, y=670)


    def __make_move(self, column):
        self.print_to_screen('pressed' + str(column))
        try:
            location = self.__game.make_move(column)
            player = self.__game.get_player_at(location[0], location[1])
            self.update_cell(location, player)
        except:
            self.print_to_screen(self.__game.ILLEGAL_MOVE_MSG)

        winner = self.__game.get_winner()
        if winner is None:
            self.__communicator.send_message(str(column))
        else:
            self.__end_game(winner)
            self.__communicator.send_message('end'+str(winner))



    def __end_game(self, winner):
        """
        :return:
        """
        self.print_to_screen('winner is '+str(winner))

    def __handle_message(self, text):
        """
        Specifies the event handler for the message getting event in the
        communicator. Prints a message when invoked (and invoked by the
        communicator when a message is received). The message will
        automatically disappear after a fixed interval.
        :param text: the text to be printed.
        :return: None.
        """
        if 'end' not in text:
            location = self.__game.make_move(text)
            player = self.__game.get_player_at(location[0], location[1])
            self.update_cell(location, player)
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
