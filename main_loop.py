import time
from collections import deque
from TTC_data_getter import getPredictions, getMultiprediction

""" """


class ttcmodel:
    """ Model has Lines have Times """
    def __init__(self):
        self.routes = deque()

    def addStop(self, route, stop):
        """ """
        self.routes.append((route, stop))

    def nextStop(self):
        """ """
        self.routes.rotate(1)

    def update(self):
        """ iterate through lines, do url get, update """
        thisRoute, thisStop = self.routes[0]
        predictions = getPredictions(thisRoute, thisStop)
        print(predictions)


def main(route_stop_pairs=[]):
    """ route-stop pairs: (route_ID, stop_ID) """
    i = 0
    N = 60

    model = ttcmodel()

    for route_stop in route_stop_pairs:
        model.addStop(route_stop[0], route_stop[1])

    try:
        while True:

            time.sleep(0.5)

            if i % 10 == 0:
                model.nextStop()
                # print("model update")
                model.update()

            # if i % 10 == 0:
                # print("image update")
            # print(i)

            i += 1
            i = i % N

    except KeyboardInterrupt:
        print("done!")


if __name__ == "__main__":

    main(route_stop_pairs=[('31','1292'),     # greenwood north
                           ('83', '7871'),    # jones north
                           ('506', '7935'),   # gerrard at leslie: west
                           ('506', '4875'),   # gerrard at leslie: east
                           ('501', '4456'),   # queen at leslie:   east
                           ('501', '8882')])  # queen at leslie:   west
