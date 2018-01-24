###################################################################################
# FILE : screen.py
# WRITERS : Gil Adam, Jonathan Zedaka, giladam, jonathanzd,  200139814, 204620835
# EXERCISE : intro2cs ex12 2017-2018
# DESCRIPTION: Screen class for four in a row game
###################################################################################

from game import Game
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk


class Screen:
    """
    GUI object using Tkinter library. Handles the graphical display of the game, updating moves,
    human user input, displaying messages for invalid moves and the result at game end.
    Assumes a local folder named 'gui' with game element images, Tkinter and PIL libraries.
    """
    CELL_ORI = (271.5, 255)         # placement coordinate constants
    CELL_OFFSET = (71.5, 65)
    BUT_ORI = (271, 165)
    TXT1_ORI = (165, 595)
    TXT2_ORI = (852, 595)
    MSG_OFFSET = 100

    DEFAULT_TIMEOUT = 4000          # timing constants
    END_TIMEOUT = 100000
    ANIM_DELAY = 50
    FLASH_DELAY = 85
    FLASH_COUNT = 1000

    def __init__(self, tk_root, my_color, button_func):
        """
        Initialize the Screen object
        :param tk_root: the tkinter object to act as root
        :param my_color: self player color (PLAYER_ONE / PLAYER_TWO defined class consts of Game class)
        :param button_func: function to bind to input buttons for making a move
        """
        self.__root = tk_root
        self.__press_func = button_func

        self.__cells = []
        self.__buttons = []

        self.import_images()
        self.build_gui(my_color)

    def import_images(self):
        """
        Imports image elements from local folder 'gui' with PIL library and saves them
        as object attributes of type ImageTk.
        :return: None
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

    def build_gui(self, my_color):
        """
        Build all GUI elements (board, buttons, text boxes) inside Tkinter root object
        :param my_color: self player color (PLAYER_ONE / PLAYER_TWO)
        :return: None
        """
        self.__root.resizable(width=False, height=False)

        text_font = font.Font(family='Courier', size=13)
        text_font_bold = font.Font(family='Courier', size=13, weight=font.BOLD)

        label_bg = tk.Label(self.__root, image=self.__bg, bd=0)     # background image
        label_bg.image = self.__bg
        label_bg.pack()

        for i in range(Game.BOARD_Y):               # board cells are image labels saved in a list
            temp_row = []
            for j in range(Game.BOARD_X):
                temp_label = tk.Label(self.__root, image=self.__blank,  bd=0)
                temp_label.image = self.__blank
                temp_label.place(x=self.CELL_ORI[0]+j*self.CELL_OFFSET[0], y=self.CELL_ORI[1]+i*self.CELL_OFFSET[1])
                temp_row.append(temp_label)
            self.__cells.append(temp_row)

        for i in range(Game.BOARD_X):                # buttons are image labels with functions bounded to events
            temp_button = tk.Label(self.__root, image=self.__but1, bd=0)
            temp_button.image = self.__but1

            temp_button.bind("<Enter>", lambda event, col=i: self.button_enter(event, col, press=False))
            temp_button.bind("<Leave>", lambda event, col=i: self.button_leave(event, col))
            temp_button.bind("<Button-1>", lambda event, col=i: self.button_leave(event, col))
            temp_button.bind("<ButtonRelease-1>", lambda event, col=i: self.button_enter(event, col, press=True))

            temp_button.place(x=self.BUT_ORI[0]+i*self.CELL_OFFSET[0], y=self.BUT_ORI[1])
            self.__buttons.append(temp_button)

        self.__textbox1 = tk.Label(self.__root, font=text_font, bg='black', fg='green', justify=tk.CENTER)
        self.__textbox2 = tk.Label(self.__root, font=text_font, bg='black', fg='green', justify=tk.CENTER)
        self.__textbox1.place(x=self.TXT1_ORI[0], y=self.TXT1_ORI[1], anchor=tk.CENTER)
        self.__textbox2.place(x=self.TXT2_ORI[0], y=self.TXT2_ORI[1], anchor=tk.CENTER)

        self.__msgbox1 = tk.Label(self.__root, font=text_font_bold, bg='black', fg='green', justify=tk.CENTER)
        self.__msgbox2 = tk.Label(self.__root, font=text_font_bold, bg='black', fg='green', justify=tk.CENTER)
        self.__msgbox1.place(x=self.TXT1_ORI[0], y=self.TXT1_ORI[1]-self.MSG_OFFSET, anchor=tk.CENTER)
        self.__msgbox2.place(x=self.TXT2_ORI[0], y=self.TXT2_ORI[1]-self.MSG_OFFSET, anchor=tk.CENTER)

        if my_color == Game.PLAYER_ONE:
            self.__textbox1.config(text = "PLAYER 1\nyou")
            self.__textbox2.config(text = "PLAYER 2\nopponent")
        else:
            self.__textbox1.config(text = "PLAYER 1\nopponent")
            self.__textbox2.config(text = "PLAYER 2\nyou")

    def button_enter(self, event, col, press):
        """
        Function to bind to the events of mouse entering button area, and pressing the button.
        :param event: event object received from tkinter (not used)
        :param col: column of the button activated (0 <= int <= 6)
        :param press: True if button pressed, False if not
        :return: None
        """
        self.__buttons[col].image = self.__but2
        self.__buttons[col].configure(image=self.__but2)
        if press:
            self.__press_func(col)

    def button_leave(self, event, col):
        """
        Function to bind to the event of mouse leaving button area.
        :param event: event object received from tkinter (not used)
        :param col: column of the button activated (0 <= int <= 6)
        :return: None
        """
        self.__buttons[col].image = self.__but1
        self.__buttons[col].configure(image=self.__but1)

    def update_cell(self, row, col, player, anim):
        """
        Update the display of a cell from blank
        :param row:
        :param col:
        :param player:
        :param anim:
        :return:
        """
        coin = self.__coin1
        if player == Game.PLAYER_TWO:
            coin = self.__coin2

        if anim:
            self.anim_helper(0, col, coin)
            for i in range(row):
                self.__root.after(self.ANIM_DELAY*(i+1), self.anim_helper, i+1, col, coin)
        else:
            self.__cells[row][col].image = coin
            self.__cells[row][col].configure(image=coin)

    def anim_helper(self, row, col, coin):
        """
        :return:
        """
        if row > 0:
            self.__cells[row-1][col].image = self.__blank
            self.__cells[row-1][col].configure(image=self.__blank)

        self.__cells[row][col].image = coin
        self.__cells[row][col].configure(image=coin)

    def win(self, coord, direction, winner):
        """
        :param coord:
        :param direction:
        :return:
        """
        if winner == Game.DRAW:
            return

        row, col = coord
        dir_row, dir_col = direction

        win_coin = self.__coin1
        if winner == Game.PLAYER_TWO:
            win_coin = self.__coin2

        cell_list = []
        for i in range(Game.WIN_LEN):
            cell_list.append(self.__cells[row+i*dir_row][col+i*dir_col])

        for i in range(self.FLASH_COUNT):
            self.__root.after(i*self.FLASH_DELAY, self.win_helper, cell_list, i, win_coin)

    def win_helper(self, cell_list, index, win_coin):
        """
        :param index:
        :return:
        """
        if index < self.FLASH_COUNT-1:
            cell_list[index % Game.WIN_LEN].image = self.__blank
            cell_list[index % Game.WIN_LEN].configure(image=self.__blank)

        cell_list[(index-1) % Game.WIN_LEN].image = win_coin
        cell_list[(index-1) % Game.WIN_LEN].configure(image=win_coin)

    def print_to_screen(self, msg, player, end=False):
        """
        :param msg:
        :return:
        """
        if player == Game.PLAYER_ONE:
            self.__msgbox1.config(text=msg)
            if end:
                self.__root.after(self.END_TIMEOUT, self.clear_msg, player)
            else:
                self.__root.after(self.DEFAULT_TIMEOUT, self.clear_msg, player)

        elif player == Game.PLAYER_TWO:
            self.__msgbox2.config(text=msg)
            if end:
                self.__root.after(self.END_TIMEOUT, self.clear_msg, player)
            else:
                self.__root.after(self.DEFAULT_TIMEOUT, self.clear_msg, player)

    def clear_msg(self, player):
        """
        :param player:
        :return:
        """
        if player == Game.PLAYER_ONE:
            self.__msgbox1.config(text='')

        elif player == Game.PLAYER_TWO:
            self.__msgbox2.config(text='')

    def get_root(self):
        return self.__root
