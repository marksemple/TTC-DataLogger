# TTC_data_getter.py

import urllib
import pprint
import xmltodict
from math import floor
from xml.etree import ElementTree

mystops = {'501': '8882',   # queen at leslie, west
           '506': '7935',   # gerrard at leslie west
           '83': '7871',    # jones bus north at gerrard
           '31': '1292'}    # greenwood bus north at gerrard


baseurl = 'http://webservices.nextbus.com/service/publicXMLFeed?command='
# query = 'command=predictionsForMultiStops&a=ttc'
# fullquery = baseurl + query

# for stop in mystops.keys():
#     fullquery += '&stops={}|{}'.format(stop, mystops[stop])


# # print(dir(body))
# # print(body.items())


def getRouteList():
    """ Returns XML like so:
        <body>
            <route tag="92" title="92-Woodbine South"/>
            <route tag="83" title="83-Jones"/>
            ...
        </body>
    """
    routeListQuery = baseurl + 'routeList&a=ttc'
    return routeListQuery


def getRouteConfig(route):
    """ Returns XML like so:
    <body>
        <route tag="83" title="83-Jones" color="ff0000"
                oppositeColor="ffffff"
                latMin="43.654699"
                latMax="43.6810699"
                lonMin="-79.34003"
                lonMax="-79.32667"/>
        ...
    </body>
    """

    routeConfigQuery = baseurl + 'routeConfig&a=ttc'
    # for route in routes:
    if type(route) is int:
        routeConfigQuery += '&r={}'.format(route)
    return routeConfigQuery


def getVehicleLocations(route):
    """ Returns XML like so:
    <body copyright=''>
        <vehccle id="####"" routeTag="##" dirTag="##_X_##"
                 lat="43.659999" lon="-79.328751"
                 secsSinceReport="14"
                 predictable="true" heading="348" />
        <lastTime time="12341523452345"/>
    </body>
    """

    vLocationQuery = baseurl + 'vehicleLocations&a=ttc'

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


def AngleToCompass():
    pass


if __name__ == "__main__":
    import webbrowser

    locations = getVehicleLocations(506)
    print(locations)
    # webbrowser.open(fullquery)

# fullquery = getRouteConfig(routes=[92, 83,])

# print(fullquery)

# with urllib.request.urlopen(fullquery) as myurl:
#     body = ElementTree.parse(myurl).getroot()

# for item in body:
#     print(item.attrib)
    # for route in item:
        # print()
    # print(dir(item))
