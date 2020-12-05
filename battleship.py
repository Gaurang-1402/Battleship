# Author: Gaurang Ruparelia
# Assignment #6 - Battleship


import random

### DO NOT EDIT BELOW (with the exception of MAX_MISSES) ###

HIT_CHAR = 'x'
MISS_CHAR = 'o'
BLANK_CHAR = '.'
HORIZONTAL = 'h'
VERTICAL = 'v'
MAX_MISSES = 20
SHIP_SIZES = {
    "carrier": 5,
    "battleship": 4,
    "cruiser": 3,
    "submarine": 3,
    "destroyer": 2
}
NUM_ROWS = 10
NUM_COLS = 10
ROW_IDX = 0
COL_IDX = 1
MIN_ROW_LABEL = 'A'
MAX_ROW_LABEL = 'J'


def get_random_position():
    """Generates a random location on a board of NUM_ROWS x NUM_COLS."""

    row_choice = chr(
                    random.choice(
                        range(
                            ord(MIN_ROW_LABEL),
                            ord(MIN_ROW_LABEL) + NUM_ROWS
                        )
                    )
    )

    col_choice = random.randint(0, NUM_COLS - 1)

    return (row_choice, col_choice)


def play_battleship():
    """Controls flow of Battleship games including display of
    welcome and goodbye messages.

    :return: None
    """

    print("Let's Play Battleship!\n")

    game_over = False

    while not game_over:

        game = Game()
        game.display_board()

        while not game.is_complete():
            pos = game.get_guess()
            result = game.check_guess(pos)
            game.update_game(result, pos)
            game.display_board()

        game_over = end_program()

    print("Goodbye.")

### DO NOT EDIT ABOVE (with the exception of MAX_MISSES) ###



class Ship:

    def __init__(self, name, start_position, orientation):
        """Creates a new ship with the given name, placed at start_position in the
        provided orientation. The number of positions occupied by the ship is determined
        by looking up the name in the SHIP_SIZE dictionary.

        :param name: the name of the ship
        :param start_position: tuple representing the starting position of ship on the board
        :param orientation: the orientation of the ship ('v' - vertical, 'h' - horizontal)
        :return: None
        """

        self.name = name
        num_positions = SHIP_SIZES[name]
        self.positions = {}
        self.sunk = False

        for pos in range(num_positions):
            if orientation == VERTICAL:
                vertical_position, horizontal_position = start_position
                self.positions[(chr(ord(vertical_position) + pos), horizontal_position)] = False

            elif orientation == HORIZONTAL:
                vertical_position, horizontal_position = start_position
                self.positions[(vertical_position, horizontal_position + pos)] = False



class Game:

    ########## DO NOT EDIT #########

    _ship_types = ["carrier", "battleship", "cruiser", "submarine", "destroyer"]


    def display_board(self):
        """ Displays the current state of the board."""

        print()
        print("  " + ' '.join('{}'.format(i) for i in range(len(self.board))))
        for row_label in self.board.keys():
            print('{} '.format(row_label) + ' '.join(self.board[row_label]))
        print()

    ########## DO NOT EDIT #########


    def __init__(self, max_misses = MAX_MISSES):
        """ Creates a new game with max_misses possible missed guesses.
        The board is initialized in this function and ships are randomly
        placed on the board.

        :param max_misses: maximum number of misses allowed before game ends
        """



        self.max_misses = MAX_MISSES
        self.ships = []
        self.guesses = []
        self.board = {}
        self.initialize_board()
        self.create_and_place_ships()



    def update_game(self, guess_status, position):
        """Updates the game by modifying the board with a hit or miss
        symbol based on guess_status of position.

        :param guess_status: True when position is a hit, False otherwise
        :param position:  a (row,column) tuple guessed by user
        :return: None
        """

        row, column = position

        if guess_status == True and self.board[row][column] == BLANK_CHAR:
            self.board[row][column] = HIT_CHAR

        elif guess_status == False and self.board[row][column] == BLANK_CHAR:
            self.board[row][column] = MISS_CHAR


        if guess_status == False:
            self.guesses.append(position)


    def is_complete(self):
        """Checks to see if a Battleship game has ended. Returns True when the game is complete
        with a message indicating whether the game ended due to successfully sinking all ships
        or reaching the maximum number of guesses. Returns False when the game is not
        complete.

        :return: True on game completion, False otherwise
        """

        if len(self.guesses) == self.max_misses:
            print("SORRY! NO GUESSES LEFT.")
            return True

        ships_sunk = []

        for ship in self.ships:
            ships_sunk.append(ship.sunk)

        if ships_sunk == ([True] * len(SHIP_SIZES)):
            print("YOU WIN!")
            return True

        return False



    def check_guess(self, position):
        """Checks whether or not position is occupied by a ship. A hit is
        registered when position occupied by a ship and position not hit
        previously. A miss occurs otherwise.

        :param position: a (row,column) tuple guessed by user
        :return: guess_status: True when guess results in hit, False when guess results in miss
        """


        for ship in self.ships:
            for occupied_position in list(ship.positions.keys()):

                if occupied_position == position and ship.positions[occupied_position] == False:
                    ship.positions[occupied_position] = True
                    if list(ship.positions.values()) == ([True] * len(ship.positions)):
                        ship.sunk = True
                        print("You sunk the {}!".format(ship.name))
                    return True
        return False





    def get_guess(self):
        """Prompts the user for a row and column to attack. The
        return value is a board position in (row, column) format

        :return position: a board position as a (row, column) tuple
        """

        min_row_ord_allowed = ord(MIN_ROW_LABEL)
        max_row_ord_allowed = ord(MAX_ROW_LABEL)

        min_column_allowed = ROW_IDX
        max_column_allowed = NUM_COLS - COL_IDX

        row_checker = False
        column_checker = False


        while row_checker ==  False:
            user_row_input = input("Enter a row: ")
            if min_row_ord_allowed <= ord(user_row_input) <= max_row_ord_allowed:
                row_checker = True


        while column_checker == False:
            user_column_input = int(input("Enter a column: "))
            if min_column_allowed <= user_column_input <= max_column_allowed:
                column_checker = True

        return (user_row_input, user_column_input)



    def create_and_place_ships(self):
        """Instantiates ship objects with valid board placements.

        :return: None
        """
        for ship_name in self._ship_types:
            starting_position = get_random_position()
            size_ship = SHIP_SIZES[ship_name]
            orientation = self.place_ship(starting_position, size_ship)
            while orientation == None:
                starting_position = get_random_position()
                orientation = self.place_ship(starting_position, size_ship)

            ship = Ship(ship_name, starting_position, orientation)
            self.ships.append(ship)


    def place_ship(self, start_position, ship_size):
        """Determines if placement is possible for ship requiring ship_size positions placed at
        start_position. Returns the orientation where placement is possible or None if no placement
        in either orientation is possible.

        :param start_position: tuple representing the starting position of ship on the board
        :param ship_size: number of positions needed to place ship
        :return orientation: 'h' if horizontal placement possible, 'v' if vertical placement possible,
            None if no placement possible
        """

        horizontal_in_bounds = self.in_bounds(start_position, ship_size, HORIZONTAL)

        horizontal_overlaps = self.overlaps_ship(start_position, ship_size, HORIZONTAL)

        vertical_in_bounds = self.in_bounds(start_position, ship_size, VERTICAL)

        vertical_overlaps = self.overlaps_ship(start_position, ship_size, VERTICAL)

        if horizontal_in_bounds == True and horizontal_overlaps == False:
            return HORIZONTAL

        elif vertical_in_bounds == True and vertical_overlaps == False:
            return VERTICAL

        else:
            return None




    def overlaps_ship(self, start_position, ship_size, orientation):
        """Checks for overlap between previously placed ships and a potential new ship
        placement requiring ship_size positions beginning at start_position in the
        given orientation.

        :param start_position: tuple representing the starting position of ship on the board
        :param ship_size: number of positions needed to place ship
        :param orientation: the orientation of the ship ('v' - vertical, 'h' - horizontal)
        :return status: True if ship placement overlaps previously placed ship, False otherwise
        """

        current_ship_positions = []

        start_position_letter, start_position_number = start_position

        for num in range(ship_size):
            if orientation == VERTICAL:
                current_ship_positions.append((chr(ord(start_position_letter) + num), start_position_number))

            elif orientation == HORIZONTAL:
                current_ship_positions.append((start_position_letter, start_position_number + num))


        already_taken_positions = []

        for ship in self.ships:
            for position in list(ship.positions.keys()):
                already_taken_positions.append(position)


        for position1 in current_ship_positions:
            for position2 in already_taken_positions:

                if position1 == position2:
                    return True


        return False



    def in_bounds(self, start_position, ship_size, orientation):
        """Checks that a ship requiring ship_size positions can be placed at start position.

        :param start_position: tuple representing the starting position of ship on the board
        :param ship_size: number of positions needed to place ship
        :param orientation: the orientation of the ship ('v' - vertical, 'h' - horizontal)
        :return status: True if ship placement inside board boundary, False otherwise
        """

        start_position_letter, start_position_number = start_position

        if orientation == VERTICAL:
            if (ord(start_position_letter) + ship_size) > ord(MAX_ROW_LABEL):
                return False

        elif orientation == HORIZONTAL:
            if (start_position_number + ship_size) > (NUM_COLS - COL_IDX):
                return False

        return True






    def initialize_board(self):
        """Sets the board to it's initial state with each position occupied by
        a period ('.') string.

        :return: None
        """
        alphabets = []

        for num in range(NUM_COLS):
            alphabets.append(chr(ord(MIN_ROW_LABEL) + num))

        for letter in alphabets:
            self.board[letter] = ["."] * NUM_COLS




def end_program():
    """Prompts the user with "Play again (Y/N)?" The question is repeated
    until the user enters a valid response (Y/y/N/n). The function returns
    False if the user enters 'Y' or 'y' and returns True if the user enters
    'N' or 'n'.

    :return response: boolean indicating whether to end the program
    """

    user_input = input("Play again (Y/N)? ")

    allowed_inputs= "yYnN"

    while not user_input in allowed_inputs:
        user_input = input("Play again (Y/N)? ")

    if user_input == "Y" or user_input == "y":
        return False

    if user_input == "N" or user_input == "n":
        return True


def main():
    """Executes one or more games of Battleship."""

    play_battleship()


if __name__ == "__main__":
    main()
