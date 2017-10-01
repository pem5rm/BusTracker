import logging

from random import randint

from flask import Flask, render_template

from jinja2 import Template

from flask_ask import Ask, statement, question, session

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

from api import *

@ask.launch

def launch():

    return question("Welcome to the UVA Bus Schedule! What would you like to know?")


@ask.intent("GetArrivalTimes", mapping={"route" : "route", "stop" : "stop"})

def get_arrival_times(route, stop):
    try:
        data = get_estimate(route, stop)
        if data["error"] != None:
            return question(data["error"] + " Could you please repeat the question?")
        elif len(data["arrivalEstimates"]) == 0:
            return statement("Sorry, it doesn't look like " + data["route"] + " will be stopping at " + data["stop"] + " anytime soon.")
        elif len(data["arrivalEstimates"]) > 1:
            return statement("The next " + data["route"] + " will arrive at " +  data["stop"] + " in " + str(data["arrivalEstimates"][0]) + " minutes. There's also a bus arriving in " + str(data["arrivalEstimates"][1]) + " minutes.")
        elif len(data["arrivalEstimates"]) == 1:
            return statement("The next " + data["route"] + " will arrive at " +  data["stop"] + " in " + str(data["arrivalEstimates"][0]) + " minutes.")
    except:
        question("Sorry, I didn't understand that.")


@ask.intent("ListRoutes")

def list_routes():
    return statement("The bus routes at UVA are " + " , ".join(routes[0:-1]) + ", and " + routes[-1])

@ask.intent("ListStops")

def list_stops():
    return statement("The bus stops at UVA are " + " , ".join(stops[0:-1]) + ", and " + stops[-1])

# @ask.intent("YesIntent")
#
# def next_round():
#     data = get_estimate("Northline", "Runk")
#     # return statement("The next " + data["route"] + " will arrive at " +  data["stop"] + " in " + str(data["arrivalEstimates"][0]) + " minutes. There's also another bus arriving in " + str(data["arrivalEstimates"][1]) + " minutes.")
#     return statement("Yes")
#
#
# @ask.intent("NoIntent")
#
# def no_answer():
#     return statement("ok, bye!")




# @ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})
#
# def answer(first, second, third):
#
#     winning_numbers = session.attributes['numbers']
#     try:
#         if [first, second, third] == winning_numbers:
#
#             # msg = render_template('win')
#             return statement("Good job!")
#
#         else:
#
#             # msg = render_template('lose')
#             # msg = Template("Sorry, that's the wrong answer.")
#             return statement("You lose!")
#
#         # return statement(msg.render())
#     except:
#         return statement("You lose!")

# @ask.session_ended
# def session_ended():
#     logging.debug("Session Ended")
#     return "", 200

if __name__ == '__main__':

    app.run(debug=True)
