from flask import Flask, render_template, request, send_file
import os
from pathlib import Path
import numpy as np
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
    if width <= 0 or height <= 0:
        return render_template("form.html", finished="Error", error_msg="ERROR: width and height must be greater than zero.")
    billiards_table = Table(geometry, width, height)
    billiards_table.reflections = 100
    billiards_ball = Ball(billiards_table, x, y, angle)
    if geometry == "rectangle":
        if abs(x) <= width/2 and abs(y) <= height/2:
            billiards_table.rectangle_calc(billiards_ball)
        else:
            return render_template("form.html", finished="Error", error_msg="ERROR: starting position not on the table.")
    elif geometry == "elliptical":
        if (x/width)**2 + (y/height)**2 <= 1:
            billiards_table.elliptical_calc(billiards_ball)
        else:
            return render_template("form.html", finished="Error", error_msg="ERROR: starting position not on the table.")
    else:
        if abs(x) <= width/2 and abs(y) <= height/2 and not ((x > width/2 and x-width/2 > np.sqrt((height/2)**2-y**2)) or (x < width/2 and x+width/2 < -np.sqrt((height/2)**2-y**2))):
                billiards_table.stadium_calc(billiards_ball)
        else:
            return render_template("form.html", finished="Error", error_msg="ERROR: starting position not on the table.")
    # Get location to save GIF
    current_folder = Path(__file__).parent.resolve()
    save_loc = current_folder / "static/scatter.gif"
    billiards_table.plot(billiards_ball, save=save_loc)
    return render_template("form.html", finished="True")