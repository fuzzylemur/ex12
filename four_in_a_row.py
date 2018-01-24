###################################################################################
# FILE : four_in_row.py
# WRITERS : Gil Adam, Jonathan Zedaka, giladam, jonathanzd,  200139814, 204620835
# EXERCISE : intro2cs ex12 2017-2018
# DESCRIPTION: Main implementation for four in a row game
###################################################################################

import sys
import tkinter as tk
from game import Game
from communicator import Communicator
from ai import AI
from screen import Screen

ARG_ERROR = "Illegal program arguments."
ARG_PLAYERS = ['human', 'ai']
ARG_PORT_MAX = 65535
NUM_ARGS = 3
PLAYER_ARGS_LOCATION = 1
PORT_ARGS_LOCATION = 2
IP_ARGS_LOCATION = 3


class FourInARow:
    """
    The high level application object, handling game events,
    turn order and legality, communication between instances 
    and controlling the objects that manage GUI, gameplay and AI.
    """
    PLAYERS = ARG_PLAYERS
    MSG_NOT_TURN = 'Not your turn!'
    MSG_DRAW = 'draw'
    MSG_WIN = 'winner!'
    MSG_LOSE = 'loser :('
    
    def __init__(self, root, player, port, ip):
        """
        The function initialize all object's private values.
        :param player: A string which decide if the player is human or ai.
        :param port: An integer between 0 to 65535. better use ~8000
        :param ip: The host IP. can be None if the player is the
        host or the host ip address.
        """
        self.__root = root
        self.__game = Game()
                                                # decide whether the player is AI or not
        if player == self.PLAYERS[1]:
            self.__is_ai = True
        else:
            self.__is_ai = False
                                                # Set both Players colors
        if ip:
            self.__my_color = Game.PLAYER_TWO
            self.__op_color = Game.PLAYER_ONE

        else:
            self.__my_color = Game.PLAYER_ONE
            self.__op_color = Game.PLAYER_TWO
        
        self.__communicator = Communicator(root, port, ip)
        self.__communicator.connect()
        self.__communicator.bind_action_to_message(self.handle_message)

        if self.__is_ai:                              # If the player is AI we initialize an AI object
            self.__screen = Screen(root, self.__my_color, lambda y: None)
            self.__ai = AI()
            if self.__my_color == Game.PLAYER_ONE:
                self.ai_find_move()                   # and call ai_find_move to make the first move.
        else:
            self.__screen = Screen(root, self.__my_color, self.play_my_move)

    def ai_find_move(self):
        """
        The function handles the AI turn.
        It creates a copy of the game object and sends it to the AI instance.
        Then, it makes the next AI move using the AI find_legal_move method.
        :return: None
        """
        # creates a copy of the game instance and sends it to the AI.
        sim_game = Game()
        board, register, cell_set, counter = self.__game.get_attr_for_sim()
        sim_game.set_attr_for_sim(board, register, cell_set, counter)

        try:
            self.__ai.find_legal_move(sim_game, self.play_my_move)
        except:
            self.__screen.print_to_screen(self.__ai.NO_AI_MOVE, self.__my_color)

    def play_my_move(self, column):
        """
        The function handles a certain game move, both by the AI instance
        and when a GUI button is pressed, by calling the class one_turn method
        and sending the opponent a message using the communicator instance.
        :param column: column in board to play (0 <= int <= 6)
        :return: None
        """
        if self.one_turn(column, self.__my_color):
            self.__communicator.send_message(str(column))

    def one_turn(self, column, player):
        """
        The function handles one turn of both kinds of players,
        AI and human by preforming the following actions:
        1. Try to make the given move(column).
        2. Update the screen instance according to the move.
        3. Send the opponent an message about the move it made.
        4. Checks if the game ended using the game get_winner method.
        :param column: column in board (0 <= int <= 6)
        :param player: The player which made the turn. Player_one/Player_two.
        :return: True if the move was done (may be illegal move). None otherwise.
        """
        # The below if make sure that both players can play only when its their turn.
        if self.__game.get_current_player() == player: 
        #Try to make the move, if the move is illegal raise an exception
            try:
                self.__game.make_move(column)
                row, col = self.__game.get_last_coord()
                move_done = True

                if self.__is_ai:
                    self.__screen.update_cell(row, col, player, anim=False)
                else:
                    self.__screen.update_cell(row, col, player, anim=True)

            except:
                self.__screen.print_to_screen(self.__game.ILLEGAL_MOVE_MSG, player)
                return

        else:
            self.__screen.print_to_screen(self.MSG_NOT_TURN, player)
            return
        # check if the game is ended by win/loss/draw.
        winner = self.__game.get_winner()
        if winner is not None:
            self.end_game(winner)

        return move_done

    def end_game(self, winner):
        """
        The function handles the situation where the game is done.
        Its using the screen instance to print the game result 
        (win/loss/draw) to the graphical interface.
        :param winner: The game result (PLAYER_ONE / PLAYER_TWO / DRAW).
        :return: None
        """
        win_coord, win_dir = self.__game.get_win_info()       # Ask the game instance for the win_coord and direction
        self.__screen.win(win_coord, win_dir, winner)         # In order to display the winning sequence (FLASH!)

        if winner == Game.DRAW:
            self.__screen.print_to_screen(self.MSG_DRAW, self.__my_color, end=True)
            self.__screen.print_to_screen(self.MSG_DRAW, self.__op_color, end=True)

        elif winner == self.__my_color:
            self.__screen.print_to_screen(self.MSG_WIN, self.__my_color, end=True)
            self.__screen.print_to_screen(self.MSG_LOSE, self.__op_color, end=True)

        elif winner == self.__op_color:
            self.__screen.print_to_screen(self.MSG_WIN, self.__op_color, end=True)
            self.__screen.print_to_screen(self.MSG_LOSE, self.__my_color, end=True)

    def handle_message(self, message=None):
        """
        The function specifies the event handler for the message getting
        event in the communicator. When it is invoked, it calls the one_turn
        method in order to update the opponent move on its screen instance
        or end the game if needed. it invoked by the
        communicator when a message is received.
        :param message: The last move the opponent made (0 <= int <= 6) Default is None.
        :return: None
        """
        if message:
            self.one_turn(int(message[0]), self.__op_color)
            if self.__is_ai:                   # If the player is AI we call ai_find_move to make the AI next move.
                if self.__game.get_win_info()[1] is None:
                    self.ai_find_move()


def main(args):
    """"
    The main function which initialize both FourInARow and
    a Tk instances in order to run the game. The function
    receives the sys.args parameters and returns None
    """
    player = args[PLAYER_ARGS_LOCATION]             # unpack all args
    port = int(args[PORT_ARGS_LOCATION])
    ip = None

    if len(args) > NUM_ARGS:                        # If the user entered an IP address when calling the program
        ip = args[IP_ARGS_LOCATION]                 # we send it when calling the FourInARow constructor.
                                                    # else, we use ip = None.

    root = tk.Tk()                                  # Creates a FourInARow and a Tk object instances
    FourInARow(root, player, port, ip)
    root.mainloop()                                 # runs the game main loop


if __name__ == "__main__":
    if not NUM_ARGS-1 < len(sys.argv) < NUM_ARGS+2:         # Validates that the given cmd arguments are correct
        print(ARG_ERROR)                                    # If there are less then 2 or more then 3
        sys.exit()                                          # arguments we print an error msg and call sys.exit
        
    if sys.argv[PLAYER_ARGS_LOCATION] not in ARG_PLAYERS:   # Make player input is human/ai.
        print(ARG_ERROR)
        sys.exit()

    if int(sys.argv[PORT_ARGS_LOCATION]) > ARG_PORT_MAX:    # make sure the port input is valid
        print(ARG_ERROR)
        sys.exit()

    main(sys.argv)
