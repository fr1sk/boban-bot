import urllib, json, os


def getLocationData(lat, long):
    endpoint = os.environ['ENDPOINT']
    api_key = os.environ['API_KEY']

    origin = str(lat) + "," + str(long)
    print origin
    destination = os.environ['MATF_LOCATION']
    print destination

    nav_request = 'origins={}&destinations={}&mode=walking&key={}'.format(origin,destination,api_key)
    request = endpoint + nav_request

    response = urllib.urlopen(request).read()

    directions = json.loads(response)
    print directions
    # print directions['origin_addresses'][0]
    yourLocation, b, c = directions['origin_addresses'][0].split(',')
    time = directions['rows'][0]['elements'][0]['duration']['text']
    return yourLocation, time