
from api import routes, stops
def train():
    # route_file = open('route_output.txt', "a")
    # stop_file = open('stop_output.txt', "a")
    for route in routes:
        # route_file.write("\n")
        # stop_file.write("\n")
        for stop in stops:
            input("when is the " + route + " going to arrive at " + stop +".")
            route_file = open('route_output.txt', "a")
            stop_file = open('stop_output.txt', "a")
            route_file.write(route + "', ")
            stop_file.write(stop + "', ")
            route_file.close()
            stop_file.close()

train()