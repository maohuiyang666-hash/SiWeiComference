from os import name
from typing import Tuple
from flask import Flask, request, render_template, url_for, redirect


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/information', methods=['GET', 'POST'])
def information():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('information.html')


@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('about2020.html')


@app.route('/host', methods=['GET', 'POST'])
def host():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('Host2020.html')


@app.route('/procedure', methods=['GET', 'POST'])
def procedure():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('procedure2020.html')


@app.route('/about2021', methods=['GET', 'POST'])
def about2021():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('about2021.html')


@app.route('/host2021', methods=['GET', 'POST'])
def host2021():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('host2021.html')


@app.route('/procedure2021', methods=['GET', 'POST'])
def procedure2021():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('procedure2021.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0", debug=True)