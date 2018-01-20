from game import Game
import tkinter as tk
from PIL import Image, ImageTk


class Screen:

    CELL_ORI = (271.5, 255)
    BUT_ORI = (271, 165)
    OFF = (71.5, 65)
    DELAY = 50

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
        label_bg = tk.Label(self.__root, image=self.__bg, bd=0, cursor='cross')
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

    def update_helper(self, row, col, player):
        """
        :return:
        """
        if row > 0:
            self.__cells[row-1][col].image = self.__blank
            self.__cells[row-1][col].configure(image=self.__blank)

        if player == Game.PLAYER_ONE:
            self.__cells[row][col].image = self.__coin1
            self.__cells[row][col].configure(image=self.__coin1)

        if player == Game.PLAYER_TWO:
            self.__cells[row][col].image = self.__coin2
            self.__cells[row][col].configure(image=self.__coin2)

    def update_cell(self, row, col, player):
        """
        :param coordinate:
        :return:
        """

        self.update_helper(0, col, player)
        for i in range(row):
            self.__root.after(self.DELAY*(i+1), self.update_helper, i+1, col, player)

    def print_to_gui(self, msg):
        """
        :param msg:
        :return:
        """
        pass

"""
def func():
    pass

root = tk.Tk()
screen = Screen(root, func, 0)
root.mainloop()"""

