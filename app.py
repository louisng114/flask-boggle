from flask import Flask, request, render_template, session, jsonify
from boggle import Boggle

app = Flask(__name__)
app.secret_key = "123"

boggle_game = Boggle()
game_board = boggle_game.make_board()

@app.route("/")
def home():
    """save game board and render homepage"""
    session.clear()
    session["board"] = game_board
    return render_template("home.html")

@app.route("/", methods=["post"])
def new_game():
    """start new game"""
    boggle_game = Boggle()
    game_board = boggle_game.make_board()
    session["board"] = game_board
    return render_template("home.html")

@app.route("/check", methods=["post"])
def word_submission():
    """handles answer submission"""
    ans = request.json["ans"]
    result = boggle_game.check_valid_word(game_board,ans)
    return jsonify({"result": result})

@app.route("/result", methods=["post"])
def result_processing():
    """updates result when game ends"""
    plays = session.get("plays", 0)
    high_score = session.get("high_score", 0)
    score = request.json["score"]
    session["plays"] = plays + 1
    if score > high_score:
        session["high_score"] = score
    return ""