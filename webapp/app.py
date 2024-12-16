from flask import Flask, render_template, request
from src.main import main

app = Flask(__name__)

@app.route('/')
def test():
    return render_template("form.html")

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['geometry']
    processed_text = text.upper()
    return processed_text
