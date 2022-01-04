"""
Module of stonehenge.

"""
import string as str_lib
import copy
from game import Game
from game_state import GameState


"""
A help class for StonehengeGame Board
"""


class StonehengeGameBoard:
    """
    Holding cells and leylines of stonehenge board

    board - holding cells
    h_leylines - holding horizontal leylines
    dl_leylines - holding downward leylines
    ul_leylines - holding upward leylines
    """
    board: list
    h_leylines: list
    dl_leylines: list
    ul_leylines: list

    def __init__(self, board: list, h_leylines: list, dl_leylines: list,
                 ul_leylines: list) -> None:
        self.board = board
        self.h_leylines = h_leylines
        self.dl_leylines = dl_leylines
        self.ul_leylines = ul_leylines


"""
An implementation of a state for StonehengeGame.

"""


class StonehengeState(GameState):
    """
    The state of a game at a certain point in time.
    """
    DUMMY_SYMBOL: str = '0'

    def __init__(self, is_p1_turn: bool, length: int, move: str = '',
                 shgb: StonehengeGameBoard = None) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.
        >>> p1 = StonehengeState(True, 2, '')
        >>> p1.board
        [['0', 'A', 'B'], ['C', 'D', 'E'], ['F', 'G', '0']]
        >>> p1.h_leylines
        [['@', 'A', 'B'], ['@', 'C', 'D', 'E'], ['@', 'F', 'G']]
        >>> p1.dl_leylines
        [['@', 'A', 'C'], ['@', 'B', 'D', 'F'], ['@', 'E', 'G']]
        >>> p1.ul_leylines
        [['@', 'F', 'C'], ['@', 'G', 'D', 'A'], ['@', 'E', 'B']]
        """
        super().__init__(is_p1_turn)
        self.length = length
        if move == '':
            # brand new state
            temp_board, temp_h_leylines, temp_dl_leylines, temp_ul_leylines = \
                self.build_board(length)
            self.board = copy.deepcopy(temp_board)
            self.h_leylines = copy.deepcopy(temp_h_leylines)
            self.dl_leylines = copy.deepcopy(temp_dl_leylines)
            self.ul_leylines = copy.deepcopy(temp_ul_leylines)
        elif shgb is not None:
            current_player_id = '2' if is_p1_turn else '1'
            # new game state after make a move
            temp_board, temp_h_leylines, temp_dl_leylines, temp_ul_leylines = \
                self.update_board(current_player_id, move, shgb)
            self.board = copy.deepcopy(temp_board)
            self.h_leylines = copy.deepcopy(temp_h_leylines)
            self.dl_leylines = copy.deepcopy(temp_dl_leylines)
            self.ul_leylines = copy.deepcopy(temp_ul_leylines)

    def build_board(self, length: int) -> (list, list, list, list):
        """
        To build the stonehenge game board with the given length
        # first list is to build the board
        # second list is h_leylines
        # third list is dl_leylines
        # fourth list is ul_leylines
        >>> p1 = StonehengeState(True, 2, '')
        >>> p1.length
        2
        >>> blist, hlist, downlist, uplist = p1.build_board(2)
        >>> blist
        [['0', 'A', 'B'], ['C', 'D', 'E'], ['F', 'G', '0']]
        >>> hlist
        [['@', 'A', 'B'], ['@', 'C', 'D', 'E'], ['@', 'F', 'G']]
        >>> downlist
        [['@', 'A', 'C'], ['@', 'B', 'D', 'F'], ['@', 'E', 'G']]
        >>> uplist
        [['@', 'F', 'C'], ['@', 'G', 'D', 'A'], ['@', 'E', 'B']]

        """
        alph_letters = list(str_lib.ascii_uppercase)

        h_board_ley_lines = []
        dl_board_ley_lines = []
        ul_board_ley_lines = []

        # the board will be row x column = (length + 1) x (length + 1)
        # with dummy_ssymbol filling in the empty spots
        new_board = []
        running_count = 0
        for i in range(2, length + 3):
            if i <= length + 1:
                temp = alph_letters[running_count:running_count + i]
                temp_len = len(temp)
                if length + 1 - temp_len > 0:
                    new_board.append([self.DUMMY_SYMBOL] *
                                     (length + 1 - temp_len))
                    new_board[i - 2].extend(temp[:])
                else:
                    new_board.append(temp[:])
                running_count += i
            else:
                new_board.append(alph_letters[running_count:(running_count +
                                                             length)])
                new_board[length].append(self.DUMMY_SYMBOL)

        # build h_board_ley_lines
        for i in range(len(new_board)):
            h_board_ley_lines.append(['@'])
            h_board_ley_lines[i].extend([x for x in new_board[i]
                                         if x != self.DUMMY_SYMBOL])

        # builld dl_board_ley_lines
        # starting with letter 'A'
        temp = list(['@', 'A'])
        i = length - 1  # column index of 'A'
        row = 1
        while i - row >= 0:
            temp.append(new_board[row][i - row])
            row += 1
        dl_board_ley_lines.append(temp)
        # continue with the last letter in each row except last row
        for i in range(length):
            row = i
            running_count = 0
            temp = list('@')
            while row <= length:
                temp.append(new_board[row][length - running_count])
                row += 1
                running_count += 1
            dl_board_ley_lines.append(temp)

        # build ul_board_ley_lines
        for column in range(length + 1):
            row = length
            temp = list('@')
            while row >= 0:
                if new_board[row][column] != self.DUMMY_SYMBOL:
                    temp.append(new_board[row][column])
                row -= 1
            ul_board_ley_lines.append(temp)

        return (new_board, h_board_ley_lines, dl_board_ley_lines,
                ul_board_ley_lines)

    def update_board(self, player_id: str, move: str,
                     shgb: StonehengeGameBoard) -> (list, list, list, list):
        """shgb.: StonehengeGameBoard
        board: list, h_leylines,
                     dl_leylines, ul_leylines
        doc string
        """
        self.update_ley_lines(player_id, shgb.h_leylines, move)
        self.update_ley_lines(player_id, shgb.dl_leylines, move)
        self.update_ley_lines(player_id, shgb.ul_leylines, move)

        for row in range(self.length + 1):
            if move in shgb.board[row]:
                move_index = shgb.board[row].index(move)
                shgb.board[row][move_index] = player_id

        return (shgb.board, shgb.h_leylines, shgb.dl_leylines,
                shgb.ul_leylines)

    def update_ley_lines(self, player_id: str, ley_lines: list,
                         move: str) -> None:
        """
        doc string
        """
        move_row = -1
        move_index = -1
        for row in range(self.length + 1):
            if move in ley_lines[row]:
                move_index = ley_lines[row].index(move)
                move_row = row
                ley_lines[row][move_index] = player_id
                break
        if move_row > -1 and move_index > -1 and ley_lines[move_row][0] == '@':
            count = len([x for x in ley_lines[move_row] if x == player_id])
            if count >= (len(ley_lines[move_row]) - 1) / 2:
                ley_lines[move_row][0] = player_id

    def is_over(self) -> bool:
        """
        doc string
        """
        total_leylines = (self.length + 1) * 3
        claimed_by_p1 = 0
        claimed_by_p2 = 0
        for i in range(self.length + 1):
            if self.h_leylines[i][0] == '1':
                claimed_by_p1 += 1
            elif self.h_leylines[i][0] == '2':
                claimed_by_p2 += 1
            if self.dl_leylines[i][0] == '1':
                claimed_by_p1 += 1
            elif self.dl_leylines[i][0] == '2':
                claimed_by_p2 += 1
            if self.ul_leylines[i][0] == '1':
                claimed_by_p1 += 1
            elif self.ul_leylines[i][0] == '2':
                claimed_by_p2 += 1

        return (claimed_by_p1 >= total_leylines / 2) or \
               (claimed_by_p2 >= total_leylines / 2)

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.
        >>> state1 = StonehengeState(True, 1, '')
        >>> print(str(state1))
              @   @
             /   /
        @ - A - B
            \\\\ / \\\\
         @ - C   @
              \\\\
               @
        >>> state2 = StonehengeState(True, 3, '')
        >>> print(str(state2))
                @   @
               /   /
          @ - A - B   @
              / \\\\ / \\\\ /
         @ - C - D - E   @
             / \\\\ / \\\\ / \\\\ /
        @ - F - G - H - I
            \\\\ / \\\\ / \\\\ / \\\\
         @ - J - K - L   @
              \\\\  \\\\  \\\\
               @   @   @
        """
        # return "Current total: {}".format(self.current_total)
        result = ''
        sep_lenth = 3
        result += ' ' * (len(self.board[0]) + 4) + self.dl_leylines[0][0] + \
                  ' ' * sep_lenth + self.dl_leylines[1][0] + '\n'
        result += ' ' * (len(self.board[0]) + 3) + '/' \
                  + ' ' * sep_lenth + '/' + '\n'

        for row in range(self.length + 1):
            result += ' ' * (self.length - len(self.h_leylines[row]) + 2) + \
                      self.h_leylines[row][0]
            for column in range(0, self.length + 1):
                if self.board[row][column] != self.DUMMY_SYMBOL:
                    result += ' - ' + self.board[row][column]
                if row + 2 <= self.length and column == self.length:
                    result += '   ' + self.dl_leylines[row + 2][0]
                if row == self.length and column == self.length:
                    result += '   ' + self.ul_leylines[row][0]
            result += '\n'
            # symbols between rows
            if row != self.length and row < (len(self.dl_leylines[0]) - 2):
                result += ' ' * (self.length - len(self.h_leylines[row]) + 5)
                for i in range(len(self.h_leylines[row]) +
                               len(self.h_leylines[row + 1]) - 2):
                    result += ' ' + '/' if i % 2 == 0 else ' ' + '\\\\'
                result += '\n'
            elif row != self.length and row >= (len(self.dl_leylines[0]) - 2):
                result += ' ' * (self.length - len(self.h_leylines[row]) + 5)
                for i in range(len(self.h_leylines[row]) +
                               len(self.h_leylines[row + 1]) - 2):
                    result += ' ' + '\\\\' if i % 2 == 0 else ' ' + '/'
                result += '\n'
        result += ' ' * 5
        result += ' \\\\ ' * self.length
        # remove the extra empty space at the end
        result = result[0:-1]
        result += '\n'
        result += ' ' * 4
        for i in range(self.length):
            result += '   ' + self.ul_leylines[i][0]
        return result

    def get_possible_moves(self) -> list:
        """
        Return all possible moves that can be applied to this state.
        >>> state1 = StonehengeState(True, 1, '')
        >>> state1.get_possible_moves()
        ['A', 'B', 'C']
        >>> state2 = state1.make_move('A')
        >>> state2.get_possible_moves()
        []
        """
        moves = []
        if self.is_over():
            return moves
        for row in range(self.length + 1):
            for column in range(1, len(self.h_leylines[row])):
                if self.h_leylines[row][column].isalpha():
                    moves.append(self.h_leylines[row][column])
        return moves

    def make_move(self, move: str) -> "StonehengeState":
        """
        Return the GameState that results from applying move to this GameState.
        >>> p1 = StonehengeState(True, 2, '')
        >>> p1.make_move('A')
        Current Player is: P2 - Total Leylines: 9
        """
        board_d_copy = copy.deepcopy(self.board)
        h_leylines_d_copy = copy.deepcopy(self.h_leylines)
        dl_leylines_d_copy = copy.deepcopy(self.dl_leylines)
        ul_leylines_d_copy = copy.deepcopy(self.ul_leylines)
        shgb = StonehengeGameBoard(board_d_copy, h_leylines_d_copy,
                                   dl_leylines_d_copy, ul_leylines_d_copy)
        new_state = StonehengeState(not self.p1_turn, self.length, move,
                                    shgb)
        return new_state

    def __repr__(self) -> str:
        """
        Return a representation of this state (which can be used for
        equality testing).
        >>> p1 = StonehengeState(True, 2, '')
        >>> p1.__repr__()
        'Current Player is: P1 - Total Leylines: 9'
        """
        # return "P1's Turn: {} - Total: {}".format(self.p1_turn,
        # self.current_total)
        if self.p1_turn:
            player_name, player_id = "P1", "1"
        else:
            player_name, player_id = "P2", "2"

        claimed_by_this_player = 0
        for i in range(self.length + 1):
            if self.h_leylines[i][0] != player_id:
                claimed_by_this_player += 1
            if self.dl_leylines[i][0] != player_id:
                claimed_by_this_player += 1
            if self.ul_leylines[i][0] != claimed_by_this_player:
                claimed_by_this_player += 1

        return "Current Player is: {} - Total Leylines: {}".format(
            player_name, claimed_by_this_player)

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.
        >>> p1 = StonehengeState(True, 1, '')
        >>> p1.rough_outcome()
        1
        """
        if any([self.make_move(move).is_over() for move in
                self.get_possible_moves()]):
            return self.WIN
        new_states = [self.make_move(move) for move in
                      self.get_possible_moves()]
        for state in new_states:
            if not all([state.make_move(next_move).is_over() for next_move in
                        state.get_possible_moves()]):
                return self.DRAW
        return self.LOSE


class StonehengeGame(Game):
    """
    Abstract class for a game to be played with two players.
    """

    def __init__(self, p1_starts):
        """
        Initialize this Game, using p1_starts to find who the first player is.

        :param p1_starts: A boolean representing whether Player 1 is the first
                          to make a move.
        :type p1_starts: bool
        """
        length = int(input("Enter the stonehenge grid side-length: "))
        self.current_state = StonehengeState(p1_starts, length)

    def get_instructions(self):
        """
        Return the instructions for this Game.

        :return: The instructions for this Game.
        :rtype: str
        """
        instructions = "Players take turns to claim cells in the Stonehenge "  \
                       "game. The first player to claim atleast half of the " \
                       "ley-lines is the winner!"
        return instructions

    def is_over(self, state: StonehengeState) -> bool:
        """
        Return whether or not this game is over.

        :return: True if the game is over, False otherwise.
        :rtype: bool
        """
        return state.is_over()

    def is_winner(self, player):
        """
        Return whether player has won the game.

        Precondition: player is 'p1' or 'p2'.

        :param player: The player to check.
        :type player: str
        :return: Whether player has won or not.
        :rtype: bool
        """
        return (self.current_state.get_current_player_name() != player
                and self.is_over(self.current_state))

    def str_to_move(self, string: str) -> str:
        """
        Return the move that string represents. If string is not a move,
        return an invalid move.
        """
        return string.strip().upper()


if __name__ == "__main__":
    from python_ta import check_all
    import doctest

    check_all(config="a2_pyta.txt")
    doctest.testmod()
