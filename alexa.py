import logging

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

from api import *

# Message that is displayed when the skil is launched
@ask.launch

def launch():

    return question("Welcome to the UVA Bus Schedule! What would you like to know?").reprompt("Which bus route and stop do you want arrival estimates for? Or, just say 'help' to get more information about this skill.")

# Allows the user to ask get estimated arrival times for a particular bus route and stop
@ask.intent("GetArrivalTimes", mapping={"route" : "route", "stop" : "stop"})

def get_arrival_times(route, stop):

    data = get_estimate(route, stop)
    if data["error"] != None:
        return question(data["error"] + " Could you please repeat the question?")
    elif len(data["arrivalEstimates"]) == 0:
        return statement("Sorry, it doesn't look like " + data["route"] + " will be stopping at " + data["stop"] + " anytime soon.")
    elif len(data["arrivalEstimates"]) > 1:
        return statement("The next " + data["route"] + " will arrive at " +  data["stop"] + " in " + str(data["arrivalEstimates"][0]) + " minutes. There's also a bus arriving in " + str(data["arrivalEstimates"][1]) + " minutes.")
    elif len(data["arrivalEstimates"]) == 1:
        return statement("The next " + data["route"] + " will arrive at " +  data["stop"] + " in " + str(data["arrivalEstimates"][0]) + " minutes.")


# Provides info about the skill
@ask.intent("Help")

def get_help():
    return statement("This skill uses TransLoc's Open API  to provide arrival estimates for any bus route and any stop at UVA. The names of bus routes and stops are the same as they are on the 'Rider' app. For example you could ask: 'When will the next Northline be at McCormick Rd @ Alderman Library'.")


if __name__ == '__main__':

    app.run(debug=True)
