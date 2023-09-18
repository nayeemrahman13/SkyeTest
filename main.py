from flask import Flask, render_template, redirect, session, request
import os
from supabase import create_client, Client
from database import get_db
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

supabase_url = os.getenv("supabase_url")
supabase_key = os.getenv("supabase_key")
supabase = create_client(supabase_url, supabase_key)

twilio_sid = os.getenv("twilio_sid")
twilio_auth_token = os.getenv("twilio_auth_token")
twilio_client = Client(twilio_sid, twilio_auth_token)

twilio_phone_number = os.getenv("twilio_phone_number")
my_phone = os.getenv("my_phone")

app = Flask(__name__, static_url_path='/static')

def send_message():
  message = twilio_client.messages.create(
    body='Hello, this is a test message from my Flask app!',
    from_=twilio_phone_number,
    to=my_phone
)
  return message

def process_sms(message_body, from_number):
    # Store the message in Supabase database
    supabase.table("messages").insert(
        [{"message": message_body, "from_number": from_number}]
    ).execute()
    # Return a response message
    response = "Your message has been stored in the database."
    return response

@app.route("/sms", methods=['POST'])
def receive_sms():
    # Fetch the message body and phone number from the request
    message_body = request.form['Body']
    from_number = request.form['From']

    # Process the message and generate a response
    response = process_sms(message_body, from_number)

    # Create a TwiML response
    twiml_response = MessagingResponse()
    twiml_response.message(response)

    return str(twiml_response)

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

@app.route('/plan')
def plan():
  
  return render_template('plan.html')
  
@app.route('/create_trip', methods =[ 'POST', 'GET'])
def create_trip():
  if request.method == 'POST':
    # Fetch the form data from the request
    destination = request.form["destination"]
    start_date = request.form["start_date"]
    end_date = request.form["end_date"]
  return render_template('plan.html')

@app.route('/trips')
def trips():
    # Get trips from the database and pass to the template
    #trips = get_all_trips()
    return render_template('trips.html')#, trips=trips)

@app.route('/invite', methods=['GET', 'POST'])
def invite():
    if request.method == 'POST':
        # Get the form data submitted by the user
        friend_name = request.form['friend_name']
        friend_phone = request.form['friend_phone']
        
        # Perform any necessary validation on the form data
        
        # Send the invitation text message
        message_body = f"Hi {friend_name}, you've been invited to join this trip. How many days would you like to stay?"
        message = twilio_client.messages.create(
            body=message_body,
            from_=twilio_phone_number,
            to=friend_phone
        )
        
        # Redirect the user to a confirmation page
        return render_template('invitation_sent.html', friend_name=friend_name)
    
    # Render the invite.html template for GET requests
    return render_template('invite.html')

app.run(host='0.0.0.0', port=81)

