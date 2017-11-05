import nltk
from geotext import GeoText
import parsedatetime
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.distance import great_circle

sentence = "I want to fly from New Delhi to BOM next tuesday evening"

# identify cities
def get_location_details(text):
    places = GeoText(text)
    data = {"cities":places.cities,"countries":places.countries}
    return data

# identify date
def get_datetime_details(text):
    p = parsedatetime.Calendar()
    time_struct, parse_status = p.parse(text)
    # print time_struct, parse_status
    if parse_status != 0: return datetime(*time_struct[:6])
    return 'error'

# identify location
def get_location(place):
    geolocator = Nominatim()
    location = geolocator.geocode(place)
    return location.address,location.latitude,location.longitude

# identify airport
def get_airport(place):
    add,lat,lon = get_location(place)
    min_dist,closest_place = 99999,[]
    with open('Airport.csv') as f:
        lines = f.readlines()
        for index,line in enumerate(lines):
            if index == 0: continue
            item = line.replace('\n','').split(',')
            if item[4] != '\N':
                air_lat,air_lon = float(item[6]),float(item[7])
                distance = great_circle((lat,lon),(air_lat,air_lon))
                if distance < min_dist:
                    min_dist = distance
                    closest_place = item
    return closest_place

def ngrams(words,n):
    result = []
    for i in range(len(words)-n+1):
        g = ' '.join(words[i:i+n])
        result.append(g)
    return result

# temp = ['midnight','morning','breakfast','noon','lunch','afternoon','evening','dinner','night']
# temp = ['today','tomorrow','friday','next monday','25th aug','11 jul','15th march next year','12/25','12.25','1/7/2020','1.7.2020']
# temp = ['10 days later','2 weeks later','4 months later','1 year later','in 9 days','5 days from next monday','one week and one day later']

"""print get_datetime_details("this month")"""
"""print get_datetime_details("next month")"""
"""print get_datetime_details("next year")"""
"""print get_datetime_details("next week")"""

# print get_location_details(sentence)['cities']
# print get_datetime_details(sentence)
# print get_airport('Delhi')

def get_airport_abb():
    result = {}
    with open('Airport.csv') as f:
        lines = f.readlines()
        for index,line in enumerate(lines):
            if index == 0: continue
            item = line.replace('\n','').split(',')
            if item[4] != '\N':	
            	result[item[4]] = item[2]
	return result

airport_code = get_airport_abb()
words = nltk.word_tokenize(sentence)
cities_spl = [airport_code[item] for item in words if item in airport_code.keys()]
cities = get_location_details(sentence)['cities']
cities += cities_spl
countries = get_location_details(sentence)['countries']
for index,item in enumerate(cities): sentence = sentence.replace(cities[index],'location_'+str(index+1))
journey = get_datetime_details(sentence)

# words_tag = nltk.pos_tag(words)
# print words_tag

# all_grams = list(set(ngrams(words,2)+ngrams(words,3)+ngrams(words,4)+ngrams(words,5)))
# all_datetimes = []
# for item in all_grams:
#     journey = get_datetime_details(item)
#     if journey != 'error':
#         all_datetimes.append(journey)
# print list(set(all_datetimes))