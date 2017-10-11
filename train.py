from data import *

# This file is always run simultaneously when the skill is running and train is set to true in get_estimate() from api.py
# Allows for the creation of the alias dictionaries, which contain Alexa's misheard phrases for routes/stops paired with the correct name of the routes/stops
# get_estimste() from api.py handles writing the misheard phrases (keys) and this function handles writing the actual route/stop name (values)

# This function propmts the user to ask the skill some question, then get_estimate() writes appropriate dictionary keys to route_output.txt and stop_output.txt
# Then after the user hits "Enter", this file writes the appropriate dictionary values to the output files, and then prompts the user to aks a new phrase
def train():
    for route in routes:
        for stop in stops:
            input("when is the " + route + " going to arrive at " + stop + ".")
            route_file = open('route_output.txt', "a")
            stop_file = open('stop_output.txt', "a")
            route_file.write(route + "', ")
            stop_file.write(stop + "', ")
            route_file.close()
            stop_file.close()


train()
