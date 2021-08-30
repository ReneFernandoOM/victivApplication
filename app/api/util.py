import requests
from math import radians, sin, cos, asin, sqrt

from flask import current_app
from shapely.geometry import Polygon, Point, LinearRing


MKAD_KM =  [ # [Longitude, Latitude]
        [37.842762,55.774558], [37.842789,55.76522], [37.842627,55.755723], [37.841828,55.747399], [37.841217,55.739103], 
        [37.840175,55.730482], [37.83916,55.721939], [37.837121,55.712203], [37.83262,55.703048], [37.829512,55.694287],
        [37.831353,55.68529], [37.834605,55.675945], [37.837597,55.667752], [37.839348,55.658667], [37.833842,55.650053],
        [37.824787,55.643713], [37.814564,55.637347], [37.802473,55.62913], [37.794235,55.623758], [37.781928,55.617713],
        [37.771139,55.611755], [37.758725,55.604956], [37.747945,55.599677], [37.734785,55.594143], [37.723062,55.589234],
        [37.709425,55.583983], [37.696256,55.578834], [37.683167,55.574019], [37.668911,55.571999], [37.647765,55.573093],
        [37.633419,55.573928], [37.616719,55.574732], [37.60107,55.575816], [37.586536,55.5778], [37.571938,55.581271],
        [37.555732,55.585143], [37.545132,55.587509], [37.526366,55.5922], [37.516108,55.594728], [37.502274,55.60249],
        [37.49391,55.609685], [37.484846,55.617424], [37.474668,55.625801], [37.469925,55.630207], [37.456864,55.641041],
        [37.448195,55.648794], [37.441125,55.654675], [37.434424,55.660424], [37.42598,55.670701], [37.418712,55.67994],
        [37.414868,55.686873], [37.407528,55.695697], [37.397952,55.702805], [37.388969,55.709657], [37.383283,55.718273],
        [37.378369,55.728581], [37.374991,55.735201], [37.370248,55.744789], [37.369188,55.75435], [37.369053,55.762936],
        [37.369619,55.771444], [37.369853,55.779722], [37.372943,55.789542], [37.379824,55.79723], [37.386876,55.805796],
        [37.390397,55.814629], [37.393236,55.823606], [37.395275,55.83251], [37.394709,55.840376], [37.393056,55.850141],
        [37.397314,55.858801], [37.405588,55.867051], [37.416601,55.872703], [37.429429,55.877041], [37.443596,55.881091],
        [37.459065,55.882828], [37.473096,55.884625], [37.48861,55.888897], [37.5016,55.894232], [37.513206,55.899578],
        [37.527597,55.90526], [37.543443,55.907687], [37.559577,55.909388], [37.575531,55.910907], [37.590344,55.909257],
        [37.604637,55.905472], [37.619603,55.901637], [37.635961,55.898533], [37.647648,55.896973], [37.667878,55.895449],
        [37.681721,55.894868], [37.698807,55.893884], [37.712363,55.889094], [37.723636,55.883555], [37.735791,55.877501],
        [37.741261,55.874698], [37.764519,55.862464], [37.765992,55.861979], [37.788216,55.850257], [37.788522,55.850383],
        [37.800586,55.844167], [37.822819,55.832707], [37.829754,55.828789], [37.837148,55.821072], [37.838926,55.811599],
        [37.840004,55.802781], [37.840965,55.793991], [37.841576,55.785017]
]

MKAD_POLYGON = Polygon(MKAD_KM)

def is_point_inside_mkad(point):
    """
    Returns if the Shapely Point is inside the MKAD.
    Input:
        - Shapely Point
    Output:
        - Boolean
    """
    return MKAD_POLYGON.contains(point)

def get_nearest_mkad_point_from_point(point):
    """
    Get the nearest Shapely Point of MKAD from a given Shaeply Point.
    Input:
        - Shapely Point
    Output:
        - Shapely Point: Nearest point
    """
    pol_ext = LinearRing(MKAD_POLYGON.exterior.coords)
    d = pol_ext.project(point)
    closest_point = pol_ext.interpolate(d)
    return closest_point

def calc_distance_between_coords(coords1, coords2):
    """
    Calculate the great circle distance between two coords
    on the earth (specified in decimal degrees)
    Input:
        - Coords1: First pair of coordinates (lon, lat)
        - Coords2: Second pair of coordinates (lon, lat)
    Output:
        - Distance between coords in km
    From: https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    """
    # convert decimal degrees to radians
    lon1, lat1 = coords1
    lon2, lat2 = coords2
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in km
    return c * r

def get_matched_places_from_address(address, max_places_matched=5):
    """
    Returns a dictionary with the Shapely Points of 
    all the places that matched the given address. 
    Input:
        - address
        - max_places_matched (optional): the number of places that the mapbox 
            API will return (maximum limit is 10.)
    Output: 
        - Dictionary: Place name as the key; Shapely Point as value.
    """
    base_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json"
    params = {
        'access_token': current_app.config['MAPBOX_API_KEY'],
        'types': 'address', 'limit': max_places_matched
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    places_with_points = {}

    for place in data['features']:
        place_coords = place['geometry']['coordinates']
        place_point = Point(place_coords[0], place_coords[1])
        places_with_points[place['place_name']] = place_point

    return places_with_points
    
def get_distance_between_mkad_and_address(address):
    """
    Returns the coordinates and distance in km & mi between the 
    mkad and all the places that matched the given address.
    Input: 
        - address
    Output:
        - Dictionary: Address as key; dictionary as value with the
         distance and coordinates of the address.
    """
    matched_places = get_matched_places_from_address(address)
    api_resp = {}
    if matched_places:
        for place, place_point in matched_places.items():
            place_coords = list(place_point.coords)[0] # lon, lat
            api_resp[place] = {
                'lon': place_coords[0], 'lat': place_coords[1],
            }

            if is_point_inside_mkad(place_point):
                api_resp[place]['distance'] = 'This address is inside the Moscow Ring Road'
                continue
                
            closest_mkad_point = get_nearest_mkad_point_from_point(place_point)
            km_distance = calc_distance_between_coords(place_point.coords[0], closest_mkad_point.coords[0])

            api_resp[place]['distance_km'] = km_distance
            api_resp[place]['distance_mi'] = km_distance * 0.62137
    else:
        return False
    
    
    return api_resp


