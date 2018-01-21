from game import Game
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk


class Screen:

    CELL_ORI = (271.5, 255)
    BUT_ORI = (271, 165)
    TXT1_ORI = (131, 570)
    TXT2_ORI = (820, 570)
    OFF = (71.5, 65)
    DELAY = 50
    WIN_DELAY = 85
    FLASH_COUNT = 1000


    def __init__(self, tk_root, button_func):
        """
        :param tk_root:
        """
        self.__root = tk_root
        self.__func = button_func

        self.__cells = []
        self.__buttons = []
        self.__msg_box = None

        self.import_images()
        self.build_gui()

    def import_images(self):
        """
        :return:
        """
        bg = Image.open("gui/bg.tiff")
        self.__bg = ImageTk.PhotoImage(bg)

        blank = Image.open("gui/blank.tiff")
        self.__blank = ImageTk.PhotoImage(blank)

        coin1 = Image.open("gui/coin1.tiff")
        self.__coin1 = ImageTk.PhotoImage(coin1)

        coin2 = Image.open("gui/coin2.tiff")
        self.__coin2 = ImageTk.PhotoImage(coin2)

        but1 = Image.open("gui/but1.tiff")
        self.__but1 = ImageTk.PhotoImage(but1)

        but2 = Image.open("gui/but2.tiff")
        self.__but2 = ImageTk.PhotoImage(but2)

    def build_gui(self):
        """
        :return:
        """
        self.__root.resizable(width=False, height=False)
        self.__text_font = font.Font(family='Courier', size=13)


        label_bg = tk.Label(self.__root, image=self.__bg, bd=0)
        label_bg.image = self.__bg
        label_bg.pack()

        for i in range(Game.BOARD_Y):
            temp_row = []
            for j in range(Game.BOARD_X):
                temp_label = tk.Label(self.__root, image=self.__blank,  bd=0)
                temp_label.image = self.__blank
                temp_label.place(x=self.CELL_ORI[0]+j*self.OFF[0], y=self.CELL_ORI[1]+i*self.OFF[1])
                temp_row.append(temp_label)
            self.__cells.append(temp_row)

        for i in range(Game.BOARD_X):
            temp_button = tk.Label(self.__root, image=self.__but1, bd=0)
            temp_button.image = self.__but1

            temp_button.bind("<Enter>", lambda event, col=i: self.button_enter(event, col))
            temp_button.bind("<Leave>", lambda event, col=i: self.button_leave(event, col))
            temp_button.bind("<Button-1>", lambda event, col=i: self.button_leave(event, col))
            temp_button.bind("<ButtonRelease-1>", lambda event, col=i: self.button_action(event, col))

            temp_button.place(x=self.BUT_ORI[0]+i*self.OFF[0], y=self.BUT_ORI[1])
            self.__buttons.append(temp_button)

        textbox1 = tk.Label(self.__root, text="PLAYER 1\ncomputer", font=self.__text_font, bg='black', fg='green', justify=tk.CENTER)
        textbox1.place(x=self.TXT1_ORI[0], y=self.TXT1_ORI[1])

        textbox2 = tk.Label(self.__root, text="PLAYER 2\nyou", font=self.__text_font, bg='black', fg='green', justify=tk.CENTER)
        textbox2.place(x=self.TXT2_ORI[0], y=self.TXT2_ORI[1])

    def button_enter(self, event, col):
        """
        :return:
        """
        self.__buttons[col].image = self.__but2
        self.__buttons[col].configure(image=self.__but2)

    def button_leave(self, event, col):
        """
        :return:
        """
        self.__buttons[col].image = self.__but1
        self.__buttons[col].configure(image=self.__but1)

    def button_action(self, event, col):
        """
        :return:
        """
        self.__buttons[col].image = self.__but2
        self.__buttons[col].configure(image=self.__but2)
        self.__func(col)

    def update_helper(self, row, col, coin):
        """
        :return:
        """

        if row > 0:
            self.__cells[row-1][col].image = self.__blank
            self.__cells[row-1][col].configure(image=self.__blank)

        self.__cells[row][col].image = coin
        self.__cells[row][col].configure(image=coin)

    def update_cell(self, row, col, player):
        """
        :param row:
        :param col:
        :param player:
        :return:
        """

        coin = self.__coin1
        if player == Game.PLAYER_TWO:
            coin = self.__coin2

        self.update_helper(0, col, coin)
        for i in range(row):
            self.__root.after(self.DELAY*(i+1), self.update_helper, i+1, col, coin)

    def win(self, coord, direction, winner):
        """
        :param coord:
        :param direction:
        :return:
        """
        row, col = coord
        dir_row, dir_col = direction

        win_coin = self.__coin1
        if winner == Game.PLAYER_TWO:
            win_coin = self.__coin2

        cell_list = []
        for i in range(Game.WIN_LEN):
            cell_list.append(self.__cells[row+i*dir_row][col+i*dir_col])

        for i in range(self.FLASH_COUNT):
            self.__root.after(i*self.WIN_DELAY, self.win_helper, cell_list, i, win_coin)


    def win_helper(self, cell_list, index, win_coin):
        """
        :param index:
        :return:
        """
        if index < self.FLASH_COUNT-1:
            cell_list[index%Game.WIN_LEN].image = self.__blank
            cell_list[index%Game.WIN_LEN].configure(image=self.__blank)

        cell_list[(index-1)%Game.WIN_LEN].image = win_coin
        cell_list[(index-1)%Game.WIN_LEN].configure(image=win_coin)


    def print_to_gui(self, msg):
        """
        :param msg:
        :return:
        """
        pass


def func(x):
    pass

"""
root = tk.Tk()
screen = Screen(root, func)
screen.win((0,0),(1,0),1)
root.mainloop()
"""

