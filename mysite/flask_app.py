from flask import Flask, request, render_template, redirect
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client
from threading import Timer
import utils


app = Flask(__name__)

# Your hosted domain name
DOMAIN = "http://cedricholz.pythonanywhere.com"

@app.route("/handle-call/<string:delay>/<string:phonenumber>", methods=['GET', 'POST'])
def greeting(delay, phonenumber):
    """
    Initial greeting for when the twilio number is called or
    the number submitted on the main page is called.
    """

    resp = VoiceResponse()

    g = Gather(numDigits=3, action="/handle-key/" + delay +"/" + phonenumber + "/-1", method="POST")
    g.say("Choose a number between 1 and 1000")
    resp.append(g)

    return str(resp)

@app.route("/handle-key/<string:delay>/<string:phonenumber>/<string:replay_digit>", methods=['GET', 'POST'])
def handle_key(delay, phonenumber, replay_digit):

    """
    If replay digit is -1, we are routed from greeting function and we need to
    get the pressed digit from the user and update the history.
    """
    if replay_digit == "-1":
        digits_pressed = int(request.values.get('Digits', None))
        utils.update_history(delay, phonenumber, str(digits_pressed))
    else:
        """
        Else we are replaying fizzbuzz from a previous call, and no update
        is necessary.
        """
        digits_pressed = int(replay_digit)


    resp = VoiceResponse()

    #Fizz Buzz
    for i in range(1, digits_pressed + 1):
        div_by_3 = i % 3 == 0
        div_by_5 = i % 5 == 0

        if div_by_3 and div_by_5:
            resp.say("Fizz Buzz")
        elif div_by_3:
            resp.say("Fizz")
        elif div_by_5:
            resp.say("Buzz")
        else:
            resp.say(str(i))
    resp.say("Have a nice day.")


    return str(resp)

@app.route("/")
def index():
    """
    Gets the calltimes from the history json file and displays the webpage with
    the histories in list form.
    """
    callTimes = utils.file_to_json("mysite/call_history.json")['history']
    return render_template("index.html", callTimes=callTimes)

def make_outgoing_call(phonenumber, redirect_url):
    account_sid = "AC9aedcd8f41bddabf0777fc646460f98c"
    auth_token = "9a63aeb9a5353dc9284dd32b583744fe"
    client = Client(account_sid, auth_token)

    call = client.api.account.calls\
          .create(to="+" + phonenumber,
                  from_="+15598887039",
                  url= redirect_url)
    print(call.sid)



@app.route('/', methods=['POST'])
def submit_phonenumber_delay():
    phonenumber = request.form['phonenumber']

    # Take only digits from phonenumber string, and add 1 if necessary
    phonenumber = utils.format_phonenumber(phonenumber)
    if phonenumber == "Invalid Number":
        return phonenumber

    # Take only digits from delay string
    delay = request.form['delay']
    delay = utils.format_delay(delay)
    if delay == "Invalid Digit":
        return delay

    url = DOMAIN + "/handle-call/"+ delay +"/" + phonenumber


    """
    Calls number after the chosen number of minutes has passed.
    """
    timer = Timer(int(delay)*60, lambda : make_outgoing_call(phonenumber, url))
    timer.start()

    return redirect("/")


@app.route('/replay/<string:digits>/<string:phonenumber>', methods=['GET', 'POST'])
def replay(digits, phonenumber):

    # Take only digits from phonenumber string, and add 1 if necessary
    phonenumber = utils.format_phonenumber(phonenumber)

    if phonenumber == "Invalid Number":
        return phonenumber

    "Create url to call a number and route it handle-key function to replay fizzbuzz"
    url = DOMAIN + "/handle-key/-1/" + phonenumber +"/" + digits

    make_outgoing_call(phonenumber, url)

    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)