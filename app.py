from flask import Flask, render_template, request, jsonify
import chess
import chess.svg
from engine import MiniMax
from engine import newMiniMax
import math
import time
import json


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/svg_game')
def new_game():
    file = open('./Games/current_game.txt', 'w')

    fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

    file.write(fen)
    file.close()

    board = chess.Board(fen)

    return render_template('svg_game.html', svg=str(chess.svg.board(board, size=500)))


@app.route('/submit', methods=['POST'])
def submit():
    file = open('./Games/current_game.txt', 'r')

    current_fen = ''

    for line in file:
        current_fen = line

    file.close()

    board = chess.Board(current_fen)

    move = request.form['move']

    invalid_move = False

    eval_string = ''
    evaluation = None
    last_move = None

    try:
        file = open('./Games/current_game.txt', 'a')

        board.push_san(move)

        new_fen = board.fen()

        file.write('\n' + new_fen)

        evaluation, move = MiniMax.minmax(board, 4, -math.inf, math.inf)
        evaluation = evaluation/100

        if move is not None:
            board.push(move)
            last_move = move

        final_fen = board.fen()

        file.write('\n' + final_fen)

        file.close()

    except ValueError:
        invalid_move = True

    if evaluation is not None:
        eval_string = eval_to_string(evaluation)

    game_over = board.is_game_over()

    return render_template('svg_game.html',
                           svg=str(chess.svg.board(board, size=500, lastmove=last_move)),
                           invalid_move=invalid_move,
                           game_over=game_over,
                           eval=eval_string)


def eval_to_string(evaluation):
        if evaluation > 0:
            eval_string = '+ ' + str(evaluation)
        elif evaluation < 0:
            eval_string = '- ' + str(abs(evaluation))
        else:
            eval_string = str(evaluation)


@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('test.html')


@app.route('/make_move', methods=['GET', 'POST'])
def make_move():
    fen = request.get_data().decode(encoding="utf-8", errors="strict").replace('%2F', '/').replace('+', ' ')[6:]

    board = chess.Board(fen)
    
    start = time.time()
    evaluation, move = MiniMax.minmax(board, 4, -math.inf, math.inf)
    evaluation = evaluation/100
    print('time to calculate:', time.time() - start, 'seconds')
    """
    start = time.time()
    move = newMiniMax.get_move(board)
    print('time to calculate:', time.time() - start, 'seconds')
    """

    return move.uci()


@app.route('/js_game', methods=['GET'])
def game():
    return render_template('js_game.html')


if __name__ == '__main__':
    app.run()
