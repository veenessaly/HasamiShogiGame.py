# Description: using the  class HasamiShogiGame, this program plays the game
# HasamiShogi (Variant) with Red and Black pawns.  If a players piece is moved
# and the opponents pieces are between the players piece and another of the players
# piece, the pieces are captured. Also, if an opponents piece is between two player
# pieces in a corner, it is captured. The game ends when a player has 0 or 1 pieces
# left

class HasamiShogiGame():
    def __init__(self):
        """initializes private data members for HasamiShogiGame.
        Initializes the board with the Red and Black pieces in the default position
        in the unfinished state
        with the initial active player as BLACK
        with the initial number of pieces for red and black being 9 each
        and an empty list to contain any captured pieces, with seperate lists for 'RED' and 'BLACK'"""
        self._board = [
            [[" "], ["1"], ["2"], ["3"], ["4"], ["5"], ["6"], ["7"], ["8"], ["9"]],
            [["a"], ["R"], ["R"], ["."], ["R"], ["R"], ["R"], ["R"], ["R"], ["R"]],
            [["b"], ["."], ["."], ["."], ["."], ["."], ["."], ["."], ["."], ["."]],
            [["c"], ["B"], ["."], ["."], ["."], ["."], ["."], ["."], ["."], ["."]],
            [["d"], ["."], ["."], ["."], ["."], ["."], ["."], ["."], ["."], ["."]],
            [["e"], ["."], ["."], ["."], ["."], ["."], ["."], ["."], ["."], ["."]],
            [["f"], ["."], ["."], ["."], ["."], ["."], ["."], ["."], ["."], ["."]],
            [["g"], ["R"], ["."], ["."], ["."], ["."], ["."], ["."], ["."], ["R"]],
            [["h"], ["."], ["."], ["."], ["."], ["."], ["."], ["."], ["."], ["."]],
            [["i"], ["B"], ["."], ["B"], ["B"], ["B"], ["B"], ["."], ["R"], ["B"]]
        ]
        self._state = "UNFINISHED"
        self._active_player = "BLACK"
        self._black_pieces = 9
        self._red_pieces = 9
        self._black_captured_by_red = []
        self._red_captured_by_black = []

    def print_board(self):
        """prints board"""
        row = 0
        while row < 10:
            line = " "
            for value in self._board[row]:
                for square in value:
                    line += square + " "
            row += 1
            print(line)

    def get_game_state(self):
        """takes no parameters. Checks if the game is unfinished or if either red or black has won."""
        return self._state

    def change_game_state(self, winner):
        """takes one parameter: winner: either 'RED' or 'BLACK', the winner of the game
        (when the opponent has all but one of their pieces captured). Purpose: to change the game states from
        'UNFINISHED' to either 'RED_WON' or 'BLACK_WON' dependingon the input from the parameter.
         returns: the game state (initialized with the board) changing to either 'RED_WON' or 'BLACK_WON'"""
        if winner == "BLACK":
            self._state = "BLACK_WON"
        elif winner == "RED":
            self._state = "RED_WON"

    def get_active_player(self):
        """takes no parameters and checks whose turn it is. returns whose turn it is - either 'RED' or 'BLACK'"""
        return self._active_player

    def change_active_player(self):
        """takes no parameters.
        sets current_player equal to the player who is currently active (either 'RED' or 'BLACK')
        Methods purpose is to change turns when a players turn is over to their opponent.
        It marks the current_player as the other player (switches from red to black or vice versa)"""
        current_player = self._active_player
        if current_player == 'BLACK':
            self._active_player = 'RED'
        elif current_player == 'RED':
            self._active_player = 'BLACK'

    def get_num_captured_pieces(self, player):
        """takes one parameter: player = 'RED' or 'BLACK'. Purpose: Checks how many pieces
        each player has captured and returns the number of pieces of that color that have been captured"""
        if player == "BLACK":
            captured_pieces = 9 - self._black_pieces
        elif player == 'RED':
            captured_pieces = 9 - self._red_pieces
        return captured_pieces

    def set_num_captured_pieces(self, player, num_captured_pieces):
        """takes two parameters: player: 'RED' or "BLACK' and num_captured_pieces: number of each players
        captured pieces. the Purpose is to change the number of pieces each player has had captured
        (initialized as 9 for each player when the game board is created and
        changes the number of captured pieces of the indicated player"""
        if player == "BLACK":
            remaining_pieces = self._black_pieces - num_captured_pieces
            self._black_pieces = remaining_pieces
        elif player == "RED":
            remaining_pieces = self._red_pieces - num_captured_pieces
            self._red_pieces = remaining_pieces

    def make_move(self, moved_from, moved_to):
        """takes two parameters:
        strings that represent the square moved from and the square moved to
        (row/column current, row/column move to).

        Purpose: If possible (ie if is a legal move), move the piece from the 1st parameter to the 2nd parameter

        returns:

        -False if:
        --the square being moved from does not contain a piece belonging to the players whose turn it is
        (check if get_square_occupant matches the moved_from pieces player ('RED' or "BLACK') or if there
        is even a piece there)
        --or if the indicated move is not legal (using legal_move)
        --or if the game has already been won (using get_game_state)

        -True and:
        --makes the indicated move (using change_square_occupant)
        --removes any captured pieces (using method remove_captured)
        --updates the game state (if necessary) (using method change_game_state)
        --update whose turn it is (using change_active_player)"""
        square_moved_from = self.get_square_from(moved_from)
        square_moved_to = self.get_square_to(moved_to)
        occupant_moved_from = self.get_square_occupant(moved_from)

        if self.legal_move(occupant_moved_from, moved_from, moved_to) is False:  # if not a legal move
            return False
        elif self.get_game_state() != "UNFINISHED": # if game has been won already
            return False
        elif self.get_square_occupant(moved_from) != self._active_player:
            return False
        else:
            # make the indicated move (using change_square_occupant)
            self.change_square_occupant(occupant_moved_from, moved_from, moved_to)

            # check for and remove any captured pieces (using method remove_captured)
            self.remove_captured(moved_to)

            # checks how many pieces opponent has left and updates the game state if necessary
            # (Using method change_game_state)
            player = self._active_player
            self.winner(player)

            # Update whose turn it is (using change active player)
            self.change_active_player()
            return True

    def winner(self, player):
        """checks how many pieces opponent has left and updates the game state if necessary (using change game state method)"""
        black_captured = len(self._black_captured_by_red)
        red_captured = len(self._red_captured_by_black)
        if player == "RED":
            self._black_pieces = 9 - black_captured
        elif player == "BLACK":
            self._red_pieces = 9 - red_captured
        if player == "RED":
            if self._black_pieces <= 1:
                self.change_game_state("RED")
        elif player == "BLACK":
            if self._red_pieces <= 1:
                self.change_game_state("BLACK")

    def get_square_from(self, moved_from):
        """using the row and column give by the player that they want to move their piece from, returns
        the value in the square"""
        for value in moved_from:
            if value == "a" or value == "b" or value == "c" or value == "d" or value == "e" or \
                    value == "f" or value == "g" or value == "h" or value == "i":
                row_from = value
            else:
                column_from = int(value)
        row_number = self.letters_to_numbers(row_from)
        square_from = self._board[row_number][column_from]
        return square_from

    def get_square_to(self, moved_to):
        """using the row and column give by the player that they want to move their piece to, returns
        the value in the square"""
        for value in moved_to:
            if value == "a" or value == "b" or value == "c" or value == "d" or value == "e" or \
                    value == "f" or value == "g" or value == "h" or value == "i":
                row_to = value
            else:
                column_to = int(value)
        row_number = self.letters_to_numbers(row_to)
        square_to = self._board[row_number][column_to]
        return square_to

    def letters_to_numbers(self, row):
        """method that takes a letter representing the row and converts the row letter to a
         number for indexing"""
        if row == "a":
            row = 1
        elif row == "b":
            row = 2
        elif row == "c":
            row = 3
        elif row == "d":
            row = 4
        elif row == "e":
            row = 5
        elif row == "f":
            row = 6
        elif row == "g":
            row = 7
        elif row == "h":
            row = 8
        elif row == "i":
            row = 9
        return row

    def get_row(self, square):
        """takes a square and returns the row component"""
        for value in square:
            if value == "a" or value == "b" or value == "c" or value == "d" or value == "e" or \
                    value == "f" or value == "g" or value == "h" or value == "i":
                row = value
                row = self.letters_to_numbers(row)
                return row

    def get_column(self, square):
        """takes a square and returns the column"""
        for value in square:
            if value == "1" or value == "2" or value == "3" or value == "4" or value == "5" or value == "6" or \
                    value == "7" or value == "8" or value == "9":
                column = int(value)
                return column

    def legal_move(self, player, moved_from, moved_to):
        """takes two parameters: moved_to (row/column) and moved_from (row/column)
        Purpose is to check to see if it is a legal move following the rules: a piece can move to any number of
        empty cells vertically or horizontally.
        -It will first check if the move is only vertical or only horizontal (ie that it is not diagonal), make
        sure there are no other pieces between moved from and moved to squares, and that the square the piece
        is being moved into is empty.
        Returns False if the piece does not move only vertically or horizontally or if there is another
        piece in it's way (not able to jump over pieces and the square it's being moved to is occupied).
        Returns true otherwise"""

        # check if a legal move:
        moved_from_row = self.get_row(moved_from)
        moved_from_column = self.get_column(moved_from)
        moved_to_row = self.get_row(moved_to)
        moved_to_column = self.get_column(moved_to)
        occupant = self.get_square_occupant(moved_to)

        # make sure moved_from and moved_to are either vertical or horizontal, not diagonal
        # (if row and column are both different, then it is a diagonal move. either row or column have to
        # be equal for it to be a valid move)
        if moved_from_row != moved_to_row and moved_from_column != moved_to_column:
            return False

        # iterate through the appropriate row or column to make sure that it doesn't go
        # through/over any other pieces (as the game rules don't allow it to jump over another piece).

        # row move
        elif moved_from_row == moved_to_row:
            # left to right row
            if moved_from_column < moved_to_column:
                for square in self._board[moved_from_row][moved_from_column+1:moved_to_column]:
                        # make sure there are no other pieces in between these moved_from and moved_to
                        # for value in square:
                    if square == "R" or square == "B":
                        return False

            # right to left row
            elif moved_from_column > moved_to_column:
                for square in self._board[moved_from_row][moved_to_column:moved_from_column]:
                    if square == "R" or square == "B":
                        return False

        # column
        elif moved_from_column == moved_to_column:
            # up to down column
            if moved_from_row < moved_to_row:
                for line in self._board[moved_from_row+1:moved_to_row+1]:
                    for value in line[moved_from_column]:
                        if value == "R" or value == "B":
                            return False

            # down to up column
            elif moved_from_row > moved_to_row:
                for line in self._board[moved_to_row:moved_from_row]:
                    for value in line[moved_from_column]:
                        if value == "R" or value == "B":
                            return False

        # check if the moved_to spot has any occupant already
        if occupant != "NONE":
            return False
        elif occupant == "NONE":
            return True

    def remove_captured(self, square_moved_to):
        """takes one parameter:
        a string representing a square being moved to (row/column)

        Purpose: used with make_move method: checks to see if there are any possible
        opponent pieces that could be captured as per the rules of the game

        returns:
        removes piece(s) that need to be captured from game board square(s)"""
        occupant = self.get_square_occupant(square_moved_to)
        occupant_initial = self.get_player_initial(occupant)
        row = self.get_row(square_moved_to)
        column = self.get_column(square_moved_to)

        # row left to right
        found = False
        piece_dict = {} # key = column, value = value in square
        column_on = column
        for square in self._board[row][column+1::]:
            for item in square:
                if not found and column_on <=9:
                    column_on += 1
                    if item != occupant_initial:
                        piece_dict[column_on] = item
                    elif item == occupant_initial:
                        found = True
                        for key, value in piece_dict.items():
                            if value != occupant_initial or value != ".":
                                if row == 1 or row == 9:
                                    if key == 1 or key == 9:
                                        self.corners(square_moved_to)
                                elif value == "R":
                                    self._red_captured_by_black.append(value)
                                    self.captured_square_occupant(row, key)
                                elif value == "B":
                                    self._black_captured_by_red.append(value)
                                    self.captured_square_occupant(row, key)


        #row right to left
        found = False
        piece_dict = {}
        column_on = column-1
        while not found and column_on >= 1:
            for block in self._board[row][column_on]:
                for square in block:
                    if square != occupant_initial:
                        piece_dict[column_on] = square
                        column_on -= 1
                    elif square == occupant_initial:
                        found = True
                        for key, value in piece_dict.items():
                            if value != occupant_initial or value != ".":
                                if row == 1 or row == 9:
                                    if key == 1 or key == 9:
                                        self.corners(square_moved_to)
                                elif value == "R":
                                    self._red_captured_by_black.append(value)
                                    self.captured_square_occupant(row, key)
                                elif value == "B":
                                    self._black_captured_by_red.append(value)
                                    self.captured_square_occupant(row, key)


        #column up to down
        found = False
        piece_list = {}
        row_on = row
        for line in self._board[row+1::]:
            if not found and row_on <= 9:
                for square in line[column]:
                    if square != occupant_initial:
                        piece_dict[row_on] = square
                        row_on += 1
                    elif square == occupant_initial:
                        found = True
                        for key, value in piece_dict.items():
                            if value != occupant_initial or value != ".":
                                if key == 1 or key == 9:
                                    if column == 1 or column == 9:
                                        self.corners(square_moved_to)
                                elif value == "R":
                                    self._red_captured_by_black.append(value)
                                    self.captured_square_occupant(key, column)
                                elif value == "B":
                                    self._black_captured_by_red.append(value)
                                    self.captured_square_occupant(key, column)

        #column down to up
        found = False
        piece_dict= {} #key = row  value = value in square
        row_on = row -1
        while not found and row_on >= 1:
            row_check = self._board[row_on]
            block = row_check[column]
            for square in block:
                if square != occupant_initial:
                    piece_dict[row_on] = square
                    row_on -= 1
                elif square == occupant_initial:
                    found = True
                    for key, value in piece_dict.items():
                        if value != occupant_initial or value != ".":
                            if value != occupant_initial or value != ".":
                                if key == 1 or key == 9:
                                    if column == 1 or column == 9:
                                        self.corners(square_moved_to)
                            elif value == "R":
                                self._red_captured_by_black.append(value)
                                self.captured_square_occupant(key, column)
                            elif value == "B":
                                self._black_captured_by_red.append(value)
                                self.captured_square_occupant(key, column)

        if row == 1 or row == 9 or column == 1 or column == 9:
            self.corners(square_moved_to)

    def corners(self, square_moved_to):
        """takes as a parameter the square the piece was moved to and checks if it is near a corner.
        if there is a corner piece that is surrounded by the opponents pieces, will be removed"""
        occupant = self.get_square_occupant(square_moved_to)
        occupant_initial = self.get_player_initial(occupant)
        row = self.get_row(square_moved_to)
        column = self.get_column(square_moved_to)

        # left upper corner column 1
        if column == 1:
            for block in self._board[1][1]:
                for unit in block:
                    if unit != occupant_initial or unit != ".":
                        found = False
                        piece_dict = {} # key = column, value = value in square
                        column_on = column
                        for square in self._board[1][column+1::]:
                            for item in square:
                                if not found and column_on <=9:
                                    column_on += 1
                                    if item != occupant_initial:
                                        piece_dict[column_on] = item
                                    elif item == occupant_initial:
                                        found = True
                                        if unit == "R":
                                            self._red_captured_by_black.append(item)
                                            self.captured_square_occupant(1, 1)
                                        elif unit == "B":
                                            self._black_captured_by_red.append(item)
                                            self.captured_square_occupant(1, 1)

        # left upper corner column 2
        if column == 2 or column == 3 or column == 4 or column == 5 or column == 6 or column == 7\
                or column == 8 or column ==9:
            for block in self._board[1][1]:
                for unit in block:
                    if unit != occupant_initial or unit != ".":
                        found = False
                        piece_dict = {}  # key = column, value = value in square
                        column_on = column
                        for list in self._board[row+1::]:
                            for square in list[1]:
                                for item in square:
                                    if not found and column_on <= 9:
                                        column_on += 1
                                        if item != occupant_initial:
                                            piece_dict[column_on] = item
                                        elif item == occupant_initial:
                                            found = True
                                            if unit == "R":
                                                self._red_captured_by_black.append(item)
                                                self.captured_square_occupant(1, 1)
                                            elif unit == "B":
                                                self._black_captured_by_red.append(item)
                                                self.captured_square_occupant(1, 1)

        # left lower corner column 1
        if column == 1:
            for block in self._board[9][1]:
                for unit in block:
                    if unit != occupant_initial or unit != ".":
                        found = False
                        piece_dict = {} # key = column, value = value in square
                        column_on = column
                        for square in self._board[9][column+1::]:
                            for item in square:
                                if not found and column_on <=9:
                                    column_on += 1
                                    if item != occupant_initial:
                                        piece_dict[column_on] = item
                                    elif item == occupant_initial:
                                        found = True
                                        if unit == "R":
                                            self._red_captured_by_black.append(item)
                                            self.captured_square_occupant(9, 1)
                                        elif unit == "B":
                                            self._black_captured_by_red.append(item)
                                            self.captured_square_occupant(9, 1)
        #left lower corner column 2
        if column == 2 or column == 3 or column == 4 or column == 5 or column == 6 or column == 7\
                or column == 8 or column ==9:
            for block in self._board[9][1]:
                for unit in block:
                    if unit != occupant_initial or unit != ".":
                        found = False
                        piece_dict = {}  # key = row  value = value in square
                        row_on = row - 1
                        while not found and row_on >= 1:
                            row_check = self._board[row_on]
                            block = row_check[1]
                            for square in block:
                                if square != occupant_initial:
                                    piece_dict[row_on] = square
                                    row_on -= 1
                                elif square == occupant_initial:
                                    found = True
                                    if unit == "R":
                                        self._red_captured_by_black.append(unit)
                                        self.captured_square_occupant(9, 1)
                                    elif unit == "B":
                                        self._black_captured_by_red.append(unit)
                                        self.captured_square_occupant(9, 1)

        # right upper corner column 9
        if column == 9:
            for block in self._board[1][9]:
                for unit in block:
                    if unit != occupant_initial or unit != ".":
                        found = False
                        piece_dict = {}
                        column_on = column - 1
                        while not found and column_on >= 1:
                            for item in self._board[row][column_on]:
                                for square in item:
                                    if square != occupant_initial:
                                        piece_dict[column_on] = square
                                        column_on -= 1
                                    elif square == occupant_initial:
                                        found = True
                                        if unit == "R":
                                            self._red_captured_by_black.append(item)
                                            self.captured_square_occupant(1, 9)
                                        elif unit == "B":
                                            self._black_captured_by_red.append(item)
                                            self.captured_square_occupant(1, 9)

        # right upper corner column 8
        if column == 8:
            for block in self._board[1][9]:
                for unit in block:
                    if unit != occupant_initial or unit != ".":
                        found = False
                        piece_dict = {}  # key = column, value = value in square
                        column_on = column
                        for list in self._board[row+1::]:
                            for square in list[9]:
                                for item in square:
                                    if not found and column_on <= 9:
                                        column_on += 1
                                        if item != occupant_initial:
                                            piece_dict[column_on] = item
                                        elif item == occupant_initial:
                                            found = True
                                            if unit == "R":
                                                self._red_captured_by_black.append(item)
                                                self.captured_square_occupant(1, 9)
                                            elif unit == "B":
                                                self._black_captured_by_red.append(item)
                                                self.captured_square_occupant(1, 9)

        #right lower corner column 9
        if column == 9:
            for block in self._board[9][9]:
                for unit in block:
                    if unit != occupant_initial or unit != ".":
                        found = False
                        piece_dict = {}  # key = row  value = value in square
                        row_on = row - 1
                        while not found and row_on >= 1:
                            row_check = self._board[row_on]
                            block = row_check[9]
                            for square in block:
                                if square != occupant_initial:
                                    piece_dict[row_on] = square
                                    row_on -= 1
                                elif square == occupant_initial:
                                    found = True
                                    if unit == "R":
                                        self._red_captured_by_black.append(unit)
                                        self.captured_square_occupant(9, 9)
                                    elif unit == "B":
                                        self._black_captured_by_red.append(unit)
                                        self.captured_square_occupant(9, 9)


        #right lower corner column 8
        if column == 2 or column == 3 or column == 4 or column == 5 or column == 6 or column == 7 \
                or column == 8 or column == 9:
            for block in self._board[9][9]:
                for unit in block:
                    if unit != occupant_initial or unit != ".":
                        found = False
                        piece_dict = {}  # key = row  value = value in square
                        row_on = row - 1
                        while not found and row_on >= 1:
                            row_check = self._board[row_on]
                            block = row_check[9]
                            for square in block:
                                if square != occupant_initial:
                                    piece_dict[row_on] = square
                                    row_on -= 1
                                elif square == occupant_initial:
                                    found = True
                                    if unit == "R":
                                        self._red_captured_by_black.append(unit)
                                        self.captured_square_occupant(9, 9)
                                    elif unit == "B":
                                        self._black_captured_by_red.append(unit)
                                        self.captured_square_occupant(9, 9)

    def get_square_occupant(self, square):
        """takes one parameter, square, a string representing a square. This method checks to see
        which (if any) player is occupying the indicated square and returns 'RED', 'BLACK', or 'NONE',
        depending on whether the specified square is occupied by a red piece, a black piece, or neither"""
        for value in square:
            if value == "a" or value == "b" or value == "c" or value == "d" or value == "e" or \
                    value == "f" or value == "g" or value == "h" or value == "i":
                row = value
            else:
                column = int(value)
        row_number = self.letters_to_numbers(row)
        square_occupant = self._board[row_number][column]
        for occupant in square_occupant:
            if occupant == "R":
                occupant = "RED"
            elif occupant == "B":
                occupant = "BLACK"
            else:
                occupant = "NONE"
        return occupant

    def change_square_occupant(self, player, square_moved_from, square_moved_to):
        """takes two parameters: the player making the move and a string representing a square where a
         piece is to be moved to. Purpose: To move the indicated piece to the appropriate square
         (legal_move method already checked first to see if empty)"""
        moved_to_row = self.get_row(square_moved_to)
        moved_to_column = self.get_column(square_moved_to)
        moved_from_row = self.get_row(square_moved_from)
        moved_from_column = self.get_column(square_moved_from)
        player = self.get_player_initial(player)

        # moved piece to new square (already checked if legal move) and replaces location with "."
        self._board[moved_to_row][moved_to_column] = [player]
        self._board[moved_from_row][moved_from_column] = ["."]

    def captured_square_occupant(self, row, column):
        """takes as a parameter the square that needs to be changed to empty because
        the piece that was their was captured"""
        self._board[row][column] = ["."]

    def get_player_initial(self, player):
        """takes as a parameter the player and returns the initial associated with that player"""
        if player == "BLACK":
            return "B"
        elif player == "RED":
            return "R"

