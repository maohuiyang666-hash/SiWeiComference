import re
from flask import Flask, render_template, request
from app import app

if __name__ == '__main__':
    app.jinja_env.line_statement_prefix = '#'
    app.config['SECRET_KEY'] = 'abcd+-*/1234'
    app.run('127.0.0.1', port=5000, debug=True)