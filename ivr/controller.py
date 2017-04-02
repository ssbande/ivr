from flask import render_template, redirect, url_for, request, session, flash, Response
from ivr import app
import twilio.twiml

def twiml(resp):
    resp = Response(str(resp))
    resp.headers['Content-Type'] = 'text/xml'
    return resp

@app.route('/')
@app.route('/ivr')
def home():
  print ("Running something")
  return render_template('index.html')


@app.route('/ivr/welcome', methods=['POST'])
def welcome():
  response = twilio.twiml.Response()
  with response.gather(numDigits=1, action=url_for('menu'), method="POST") as g:
    g.play(url="http://howtodocs.s3.amazonaws.com/et-phone.mp3", loop=3)

  return twiml(response)


@app.route('/ivr/menu', methods=['POST'])
def menu():
  selected_option = request.form['Digits']
  option_actions = {'1': _give_instructions,'2': _list_planets}

  if option_actions.has_key(selected_option):
    response = twilio.twiml.Response()
    option_actions[selected_option](response)
    return twiml(response)

  return _redirect_welcome()


@app.route('/ivr/planets', methods=['POST'])
def planets():
  selected_option = request.form['Digits']
  option_actions = {'2': "+819018874371"}

  if option_actions.has_key(selected_option):
    response = twilio.twiml.Response()
    response.dial(option_actions[selected_option])
    return twiml(response)

  return _redirect_welcome()


# private methods

def _give_instructions(response):
  response.say("uncle pehle 1 kilometer tak seedha jana " +
    "uske baad doosre left me le lena" +
    "fir aage jaa ke hanuman mandir milega wahan se right " +
    "le ke ek paan ki ghunti milegi uske baju wala planet hai tumhara",
    voice="alice", language="hi-IN")

  response.say("Thank you for calling the ET Phone Home Service - the " +
    "adventurous alien's first choice in intergalactic travel")

  response.hangup()
  return response


def _list_planets(response):
  with response.gather(numDigits=1, action=url_for('planets'), method="POST") as g:
    g.say("To call the planet Broh doe As O G, press 2. To call the planet " +
      "DuhGo bah, press 3. To call an oober asteroid to your location, press 4. To " +
      "go back to the main menu, press the star key ",
      voice="alice", language="en-GB", loop=3)

  return response


def _redirect_welcome():
  response = twilio.twiml.Response()
  response.say("Returning to the main menu", voice="alice", language="en-GB")
  response.redirect(url_for('welcome'))

  return twiml(response)