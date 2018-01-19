from game import Game
import tkinter as tk

class Screen:

    COLOR_ONE = 'blue'
    COLOR_TWO = 'red'

    def __init__(self, tk_root, button_func):
        """
        :param tk_root:
        """
        self.__root = tk_root
        self.__func = button_func

        self.__circles = []
        self.__canvas = None
        self.__msg_box = None

        self.build_gui()

    def build_gui(self):
        """
        :return:
        """
        self.__canvas = tk.Canvas(self.__root, width=700, height=700, bg='black')
        self.__canvas.pack()

        for j in range(Game.BOARD_Y):
            temp_row = []
            for i in range(Game.BOARD_X):
                temp_row.append(
                    self.__canvas.create_oval(5 + 100 * i, 100 * j + 50, 100 * i + 95, 100 * j + 140, fill="white"))
            self.__circles.append(temp_row)

        for i in range(7):
            temp_button = tk.Button(self.__canvas, text='button ' + str(i), command=lambda col=i: self.__func(col))
            temp_button.place(x=i * 100, y=0)

        self.__msg_box = tk.Label(self.__canvas, text='Yo yo yo...', fg='red', bg='black')
        self.__msg_box.place(x=10, y=670)

    def update_cell(self, coordinate, player):
        """
        :param coordinate:
        :return:
        """
        row, col = coordinate

        if player == Game.PLAYER_ONE:
            self.__canvas.itemconfig(self.__circles[row][col], fill=self.COLOR_ONE)

        if player == Game.PLAYER_TWO:
            self.__canvas.itemconfig(self.__circles[row][col], fill=self.COLOR_TWO)

    def print_to_gui(self, msg):
        """
        :param msg:
        :return:
        """
        self.__msg_box.config(text=msg)
        self.__msg_box.place(x=10, y=670)