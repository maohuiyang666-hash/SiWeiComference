import re
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

from app import app

import os

app.config['SECRET_KEY'] = os.urandom(24)

if __name__ == '__main__':
    app.run(debug=True)