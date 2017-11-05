import nltk
import airports as Airports
from cities import get_location_details
from date_time import get_datetime_details

# nltk.download('punkt')
sentence = "I want to fly from Bangalore to Aurangabad next tuesday evening"

# Algo flow:
# 1.Find list of cities
# 2.Find their corresponding/nearest Airports
# 3.Find list of Airport Codes
# 4.Find list of times

words = nltk.word_tokenize(sentence)

# 1
cities = get_location_details(sentence)["cities"]
print(cities)
if cities:
    # 2
    city_airports = Airports.get_city_airports(cities)
    print(city_airports)
# 3
airtport_codes = Airports.find_airport_codes(words)
print(city_airports, airtport_codes)

# 4
journey_time = get_datetime_details(sentence)
print(journey_time)
