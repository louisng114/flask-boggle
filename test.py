from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle
import json

class FlaskTests(TestCase):
    def test_home(self):
        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1>BOGGLE TIME!</h1>", html)
    def test_new_game(self):
        with app.test_client() as client:
            res = client.post("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1>BOGGLE TIME!</h1>", html)
    def test_word_submission(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["board"] = [["A", "P", "P", "L", "E"],
                                           ["A", "P", "P", "L", "E"],
                                           ["A", "P", "P", "L", "E"],
                                           ["A", "P", "P", "L", "E"],
                                           ["A", "P", "P", "L", "E"]]
            res = client.get("/check?ans=apple")

            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json["result"], "ok")
    def test_word_submission_repeat(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["board"] = [["A", "P", "P", "L", "E"],
                                           ["A", "P", "P", "L", "E"],
                                           ["A", "P", "P", "L", "E"],
                                           ["A", "P", "P", "L", "E"],
                                           ["A", "P", "P", "L", "E"]]
            res = client.get("/check?ans=apple")
            res = client.get("/check?ans=apple")

            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json["result"], "already found")
    def test_word_submission_not_on_board(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["board"] = [["A", "P", "P", "L", "E"],
                                           ["A", "P", "P", "L", "E"],
                                           ["A", "P", "P", "L", "E"],
                                           ["A", "P", "P", "L", "E"],
                                           ["A", "P", "P", "L", "E"]]
            res = client.get("/check?ans=orange")

            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json["result"], "not-on-board")
    def test_word_submission_fake(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["board"] = [["A", "P", "P", "L", "E"],
                                           ["A", "P", "P", "L", "E"],
                                           ["A", "P", "P", "L", "E"],
                                           ["A", "P", "P", "L", "E"],
                                           ["A", "P", "P", "L", "E"]]
            res = client.get("/check?ans=aaple")

            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json["result"], "not-word")
    def test_result_processing(self):
        with app.test_client() as client:
            res = client.post("/result", data=json.dumps({"score": 500}), content_type="application/json")

            self.assertEqual(res.status_code, 200)
            self.assertEqual(session["high_score"], 500)
            self.assertEqual(session["plays"], 1)
