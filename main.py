from flask import Flask, render_template, redirect, session, request
from replit import db

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
  username = request.headers['X-Replit-User-Name']
  return render_template('index.html', username = username)

@app.route('/trip/<trip_id>')
def trip_details(trip_id):
  # Fetch the trip information from the database based on the trip ID
  trip_data = db[trip_id]

  # Render the trip details template with the trip information
  return render_template('trip_details.html', trip_data=trip_data)

app.run(host='0.0.0.0', port=81)

