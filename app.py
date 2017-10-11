import logging

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

from api import *

# Message that Alexa says when the skill is launched
@ask.launch
def launch():
    return question("Welcome to UVA Bus Tracker! Which bus route and stop do you want arrival estimates for?").reprompt(
        "For example you could ask: 'When will the Northline arrive at University Avenue at Snyder Tennis Courts'. Which bus route and stop would you like arrival estimates for?")

# Exits the skill if the user says "stop", "cancel", or "never mind" at any time
@ask.intent("AMAZON.StopIntent")
def exit():
    return statement("")

# Allows the user to ask get estimated arrival times for a particular bus route and stop at UVA
@ask.intent("GetArrivalTimes", mapping={"route": "route", "stop": "stop"})
def get_arrival_times(route, stop):
    data = get_estimate(route, stop)

    # If training, have Alexa read out the route and stop that she thinks the user said for debugging purposes
    if data["train"] != None:
        return question(data["train"])
    # If there was an error, prompt the user to repeat the question
    if data["error"] != None:
        return question(data[
                            "error"] + " Please make sure to use the full name of the bus route and stop. Could you please repeat the question?")
    # If the list of upcoming arrival times is empty, then inform the user that none of the busses from that route are arriving at that stop soon
    elif len(data["arrivalEstimates"]) == 0:
        return statement(
            "Sorry, it doesn't look like " + data["route"] + " will be stopping at " + data["stop"] + " anytime soon.")

    # Tell the user when the next bus will arrive, then list the other upcoming arrival times
    else:

        current = "The next " + data["route"] + " will arrive at " + data["stop"] + " in " + data["arrivalEstimates"][
            0] + " minutes."
        if data["arrivalEstimates"][0] == "1":
            current = "The next " + data["route"] + " will arrive at " + data["stop"] + " in 1 minute."
        elif data["arrivalEstimates"][0] == "0":
            current = "There's a " + data["route"] + " boading at " + data["stop"] + " now."

        if len(data["arrivalEstimates"]) > 2:
            return statement(current + " There are also " + data["route"] + " busses arriving in " + " minutes, ".join(
                    data["arrivalEstimates"][1:-1]) + " minutes, and " + (data["arrivalEstimates"][-1] + " minutes."))

        elif len(data["arrivalEstimates"]) == 2:
            return statement(
                current + " There's also a " + data["route"] + " bus arriving in " + data["arrivalEstimates"][
                    1] + " minutes.")
        elif len(data["arrivalEstimates"]) == 1:
            return statement(current)


# Provides more info about the skill
@ask.intent("AMAZON.HelpIntent")
def get_help():
    return question(
        "You can ask UVA Bus Tracker to get arrival estimates for buses at the University of Virginia. Please make sure to use the full name of the bus route and stop. For example you could ask: 'When will the Northline arrive at University Avenue at Snyder Tennis Courts'. Which bus route and stop do you want arrival estimates for?")


if __name__ == '__main__':
    app.run(debug=True)
