from flask import Flask, render_template, request, send_file
import os
from pathlib import Path
from mathematical_billiards.table import Table
from mathematical_billiards.ball import Ball

app = Flask(__name__)

gif_path = os.path.join('static', 'scatter.gif')

@app.route('/')
def test():
    return render_template("form.html", finished="False")

@app.route('/')
def loading():
    return render_template("loading.html")

@app.route('/', methods=['POST'])
def my_form_post():
    geometry = request.form['geometry']
    width = float(request.form['width'])
    height = float(request.form['height'])
    x = float(request.form['start_x'])
    y = float(request.form['start_y'])
    angle = float(request.form['angle'])
    billiards_table = Table(geometry, width, height)
    billiards_table.reflections = 100
    billiards_ball = Ball(billiards_table, x, y, angle)
    if geometry == "rectangle":
        billiards_table.rectangle_calc(billiards_ball)
    elif geometry == "elliptical":
        billiards_table.elliptical_calc(billiards_ball)
    else:
        billiards_table.stadium_calc(billiards_ball)
    # Get location to save GIF
    current_folder = Path(__file__).parent.resolve()
    save_loc = current_folder / "static/scatter.gif"
    billiards_table.plot(billiards_ball, save=save_loc)
    return render_template("form.html", finished="True")