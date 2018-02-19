import urllib
import xmltodict
from xml.etree import ElementTree

agency = 'ttc'
baseurl = 'http://webservices.nextbus.com'
baseurl += '/service/publicXMLFeed?a={}&command='.format(agency)

""" Helper functions for interacting with the NEXTBUS API
    There are more query commands that can be used,
    but for my current needs these ones were sufficient.
    I want to periodically poll the API for my nearest transit predictions
    and then do something with that later.
"""


def getRouteConfig(route):
    """ Returns XML:
    <body>
        <route>
    """

    query = baseurl + 'routeConfig'
    query += '&r={}'.format(route)
    with urllib.request.urlopen(query) as myurl:
        body = ElementTree.parse(myurl).getroot()
    for item in body:
        for ii in item:
            print(ii.attrib)


def getVehicleLocations(route):
    """ Returns XML like so:
    <body copyright=''>
        <vehicle id="####"" routeTag="##" dirTag="##_X_##"
                 lat="43.659999" lon="-79.328751"
                 secsSinceReport="14"
                 predictable="true" heading="348" />
        <lastTime time="12341523452345"/>
    </body>
    """

    vLocationQuery = baseurl + 'vehicleLocations&a={}'.format(agency)

    if type(route) is int:
        vLocationQuery += '&r={}'.format(route)

    vLocationQuery += '&t=0'

    with urllib.request.urlopen(vLocationQuery) as myurl:
        body = ElementTree.parse(myurl).getroot()

    vLocations = []
    for item in body:
        print(item)
        print(item.attrib)
        if 'lat' not in item.attrib:
            continue
        else:
            vLocations.append((float(item.attrib['lat']),
                               float(item.attrib['lon'])))

    return vLocations


def getPredictions(route, stop):
    """ get single prediction for stop at route """

    myPrediction = {'route': route,
                    'direction': 'N/A',
                    'stopTitle': 'N/A',
                    'times': []}

    query = baseurl + 'predictions&s={}&r={}'.format(stop, route)

    with urllib.request.urlopen(query) as myurl:
        body = ElementTree.parse(myurl).getroot()

    for predictions in body:
        routeTag = predictions.get('routeTag')
        myPrediction['stopTitle'] = predictions.get('stopTitle')

        for direction in predictions:

            try:
                dirr = direction.get('title')
                dirr = dirr.split()[0]
                myPrediction['direction'] = dirr
            except AttributeError:
                pass

            for idx, prediction in enumerate(direction):
                if idx < 3:
                    time = prediction.get('minutes')
                    myPrediction['times'].append(time)

    return myPrediction


def getMultiprediction(RouteStop_pairs):
    """ <body: copyright>
            <predictions: agency, routetag, stoptitle>
                <direction: title>
                    <prediction: minutes>"""

    query = baseurl + 'predictionsForMultiStops'

    for stop in RouteStop_pairs:
        query += '&stops={}|{}'.format(stop[0], stop[1])

    print(query)

    with urllib.request.urlopen(query) as myurl:
        body = ElementTree.parse(myurl).getroot()

    for predictions in body:
        routeTag = predictions.get('routeTag')
        stopTitle = predictions.get('stopTitle')
        for direction in predictions:
            dirr = direction.get('title')
            dirr = dirr.split()[0]
            for idx, prediction in enumerate(direction):
                if idx > 0:
                    continue
                minutes = prediction.get('minutes')
                print('{} {} {}: {} minutes'.format(routeTag,
                                                    dirr,
                                                    stopTitle,
                                                    minutes))


if __name__ == "__main__":

    getMultiprediction([('31','1292'),     # greenwood north
                        ('83', '7871'),    # jones north
                        ('506', '7935'),   # gerrard at leslie: west
                        ('506', '4875'),   # gerrard at leslie: east
                        ('501', '4456'),   # queen at leslie:   east
                        ('501', '8882')])  # queen at leslie:   west

