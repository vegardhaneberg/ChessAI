import chess
import math
import engine.PieceValueBoards as PieceValueBoards


def evaluation_function(board):

    if board.is_game_over():
        result = board.result()
        if result == '1-0':
            return math.inf
        elif result == '0-1':
            return -math.inf
        else:
            return 0

    white_pawns = list(board.pieces(chess.PAWN, chess.WHITE))
    black_pawns = list(board.pieces(chess.PAWN, chess.BLACK))

    white_knights = list(board.pieces(chess.KNIGHT, chess.WHITE))
    black_knights = list(board.pieces(chess.KNIGHT, chess.BLACK))

    white_bishops = list(board.pieces(chess.BISHOP, chess.WHITE))
    black_bishops = list(board.pieces(chess.BISHOP, chess.BLACK))

    white_rooks = list(board.pieces(chess.ROOK, chess.WHITE))
    black_rooks = list(board.pieces(chess.ROOK, chess.BLACK))

    white_queens = list(board.pieces(chess.QUEEN, chess.WHITE))
    black_queens = list(board.pieces(chess.QUEEN, chess.BLACK))

    white_king = list(board.pieces(chess.KING, chess.WHITE))
    black_king = list(board.pieces(chess.KING, chess.BLACK))

    white_pawns_score = len(white_pawns)*100 + sum([PieceValueBoards.black_pawn[::-1][i] for i in white_pawns])
    black_pawns_score = len(black_pawns) * 100 + sum([PieceValueBoards.black_pawn[i] for i in black_pawns])

    white_knights_score = len(white_knights)*320 + sum([PieceValueBoards.black_knight[::-1][i] for i in white_knights])
    black_knights_score = len(black_knights)*320 + sum([PieceValueBoards.black_knight[i] for i in black_knights])

    white_bishops_score = len(white_bishops)*330 + sum([PieceValueBoards.black_bishop[::-1][i] for i in white_bishops])
    black_bishops_score = len(black_bishops)*330 + sum([PieceValueBoards.black_bishop[i] for i in black_bishops])

    white_rooks_score = len(white_rooks)*500 + sum([PieceValueBoards.black_rook[::-1][i] for i in white_rooks])
    black_rooks_score = len(black_rooks)*500 + sum([PieceValueBoards.black_rook[i] for i in black_rooks])

    white_queen_score = len(white_queens)*900 + sum([PieceValueBoards.black_queen[::-1][i] for i in white_queens])
    black_queen_score = len(black_queens)*900 + sum([PieceValueBoards.black_queen[i] for i in black_queens])

    if white_queen_score == black_queen_score == 0 or \
            sum([len(white_knights), len(black_knights), len(white_bishops), len(black_bishops),
                 len(white_rooks), len(black_rooks)]) == 0:
        white_king_score = PieceValueBoards.black_king_endgame[::-1][white_king[0]]
        black_king_score = PieceValueBoards.black_king_endgame[black_king[0]]
    else:
        white_king_score = PieceValueBoards.black_king_middelgame[::-1][white_king[0]]
        black_king_score = PieceValueBoards.black_king_middelgame[black_king[0]]

    white_total_score = white_pawns_score + white_knights_score + white_bishops_score + white_rooks_score + white_queen_score + white_king_score
    black_total_score = black_pawns_score + black_knights_score + black_bishops_score + black_rooks_score + black_queen_score + black_king_score

    return white_total_score - black_total_score


def minmax(board, depth, alpha, betha):

    if depth == 0 or board.is_game_over():
        return evaluation_function(board), None

    legal_moves = board.legal_moves

    if board.turn:
        best_move = None
        best_eval = -math.inf

        for current_move in legal_moves:
            board_copy = board.copy()
            board_copy.push(current_move)
            current_eval, move = minmax(board_copy, depth - 1, alpha, betha)

            if current_eval > best_eval:
                best_move = current_move
                best_eval = current_eval
            alpha = max(alpha, current_eval)
            if alpha >= betha:
                break
        return best_eval, best_move

    else:
        best_move = None
        best_eval = math.inf

        for current_move in legal_moves:
            board_copy = board.copy()
            board_copy.push(current_move)
            current_eval, move = minmax(board_copy, depth - 1, alpha, betha)

            if current_eval < best_eval:
                best_eval = current_eval
                best_move = current_move

            betha = min(betha, current_eval)
            if alpha >= betha:
                break
        return best_eval, best_move



