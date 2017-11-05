from geotext import GeoText


# identify cities
def get_location_details(text):
    places = GeoText(text)
    data = {"cities": places.cities, "countries": places.countries}
    return data