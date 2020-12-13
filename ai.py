import chess
from datetime import datetime, time
import time

import eval

class Stopwatch(object):
    def __init__(self):
        self.start_time = None
    def start(self):
        self.start_time = datetime.now()
    @property
    def value(self):
        return (datetime.now() - self.start_time).total_seconds()
    def peek(self):
        return self.value
    def finish(self):
        return self.value

nodes = 0

def minimax_root(depth, board, is_white):
    # timer
    global nodes

    nodes = 0
    count = Stopwatch()
    count.start()
    third_best = None
    second_best = None
    leg_moves = board.legal_moves
    final_move = None
    best_value = 0

    depth -= 1 # currently working like this --> depth n = n - 1
    if is_white:
        best_value = -9999
        for i_move in leg_moves:
            move = chess.Move.from_uci(str(i_move))
            board.push(move)
            value = minimax(depth, board, -10000, 10000, not is_white)
            board.pop()
            if value > best_value:
                best_value = value
                third_best = second_best
                second_best = final_move
                final_move = move
    else:
        best_value = 9999
        for i_move in leg_moves:
            move = chess.Move.from_uci(str(i_move))
            board.push(move)
            value = minimax(depth, board, -10000, 10000, not is_white)
            board.pop()
            if value < best_value:
                best_value = value
                third_best = second_best
                second_best = final_move
                final_move = move
    time_elapsed = count.finish()
    print("nodes: ",nodes)
    print(f"1st:{final_move}\n2nd:\t{second_best}\n3rd:\t\t{third_best}")
    print(f"time spent: {time_elapsed}s")

    # to check if draw
    board.push(final_move)
    if board.can_claim_threefold_repetition() and second_best is not None:
        print("======================")
        print("     INGEN REMI")
        print("======================")
        board.pop()
        return second_best
    board.pop()
    return final_move

def minimax(depth, board, alpha, beta, is_max):
    global nodes

    if depth == 0:
        return evaluation(board)

    nodes += 1

    leg_moves = board.legal_moves
    if is_max:
        value = -9999
        for i_move in leg_moves:
            move = chess.Move.from_uci(str(i_move))
            board.push(move)
            value = max(value, minimax(depth - 1, board, alpha, beta, False))
            board.pop()
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value
    else:
        value = 9999
        for i_move in leg_moves:
            move = chess.Move.from_uci(str(i_move))
            board.push(move)
            value = min(value, minimax(depth - 1, board, alpha, beta, True))
            board.pop()
            beta = min(beta, value)
            if(beta <= alpha):
                break
        return value

def evaluation(board):
    total = 0
    for i in range(64):
        total += getPieceValue(board.piece_at(i), i)
    return total

def getPieceValue(piece, i):
    if piece == None:
        return 0
    piece = str(piece)

    is_white = piece.isupper()

    multiplier = 1 if is_white else -1

    row = 7 - i // 8
    col = i % 8
    # assert row and col are the correct size?

    value = 0
    if piece == "P" or piece == "p":
        value = 10 + eval.pawn_white[row][col] if is_white else 10 + eval.pawn_black[row][col]
    elif piece == "N" or piece == "n":
        value = 30 + eval.knight[row][col]
    elif piece == "B" or piece == "b":
        value = 30 + eval.bishop_white[row][col] if is_white else 30 + eval.bishop_black[row][col]
    elif piece == "R" or piece == "r":
        value = 50 + eval.rook_white[row][col] if is_white else 50 + eval.rook_black[row][col]
    elif piece == "Q" or piece == "q":
        value = 90 + eval.queen[row][col]
    elif piece == 'K' or piece == 'k':
        value = 900 + eval.king_white[row][col] if is_white else 900 + eval.king_black[row][col]
    # print(f"p: {piece}\t val: {value*multiplier}\t at square: {chess.SQUARE_NAMES[i]}")
    return value * multiplier