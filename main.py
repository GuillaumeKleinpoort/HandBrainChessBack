import chess
from flask import Flask
from flask import request
from threading import Thread
from stockfish import Stockfish
from flask_cors import CORS, cross_origin
import random

stockfish = Stockfish("stockfish_14/stockfish_14.1_linux_x64")

app = Flask('')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def get_move_from_brain(fen, brain):
  if brain == "chaos":
    brain = random.choice(["stockfish", "random"])
  
  board = chess.Board(fen)
  
  if brain == "stockfish":
    stockfish.set_fen_position(fen)
    square = str(stockfish.get_best_move_time(1000))[0:2]
    return chess.piece_name(board.piece_type_at(chess.parse_square(square)))
  if brain == "random":
    piece_types = []
    for move in board.legal_moves:
      piece_type = chess.piece_name(board.piece_type_at(move.from_square))
      if piece_type not in piece_types:
        piece_types.append(piece_type)
    
    return random.choice(piece_types)
  

@app.route('/')
def home():
  return str("aaaaye me gusta chess")

@app.route('/move', methods=["POST"])
@cross_origin()
def get_move():
  fen = request.form["fen"]
  brain = request.form["brain"]
  
  return get_move_from_brain(fen, brain)

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()