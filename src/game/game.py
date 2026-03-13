import copy
import random

SIZE = 4
GOAL_TILE = 2048
ACTION_LEFT = "left"
ACTION_RIGHT = "right"
ACTION_UP = "up"
ACTION_DOWN = "down"
ACTIONS = [ACTION_LEFT, ACTION_RIGHT, ACTION_UP, ACTION_DOWN]


def _transpose(board):
    return [list(row) for row in zip(*board)]


def _slide_row_left_with_score(row):
    tiles = [value for value in row if value != 0]
    merged = []
    score_gain = 0
    idx = 0

    while idx < len(tiles):
        if idx + 1 < len(tiles) and tiles[idx] == tiles[idx + 1]:
            new_value = tiles[idx] * 2
            merged.append(new_value)
            score_gain += new_value
            idx += 2
        else:
            merged.append(tiles[idx])
            idx += 1

    merged += [0] * (len(row) - len(merged))
    return merged, score_gain


def _move_left(board):
    new_board = []
    score_gain = 0
    for row in board:
        moved_row, gained = _slide_row_left_with_score(row)
        new_board.append(moved_row)
        score_gain += gained
    return new_board, score_gain


def _move_right(board):
    reversed_board = [list(reversed(row)) for row in board]
    moved, score_gain = _move_left(reversed_board)
    return [list(reversed(row)) for row in moved], score_gain


def _move_up(board):
    transposed = _transpose(board)
    moved, score_gain = _move_left(transposed)
    return _transpose(moved), score_gain


def _move_down(board):
    transposed = _transpose(board)
    moved, score_gain = _move_right(transposed)
    return _transpose(moved), score_gain


def _simulate_action(board, action):
    if action == ACTION_LEFT:
        return _move_left(board)
    if action == ACTION_RIGHT:
        return _move_right(board)
    if action == ACTION_UP:
        return _move_up(board)
    if action == ACTION_DOWN:
        return _move_down(board)
    raise ValueError(f"Unknown action: {action}")


class Game2048:
    def __init__(self, size=SIZE):
        self.size = size
        self.board = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.has_won = False
        self.reset()

    def reset(self):
        self.board = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.has_won = False
        self._add_new_tile()
        self._add_new_tile()

    def _get_empty_cells(self):
        return [
            (r, c)
            for r in range(self.size)
            for c in range(self.size)
            if self.board[r][c] == 0
        ]

    def _add_new_tile(self):
        empty_cells = self._get_empty_cells()
        if not empty_cells:
            return False
        row, col = random.choice(empty_cells)
        self.board[row][col] = 2 if random.random() < 0.9 else 4
        return True

    def get_state(self):
        return copy.deepcopy(self.board)

    def get_legal_actions(self):
        legal_actions = []
        for action in ACTIONS:
            next_board, _ = _simulate_action(self.board, action)
            if next_board != self.board:
                legal_actions.append(action)
        return legal_actions

    def apply_action(self, action):
        if action not in ACTIONS:
            raise ValueError(f"Unknown action: {action}")

        next_board, score_gain = _simulate_action(self.board, action)
        changed = next_board != self.board

        if not changed:
            return False

        self.board = next_board
        self.score += score_gain
        self.has_won = self.has_won or self.get_highest_tile() >= GOAL_TILE
        self._add_new_tile()
        return True

    def clone(self):
        cloned = Game2048(size=self.size)
        cloned.board = copy.deepcopy(self.board)
        cloned.score = self.score
        cloned.has_won = self.has_won
        return cloned

    def is_terminal(self):
        return len(self.get_legal_actions()) == 0

    def get_score(self):
        return self.score

    def get_highest_tile(self):
        return max(max(row) for row in self.board)
