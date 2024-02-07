from flask import Flask, jsonify, request

from marks import get_marks

app = Flask(__name__)


@app.get("/")
def home():
    return "Home"


@app.post("/result")
def get_result():
    request.form.get("link")
    return "Got Link"
