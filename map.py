import pprint,json,urllib,googlemaps,talkey,os,sys,pyttsx,time
from datetime import datetime

engine = pyttsx.init()
engine.setProperty('rate', 150)
engine.say('WELCOME')

key = 'AIzaSyB0vDdauLIixfUqauZIblqxbzP3hFHLCMw'
latitude = 40.714224
longitude = -73.961452
address = '1600 Amphitheatre Parkway, Mountain View, CA'
source = 'Jadavpur University Campus Area, Jadavpur, Kolkata, West Bengal'
destination = 'Masterda Surya Sen, Bansdroni Post Office Road, Naktala, Bansdroni, Kolkata, West Bengal 700070'
mode = 'transit'
clock = datetime.now()
unit = 'metric'

gmaps = googlemaps.Client(key=key)

# Geocoding an address
# geocode_result = gmaps.geocode(address)
# pprint.pprint(geocode_result)

# Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude))
# pprint.pprint(reverse_geocode_result)

# Request directions via public transit
directions_result = gmaps.directions(source,destination,mode=mode,departure_time=clock,alternatives=True)
total_ways = len(directions_result)
# print directions_result
for index,item in enumerate(directions_result):
	voice = "OPTION "+str(index+1)
	print voice
	engine.say(voice)
	# pprint.pprint(item.keys())
	route = item['legs'][0]
	for item in route['steps']:
		# print item.keys()
		instruction = item['html_instructions']
		distance = item['distance']['text']
		duration = item['duration']['text']
		mode = item['travel_mode']
		voice = mode+' '+instruction+' '+distance+' '+duration.replace('mins','minutes')
		print voice
		# try: time.sleep(int(duration.replace(' mins','')))
		# except: time.sleep(int(duration.replace(' min','')))
		engine.say(voice)
		if mode == 'WALKING':
			text = item['steps']
			for item in text:
				walk_distance = item['distance']['text']
				walk_duration = item['duration']['text']				
				try:
					walk_instruction = item['html_instructions'].replace('<b>','').replace('</b>','').replace('</div>','').replace('&nbsp;',' ')
					walk_instruction = walk_instruction.replace('<div style="font-size:0.9em">',' , ')
					walk_instruction = walk_instruction+' '+walk_distance+' '+walk_duration.replace('mins','minutes')
					# print walk_instruction
				except: pass
			
		if mode == 'TRANSIT':
			text = item['transit_details']
			num_stops = text['num_stops']
			arrival_stop = text['arrival_stop']['name']
			arrival_time = text['arrival_time']['text']
			departure_stop = text['departure_stop']['name']
			departure_time = text['departure_time']['text']
			vehicle_destination = text['headsign']
			vehicle_route = text['line']['name']
			try: vehicle_number = text['line']['short_name']
			except: vehicle_number = ''
			vehicle_type = text['line']['vehicle']['name']
			# print vehicle_type, vehicle_number, vehicle_route, vehicle_destination, departure_stop, departure_time, arrival_stop, arrival_time, num_stops
	# print '--------------------------------------------------------------------------------------------------------------------'
	# break

# url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units='+unit+'&origins='+source+'&destinations='+destination+'&key='+key
# ur = urllib.urlopen(url)
# result = json.load(ur)
# pprint.pprint(result)


engine.runAndWait()