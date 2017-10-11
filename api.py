import requests
import datetime
import difflib
from data import *

# base URL of TransLoc's OpenAPI
url = "https://transloc-api-1-2.p.mashape.com/"



# Gets arrival estimate for a given route and stop at UVA

# train is set to true when running train.py; this causes whatever route/stop phrase that Alexa hears to be written to route_output.txt and stop_output.txt as dictionary keys so that they can later be added to the alias dictionaries in data.py
# The alias dictionaries in data.py improve the skill's accuracy at choosing the correct route/stop that the user said
def get_estimate(routeName, stopName, direction="forward", train=False):
    # by default there are no errors and we are not training
    data = {"error": None, "train": None}

    try:
        try:
            # Use difflib to create a list of routes that most closely match the keys in route_alias from data.py (if they match by at least the cutoff amount)
            # Get the first value (closest match) from this list and get the value (actual route name)
            # Set bestRoute equal to the id of the route that corresponds to that route name
            bestRoute = routeToId[route_alias[(difflib.get_close_matches(routeName, route_alias, cutoff=0.5))[0]]]

            # Perform the same steps as above, using stops this time
            bestStop = stopToId[stop_alias[(difflib.get_close_matches(stopName, stop_alias, cutoff=0.5))[0]]]

            # If training, write whatever route/stop Alexa thinks she heard as a dictionary key to route_output.txt and stop_output.txt, then return
            if (train):
                route_file = open('route_output.txt', "a")
                stop_file = open('stop_output.txt', "a")
                print(routeName)
                route_file.write("'" + routeName + "' : '")
                print(stopName)
                stop_file.write("'" + stopName + "' : '")
                route_file.close()
                stop_file.close()
                data["train"] = str(idToRoute[bestRoute] + " ; " + idToStop[bestStop])
                return data

        # If something goes wrong, return an error message and prompt the user to ask again
        except:
            data["error"] = "Hmm, I didn't quite get that. "
            return data

        # This section sends a GET request to the TransLoc Open API to get the arrival estimates
        # UVA agency ID = 347

        # Construct the appropriate url using the id of the stop and route found above
        arrivalEstimates_url = url + "arrival-estimates.json?agencies=347&callback=call&stops=" + bestStop + "&routes=" + bestRoute
        # Send the request, convert the response into json
        arrivalEstimatesResponse = requests.get(arrivalEstimates_url, headers={
            "X-Mashape-Key": "7zef4m39KxmshI8Z2wZHynIctO7ap1YpFbmjsnL1PAIUpeybSu"}).json()

        # Construct a list of upcoming arrival times for the requested route at the requested stop and return it
        arrivalEstimates = []
        for result in arrivalEstimatesResponse["data"]:
            for arrival in result["arrivals"]:
                formatted_arrival = arrival["arrival_at"].replace("-04:00", "").replace("T", " ")
                wait_time = datetime.datetime.strptime(formatted_arrival, "%Y-%m-%d %H:%M:%S") - datetime.datetime.now()
                arrivalEstimates.append(str(wait_time.seconds // 60 - 60))
        data.update({"arrivalEstimates": arrivalEstimates, "route": idToRoute[bestRoute],
                     "stop": idToStop[bestStop].replace(" Dr ", " drive ").replace("NW", "northwest").replace(" St ",
                                                                                                              " street ")
                     })

        return data

    # Returns an error message if something goes wrong and prompts the user to ask again
    except:
        data["error"] = "Hmm, I didn't quite get that. "
        return data
