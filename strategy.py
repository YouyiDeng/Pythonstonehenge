"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
from typing import Any, List, Union
from random import randint
from game import Game
from game_state import GameState


# TODO: Adjust the type annotation as needed.
def interactive_strategy(game: Any) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def rough_outcome_strategy(game: Any) -> Any:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.

    NOTE: game.rough_outcome() should do the following:
        - For a state that's over, it returns the score for the current
          player of that state.
        - For a state that's not over:
            - If there is a move that results in the current player winning,
              return 1.
            - If all moves result in states where the other player can
              immediately win, return -1.
            - Otherwise; return a number between -1 and 1 corresponding to how
              'likely' the current player will win from the current state.

        In essence: rough_outcome() will only look 1 or 2 states ahead to
        'guess' the outcome of the game, but no further. It's better than
        random, but worse than minimax.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2  # Temporarily -- just so we can replace this easily later

    # Get the move that results in the lowest rough_outcome for the opponent
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)

        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move

    # Return the move that resulted in the best rough_outcome
    return best_move


# TODO: Implement a recursive version of the minimax strategy.
def minimax_recursive_strategy(game: Game) -> Any:
    """
    doc string
    """
    current_state = game.current_state
    current_player = current_state.get_current_player_name()
    move = get_mr_best_move(game, current_state, current_player)
    # restore back to original state
    game.current_state = current_state
    return game.str_to_move(str(move))


def get_mr_best_move(game: Game, state: GameState, this_player: str) \
        -> Any:
    """
    doc string
    """
    possible_moves = state.get_possible_moves()
    score_list = []
    best_score = get_mr_score(game, state, this_player, 0, score_list)
    candidate = []

    for i in range(len(score_list)):
        if score_list[i] == best_score:
            candidate.append(possible_moves[i])
    if not candidate:
        return ''
    return candidate[randint(0, len(candidate) - 1)]


def get_mr_score(game: Game, state: GameState, this_player: str, depth: int,
                 score_list: list) -> float:
    """
    doc string
    """
    other_player = 'p1' if this_player == 'p2' else 'p2'
    # apply the new state
    game.current_state = state
    if game.is_over(state):
        if game.is_winner(this_player):
            score = GameState.WIN
        elif game.is_winner(other_player):
            score = GameState.LOSE
        else:
            score = GameState.DRAW
        return score

    # initialize score
    if this_player == state.get_current_player_name():
        score = GameState.LOSE
    else:
        score = GameState.WIN

    for move in state.get_possible_moves():
        new_state = state.make_move(move)
        # recursive to find the score of subtree
        next_score = get_mr_score(game, new_state, this_player, depth + 1,
                                  score_list)
        if this_player == state.get_current_player_name():
            score = max(score, next_score)
        else:
            score = min(score, next_score)

        if depth == 0:
            score_list.append(next_score)
    return score


# TODO: Implement an iterative version of the minimax strategy.
def minimax_iterative_strategy(game: Game) -> Any:
    """
    doc string
    """
    stack = []
    current_state = game.current_state
    this_player = current_state.get_current_player_name()
    other_player = 'p1' if this_player == 'p2' else 'p2'

    root_node = GameTreeNode(GameState.LOSE, current_state, '', None)
    stack.append(root_node)
    count = len(stack)
    while count > 0:
        node = stack.pop()
        state = node.state
        if not game.is_over(state) and node.children is None:
            children_nodes = [GameTreeNode(GameState.LOSE, state.make_move(x),
                                           x, None) for x in
                              state.get_possible_moves()]
            node.children = children_nodes
            stack.append(node)
            for child in children_nodes:
                stack.append(child)
        elif not game.is_over(state) and node.children:
            if this_player == state.get_current_player_name():
                node.best_score = max([child.best_score for child in
                                       node.children])
            else:
                node.best_score = min([child.best_score for child in
                                       node.children])
        else:
            game.current_state = state
            if game.is_winner(this_player):
                new_score = GameState.WIN
            elif game.is_winner(other_player):
                new_score = GameState.LOSE
            else:
                new_score = GameState.DRAW
            node.best_score = new_score
        count = len(stack)
    # the node is now the root nnode
    best_move = root_node.children[0].move_taken
    highest_score = root_node.children[0].best_score
    for child in root_node.children:
        child_score = child.best_score
        if child_score >= highest_score:
            highest_score = child_score
            best_move = str(child.move_taken)
    game.current_state = current_state  # restore game state
    return game.str_to_move(str(best_move))


class GameTreeNode:
    """
    The node.

    best_score - the score of the node
    state - the state of the game
    children - next states accssible from state
    move_taken - the move leading to this state
    """
    best_score: int
    state: GameState
    children: list
    move_taken: str

    def __init__(self, best_score: int, state: GameState, move_taken: str,
                 children: Union[List["GameTreeNode"], None]) -> None:
        """
        Initialize this GameTreeNode based on score, state and children.

        """
        self.best_score = best_score
        self.state = state
        self.children = None if children is None else children[:]
        self.move_taken = move_taken


if __name__ == "__main__":
    from python_ta import check_all

    check_all(config="a2_pyta.txt")
