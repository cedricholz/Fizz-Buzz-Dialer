# Fizz-Buzz-Dialer - Hosted at http://cedricholz.pythonanywhere.com/

A Twilio Flask application that will call an input phone number, and ask for a number between 1 and 1000. It will then count up to the input number from one, but will say "Fizz" instead of numbers divisible by 3, "Buzz," instead of numbers divisible by 5, and "Fizzbuzz," for numbers divisible by both 3 and 5. It also asks for a delay, and will only make the call after the input number of minutes have passed.

It also keeps a log of the calls made and when the replay button is pressed, the number in its history will be called, and the Fizzbuzz for the number previously entered will be repeated.


# To run locally on Windows

Create an account on twilio and get a phone number. Put the number in the variable my_twilio_number in flask.py

Change my_twilio_number in flask_app to your number twilio number.

From your twilio Dashboard get your ACCOUNT SID and AUTH_TOKEN, and create a file with them called api_keys.json in the main folder.

Make sure it looks similar to this.
{
  "account_sid": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "auth_token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}

Install Python and Gitbash. In the terminal install flask with the command, pip3 install flask.

Then move to the directory of the Fizz-Buzz-Dialer

Run the app with the command, python flask_app.py

Go to http://127.0.0.1:5000/ to view the application.

