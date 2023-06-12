from flask import Flask, render_template, redirect, session, request
import os
from supabase import create_client, Client
from database import get_db

def create_tables():
  with get_db() as db:
    db.execute(open("schema.sql").read())

supabase_url = os.getenv("supabase_url")
supabase_key = os.getenv("supabase_key")
supabase = create_client(supabase_url, supabase_key)

    
app = Flask(__name__, static_url_path='/static')
create_tables()



@app.route('/')
def index():
  username = request.headers['X-Replit-User-Name']
  return render_template('index.html', username = username)

@app.route('/trip/<trip_id>')
def trip_details(trip_id):
  # Fetch the trip information from the database based on the trip ID
  db = get_db()
  trip_data = db.execute(
    'SELECT * FROM trips WHERE id = ?', (trip_id,)
  ).fetchone()
  db.close()

  # Render the trip details template with the trip information
  return render_template('trip_details.html', trip_data=trip_data)

app.run(host='0.0.0.0', port=81)

