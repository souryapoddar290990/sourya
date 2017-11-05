from geopy.geocoders import Nominatim
from geopy.distance import great_circle

def get_airport_abb():
    result = {}
    with open('../data/Airport.csv') as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            if index == 0: continue
            item = line.replace('\n', '').split(',')
            if item[4] != '\N':
                result[item[4]] = item[2]
        return result


def check_city_exist(place):
    airport_code = get_airport_abb()
    for key,val in airport_code.items():
        if val == place.title(): return key
    return False


def get_city_airports(cities):
    airports = []
    for city in cities:
        city_airport = get_airport(city)
        if city_airport:
            airports.append(city_airport)
    return airports


# identify location
def get_location(place):
    geolocator = Nominatim()
    location = geolocator.geocode(place)
    return location.address, location.latitude, location.longitude


# identify airport
def get_airport(place):
    result = check_city_exist(place)
    if result == False:
        add, lat, lon = get_location(place)
        min_dist, closest_place = 99999, []
        with open('../data/Airport.csv') as f:
            lines = f.readlines()
            for index, line in enumerate(lines):
                if index == 0: continue
                item = line.replace('\n', '').split(',')
                if item[4] != '\N':
                    air_lat, air_lon = float(item[6]), float(item[7])
                    distance = great_circle((lat, lon), (air_lat, air_lon))
                    if distance < min_dist:
                        min_dist = distance
                        closest_place = item
        return closest_place[4]
    else: return result


def ngrams(words, n):
    result = []
    for i in range(len(words) - n + 1):
        g = ' '.join(words[i:i + n])
        result.append(g)
    return result


def find_airport_codes(words):
    airport_code = get_airport_abb()
    return [item for item in words if item in airport_code.keys()]
