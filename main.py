from flask import Flask, render_template, redirect, session, request
from replit import db

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
  username = request.headers['X-Replit-User-Name']
  return render_template('index.html', username = username)

app.run(host='0.0.0.0', port=81)

