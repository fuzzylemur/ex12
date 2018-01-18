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

    NOT_YOUR_TURN_MSG = 'Not your turn!'
    
    def __init__(self, root, player, port, ip):
        """
        :param player:
        :param port:
        :param ip:
        """
        self.__game = Game()
        self.__root = root
        self.__player = player
        
        if ip:
            self.__color = Game.PLAYER_TWO
        else:
            self.__color = Game.PLAYER_ONE
            
        if self.__player == ARG_PLAYERS[1]:
            print(self.__color)
            self.__ai = AI(self.__color)
            if self.__color == Game.PLAYER_ONE:
                self.__ai.find_legal_move(self.game, self.game.make_move)
                
        self.__communicator = Communicator(self.__root, port, ip)
        self.__communicator.connect()
        self.__communicator.bind_action_to_message(self.__handle_message)

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
        row, col = coordinate
        player = self.__game.get_player_at(row, col)

        if player == Game.PLAYER_ONE:
            self.__canvas.itemconfig(self.__circles[row][col], fill=COLOR_ONE)

        if player == Game.PLAYER_TWO:
            self.__canvas.itemconfig(self.__circles[row][col], fill=COLOR_TWO)

    def print_to_gui(self, msg):
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
        if self.__game.get_current_player() == self.__color:
            try:
                self.__game.make_move(column)
                coord = self.__game.get_coord()
                self.update_cell(coord)
                self.__communicator.send_message(str(column))

            except:
                self.print_to_gui(self.__game.ILLEGAL_MOVE_MSG)
        else:
            self.print_to_gui(self.NOT_YOUR_TURN_MSG)
            return
            
        winner = self.__game.get_winner()
        self.print_to_gui('pressed ' + str(column) + '  last coord ' + str(self.__game.get_coord())+' winner '+str(winner))

        if winner is not None:
            self.end_game(winner)
            self.__communicator.send_message('end'+str(winner))

    def end_game(self, winner):
        """
        :return:
        """
        win_info = self.__game.get_win_info()
        if winner == 2:
            self.print_to_gui('Draw')
        else:
            self.print_to_gui('winner is '+str(winner))

    def __handle_message(self, text=None):
        """
        Specifies the event handler for the message getting event in the
        communicator. Prints a message when invoked (and invoked by the
        communicator when a message is received).
        :param text: the text to be printed.
        :return: None.
        """
        if text:
            if 'end' not in text:
                if self.__player == ARG_PLAYERS[0]:
                    self.__game.make_move(int(text))
                    coord = self.__game.get_coord()
                    self.update_cell(coord)
                else:
                    self.__ai.find_legal_move(self.game, self.game.make_move)
            else:
                self.__game.end_game()
                self.end_game(text[3])


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
