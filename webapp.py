from flask import Flask, jsonify, render_template, request

from marks import get_marks

app = Flask(__name__)


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/result")
def get_result():
    link = request.form.get("link")
    try:
        return str(get_marks(link))
    except Exception:
        return "Exception"
