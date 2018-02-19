# google_maps_getter

# LOAD STATIC KEY
staticKey = ''

def getStaticMaps(center=(43.671000, -79.328089), markers=[]):
    """ center is where the map centered about
        markers is list of tuples with (lat, long)
    """

    mapRequest = """https://maps.googleapis.com/maps/api/staticmap?key={}
&center={}, {}
&zoom=13
&format=png
&maptype=roadmap
&size=640x384
&scale=2
&style=features:all|color:0xffffff
&style=element:labels|visibility:off
&style=feature:road|element:geometry.fill|color:0x000000|visibility:on
&style=feature:road.local|visibility:off
&style=feature:transit.station|visibility:off
&style=feature:transit.line|element:geometry|color:0x888888|visibility:off
&markers=anchor:center|size:tiny|icon:http://mineralsy.pl/upload/mineral/icons/domek.png|191+hastings+av+toronto
""".format(staticKey, center[0], center[1])

    for marker in markers:
        mapRequest += '&markers=anchor:center|icon:https://www.comparabus.com/bundles/app/images/favicon/company_le-bus-direct.png|{}, {}'.format(marker[0], marker[1])

    return mapRequest


if __name__ == "__main__":
    import webbrowser
    from TTC_data_getter import getVehicleLocations

    locations = getVehicleLocations(501)
    # locations += getVehicleLocations(506)
    locations += getVehicleLocations(83)


    req = getStaticMaps(markers=locations)
    webbrowser.open(req)
