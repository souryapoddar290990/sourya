# PACKAGES
import facebook,os,sys,urllib,urllib2,json,pprint,omdb,requests,re,time,datetime,json
import numpy as np
from pytvdbapi import api 
import tmdbsimple as tmdb
from collections import Counter


# GLOBAL VARIABLE DECLARATIONS
access_token = "CAACEdEose0cBAKqwqnYtZAbyR4fh6zUM9Cbab9XDDmV4vaytbTns1NBQ8RqEfLwJkGBu0vLrALmXwg1MyhbtDdkMoUYVhxzf6tCZCbOhh5JzUY1gVszHx0L8ZAEBO5nHOCiZCqx7qaewFgDJiaKNAzDLJ3X1ain5YFrP6dF39cchYxePutxDgZBq0P8ZAyZCq8pFpyH5EAiL0Ii7dL983IZC"
tmdb.API_KEY = "d755eb7a7ed73decd492efae231c484a"
user_movie_persona = {"name":"","movies":[]}
user_serial_persona = {"name":"","serial":[]}
# schedule_url = "http://timesofindia.indiatimes.com/tvschedulejson.cms?userid=0&channellist=Star%20Jalsa,Maa%20TV,Gemini%20TV,POGO,Hungama,Disney%20Channel,Zee%20Telugu,Star%20Utsav,Star%20Vijay,Zee%20Anmol,And%20Pictures,KTV,Star%20Sports%201,UTV%20Movies,Zee%20Bangla,&fromdatetime=201602020000&todatetime=201602030000&deviceview=other&channellogo=1"
channel_list = "Star Plus,Colors,Zee TV,Life OK,Sun TV,SAB TV,Sony Entertainment tv,Star Gold,MAX,Zee Cinema,Nick,Movies OK,Cartoon Network,Star Sports 3,Zee Marathi,Star Jalsa,Maa TV,Gemini TV,Pogo,Hungama,Disney Channel,Zee Telugu,Star Utsav,Star Vijay,Zee Anmol,and Pictures,KTV,Star Sports 1,UTV Movies,Zee Bangla,Udaya TV,UTV Action,B4U Movies,Star Pravah,Asianet,Colors Marathi,Sony Max 2,Aaj Tak,Gemini Movies,Zee Classic,BIG Magic,Colors Kannada,Sony Mix,Channel V,Asianet Suvarna,ABP News,Zee Talkies,India TV,Ten Sports,Discovery channel,Rishtey,Maa Movies,DD1,9x M,Bindass,Zee News,Cinema TV,Sonic,India News,MTV,ABP Majha,National Geographic ch.,B4U Music,Sun Music channel,9X Jalwa,Kalaignar TV,Udaya Movies,Zee Kannada,Sony Pal,Enter 10,Zindagi,Mastiii,Colors Bangla,News24,Polimer TV,Raj TV,Dangal,Disney XD,Jalsha Movies,Zee Tamil,PTC Punjabi,IBN7,Jaya TV,Star Movies,History TV18,Adithya TV,Animal Planet,Chutti TV,Zee 24Taas,Zee Action,ABP Ananda,IBN Lokmat,NDTV India,Surya TV,Isai Aruvi,J Movies,NTV,TV9 Kannada,Gemini Comedy,M Tunes,Mazhavil Manorama,SIX,Zing,Zoom,Tez,Dabangg TV,Aakash Aath,Maa Gold,Sirippoli,Zee Smile,Discovery Kids,E24,Gemini Music,Mi Marathi,Movies Now,Suvarna Plus,Sahara One,TV9 Marathi,Bhakti TV,Filmy,HBO,Jaya Plus,Maa Music,MH1,Ten Cricket,Thanthi TV,9X Tashan,Jaya Max,Kolkata TV,Music India,Nat Geo Wild,Puthiya Thalaimurai,Sarthak TV,Udaya Music,DD News,ETV Andhra Pradesh,Kasturi,Live India TV,Mahuaa TV,PIX,Star Sports 2,Sun News,Tarang TV,WB,Zee Bangla Cinema,Z ETC Bollywood,Zee 24 Ghanta,Colors Gujarati,Fox Life,Kiran TV,Maiboli,Mega TV,PTC Chakde,Sony AATH,Sun Life,TV9 Gujarati,Udaya Comedy,Bindass Play,Asianet Movies,Discovery Science,Gemini Life,Kairali,Kushi TV,OTV,MH One Shraddha,T News,Sangeet Bangla,Suvarna News,9X Jhakaas,Asianet Plus,DD Bangla,DD Punjabi,DD Sahyadri,Discovery Tamil,Murasu,News Express,R Plus News,Saam TV,Star Sports 4,Ten Action,Living Foodz,Zee Q,Captain TV,Chintu TV,Awaaz,DD Podhigai,Disney Junior,Music Xpress,Seithigal 24X7,Star World,TLC,Nick Junior,Asianet News,AXN,Food Food,FX,Jai Maharashtra,Kochu TV,Manorama News,MBC TV,Mega Musiq,PTC News,Star Movies Action,Zee Business,Zee Madhya Pradesh Chhattisgarh,Zee Studio,Makkal TV,Ruposhi Bangla TV,Amrita TV,CNBC TV18,DD Chandana,DD Girnar,DD India,DD Sapthagiri,DD Sports,Colors Oriya,ETV Rajasthan,ID,NDTV Good Times,Polimer Kannada,Prarthana TV,Raj Musix,Raj Musix Kannada,Sakshi TV,Sandesh News,Sangeet Bhojpuri,Times Now,Zee Salaam,India 24x7,Bansal News,ETV Bihar,Janasri News,News Live,Raj Digital,Big Ganga,CNN IBN,DD Bharati,DD Malyalam,Delhi Aajtak,ET Now,ETV MadhyaPradesh,ETV Urdu,ETV Uttar Pradesh,Gemini News,INDIA TODAY,HMTV,I News,India News Haryana,Kasthuri Newz 24,Loksabha TV,Mahuaa Plus,Mathrubhumi News,Peppers TV,Rang,Romedy Now,Sadhna,Samay MP Chhattisgarh,Surya Music,Star Gold HD,Asianet Sitara,MTV International,Al Jazeera,CNN International,Eenadu TV,WOA DW GERMAN,France 24,Baby TV,Nat Geo Music,Nat Geo People,Nat Geo People HD,NEO Prime,Nat Geo Wild HD,HBO Hits,Zee Cinema HD,Zee Cafe,NDTV Profit Prime,NDTV 24x7,Star Plus HD,Star Sports HD 2,BBC india,Discovery channel HD,God TV,NGC HD,Comedy Central,Kairali We,Neo Sports,TV9 Telugu News,Discovery Turbo,Trace Urban HD,Vh1,TV5 Monde Asia,Vasanth TV,Zee Variasi,Aastha,DD Oriya,Star Movies HD,SVBC,Star Sports HD 1,India Talkies,Zee Studio HD,Sony HD,Jaihind TV,3ABN,Mega 24,DD Urdu,DD Kashir,Bloomberg TV India,Ten HD,Sanskar,Jeevan TV,TV5 Telugu,Zee Punjab Haryana Himachal,AMN TV,CNBC Bajar,Animax,ABN Telugu News,Topper TV,FTV,SIX HD,TCM,Australia Plus,9X,Care World,Kairali People,Vanitha TV,Subhavaartha,Shalom TV,P7News,Indiavision,Angel TV,Vissa TV,Colors HD,Mahuaa News,Powervision,Firangi,Star World Premiere HD,Udaya Varthegalu,Samay National,Trace Sport Stars HD,Travel XP,Nepal 1,Star World HD,NewsX,Aastha Bhajan,Zee TV HD,Sri Sankara,CNBC TV18 prime HD,Imayam TV,Gyandarshan,Aradana TV,Chardikla Time TV,Life OK HD,Kappa TV,IBC24,Tamilan TV,Moon TV,Athmeeya Yathra TV,NHK World,Samay UP Uttrakhand,Sahara Samay Mah Guj,Tarang Music,TV1,Mangal Kalash TV,Shop CJ,Darshan 24,DD North East,Satsang,Day And Night News,Raj News 24x7,Total TV,Paras TV,Tara Muzik,Shubh Sandesh,Arihant,Samay Bihar Jharkhand,Win TV,Channel One,Disha TV,ten TV Telugu News,Chithiram,Jan TV,Adhyatma TV,MH1 News,Sobhagya Mithila TV,RT,DY365,KTV HD,History TV18 HD,Yes Indiavision,Sudarshan News,Ishwar TV,Aalami Samay,Gyandarshan 2,Dhoom Music,Sathiyam TV,HBO Hits HD,Sun TV HD,Peace of Mind,Fox Life HD,9XO,Lemon News,Khoj India,M Tunes HD,Anjan TV,Protidin Time,Jano Duniya,Tara News,MediaOne,India News Rajasthan,Soham TV,Channel UFX,Kaumudy TV,TV24,Shalini Plus,Lotus News,Y Plus,Sada Channel,Jinvani TV,Mahaa TV,Gemini TV HD,Oscar Movies,Reporter,Sristi TV,Travel XP HD,Sun Music Channel HD,Baby TV HD,SMBC Insight,Salvation,Bindass Play HD,Bhakti Sagar,Chirithira,Gemini Action,7S Music,4 Real News,Super TV,Janta TV,News Nation,India News UP,NewsTime 24x7,RKM Gold,Raj Musix Malayalam,DD Madhya Pradesh,NTV Bangladesh,Pearls Haryana Express,Lord Buddha,PIX HD,DD Bihar,Ten Cricket HD,Kanak TV,Nat Geo Music HD,The EPIC Channel,Animal Planet HD World,Movies Now HD,Home Shop 18,Sun Action,and TV"
schedule_url_prefix = "http://timesofindia.indiatimes.com/tvschedulejson.cms?userid=0&channellist="
schedule_url_suffix = "&deviceview=other&channellogo=1"

# all_channel = channel_list.split(",")
# for item in sorted(all_channel): print item

channel_type_list = ["movies_soaps","news","sports","others"]
movies_soaps = ["Drama","Filmi","action","comedy","reality show","entertainment","magazine programme","animation","rom-com","thriller","mystery","sitcom","fantasy","horror","romance","tele film","short film","mythology","sci-fi"]
news = ["news","news bulletin","special report","headlines","weather"]
sports = ["cricket","football","tennis","kabaddi","basketball","golf","sport","hockey","badminton","polo","WWE/WWF","Multi-Sport Event","chess","Table Tennis","archery","racing","Volleyball","wrestling"]
others = ["nature","adventure","astrology","consumer","religious","cooking","music","pop","Market Watch","Education (Adult)","Education (Kids)","game show","travel","science","Talk Show","Trailers","Art/Culture","Health and Wellbeing","Fashion","Showbiz","Chat","Astrology","live show","countdown","Others","interactive","request","Food &amp; Cuisine","Factual Entertainment","docu drama","social","classics","interviews","investigation","Agriculture/Rural","lifestyle","detective","Variety Show","special feature", "technology","Entertainment Biz","Biography/Biopic","Events/Festivals","opera","concert","family","culture","Space","Consultation","Award Shows","war","Engineering","Martial Arts","chat show","biography","musical","Popular Science","Dance","Body Science","crime"]

# FUNCTIONS
def check_access_token_validity(access_token):
    try:
        fb_graph_url = "https://graph.facebook.com/v2.5/me?fields=id,name&access_token="+access_token
        api_request = urllib2.Request(fb_graph_url)
        api_response = urllib2.urlopen(api_request)
        return "valid"
    except IOError, e: return e

def get_day_channel_schedule(schedule_channel,schedule_day,schedule_month,schedule_year,feature):
    # print "get_day_channel_schedule"
    schedule_url_channel = schedule_channel+","
    schedule_url_start_time = "&fromdatetime="+schedule_year+schedule_month+schedule_day+"0000"
    schedule_url_end_time = "&todatetime="+schedule_year+schedule_month+schedule_day+"2359"
    schedule_url = schedule_url_prefix+schedule_url_channel+schedule_url_start_time+schedule_url_end_time+schedule_url_suffix
    # print schedule_url
    response = urllib.urlopen(schedule_url)
    data = json.loads(response.read())['ScheduleGrid']['channel'][0]['programme']
    schedule_dict = {"channel":schedule_channel,"title":[],"subgenre":[],"start":[],"stop":[],"duration":[]}
    for item in data:
        schedule_dict["title"].append(item["title"])
        schedule_dict["subgenre"].append(item["subgenre"])
        schedule_dict["start"].append(item["start"])
        schedule_dict["stop"].append(item["stop"])
        schedule_dict["duration"].append(item["duration"])
    if feature == "all": return schedule_dict
    else: return schedule_dict[feature]

def get_movies(access_token):
    # print "get_movies"
    fb_graph_url = "https://graph.facebook.com/v2.5/me?fields=id,name,movies{network,directed_by,name,release_date}&access_token="+access_token
    try:
        api_request = urllib2.Request(fb_graph_url)
        api_response = urllib2.urlopen(api_request)
        try: return json.loads(api_response.read())
        except (ValueError, KeyError, TypeError): return "JSON error"
    except IOError, e: return e

def get_page_likes(access_token):
    # print "get_page_likes"
    fb_graph_url = "https://graph.facebook.com/v2.5/me?fields=id,name,likes.limit(100){category,id,name,likes}&access_token="+access_token
    try:
        api_request = urllib2.Request(fb_graph_url)
        api_response = urllib2.urlopen(api_request)
        try: return json.loads(api_response.read())
        except (ValueError, KeyError, TypeError): return "JSON error"
    except IOError, e: return e

def get_movie_details(movie_title):
    # print "get_movie_details"
    try:
        movie = omdb.title(movie_title)
        # print "MOVIE",movie
        # print movie['plot'],movie['rated'],movie['language'],movie['title'],movie['country']
        # print movie['writer'],movie['year'],movie['metascore'],movie['imdb_id'],movie['director']
        # print movie['released'],movie['imdb_rating'],movie['awards'],movie['poster'],movie['genre']
        # print movie['actors'],movie['runtime'],movie['type'],movie['response'],movie['imdb_votes']
        return [movie['released'],movie['genre'],movie['director'],movie['actors'],movie['language'],movie['imdb_rating'],movie['imdb_id']]
    except: return "NF"

def generate_movie_doc(movie_title,movie_data):
    # print "generate_movie_doc"
    # print movie_title,movie_data
    temp = {"title":movie_title,"year":movie_data[0],"genre":movie_data[1],"director":movie_data[2],"actors":movie_data[3],"language":movie_data[4],"imdb_rating":movie_data[5]}
    # persona.append(temp)
    # return persona
    return temp

def generate_movie_list(access_token):
    # print "generate_movie_list"
    # FETCH DATA FROM FB LIKES
    try:
        page_data = get_page_likes(access_token)
        # print page_data
        user_movie_persona['name'] = page_data['name']    
        data = page_data['likes']['data']
        item_name1 = [item['name'] for item in data if item['category'] in ['Movie']]
    except:
        item_name1 = []

    # FETCH DATA FROM FB MOVIES
    try:
        page_data = get_movies(access_token)
        # print page_data
        item_name2 = [item['name'] for item in page_data['movies']['data']]
    except:
        item_name2 = []

    try:
        # FETCH DATA FROM VIDEOS LIKED
        videos_watched = movie_serial_watched(access_token)
        item_name3 = videos_watched['movie']
    except:
        item_name3 = []

    return list(set(item_name1+item_name2+item_name3))
        
def generate_movie_persona(movie_list):
    # print "generate_movie_persona"
    temp_persona = []
    for movies in movie_list:
        # print movies
        movie = re.sub(r'\([^)]*\)', '', movies)
        movie = movie.encode('utf-8')
        movie_details = get_movie_details(movie)
        # print "MD",movie,movie_details
        if movie_details == "NF":
            search = tmdb.Search()
            response = search.movie(query=movie)
            data = search.results
            if (len(data) == 0) or (data[0]['title'] != movie): 
                # print "MOVIE NOT FOUND",movie
                temp_persona.append(movie)
            else:
                movie_details_original = get_movie_details(data[0]['title'])
                temp_persona.append(generate_movie_doc(movie,movie_details_original))
        else:
            temp_persona.append(generate_movie_doc(movie,movie_details))
    return temp_persona

def movie_feature_scoring(movie_data):
    # print "movie_feature_scoring"
    movie_feature_dict = {"title":[],"actors":[],"director":[],"language":[],"genre":[],"year":[]}
    # print movie_data
    for movie in movie_data:
        if isinstance(movie, str):
            pass
        else:
            year_code = 0
            movie_feature_dict["title"].append(movie['title'])
            if int(movie['year']) <1960 : year_code = 1
            if int(movie['year']) >=1960 : year_code = 2
            if int(movie['year']) >=1990 : year_code = 3
            if int(movie['year']) >=2010 : year_code = 4
            movie_feature_dict["year"].append(year_code)
            for item in movie['actors'].split(", "): movie_feature_dict["actors"].append(item)
            for item in movie['director'].split(", "): movie_feature_dict["director"].append(item)
            for item in movie['genre'].split(", "): movie_feature_dict["genre"].append(item)
            # for item in movie['language'].split(", "): movie_feature_dict["language"].append(item)
            movie_feature_dict["language"].append(movie['language'].split(", ")[0])
            # print movie_feature_dict["language"]
    return movie_feature_dict

def eval_feature(persona_data,to_rate_data,weight):
    # print "eval_feature"
    c = Counter(persona_data)
    t = len(persona_data)
    # print c,t
    if t > 0 :
        score = 0
        for item in to_rate_data:
            # print item,float(c[item]+1)/(t+1)
            score = score + float(c[item])/(t)
        if score == 0: score = 1.0/(t+1)
        # print weight,score,score*weight
        return score*weight
    else: return 0

def movie_schedule_evaluation(movie_schedule,movie_list,persona_score):
    # print "movie_schedule_evaluation"
    final_score = {}
    movie_recommendation = {"show":[],"channel":[]}
    features = {0:'year',1:'actors',2:'director',3:'genre',4:'language'}
    weight = [1,4,1,2,2]
    for movie in movie_schedule["title"]:
        score = 1
        if movie in movie_list: score = 2
        movie_details = generate_movie_persona([movie])
        # print movie_details
        parsed_data = movie_feature_scoring(movie_details)
        for index in range(5): score = score * eval_feature(persona_score[features[index]],parsed_data[features[index]],weight[index])
        # final_score.append(score)
        # print movie,score
        final_score[movie] = score
    movie_recommendation["show"] = sorted(final_score, key=lambda key: final_score[key], reverse=True)
    # print ranked_show
    # print final_score
    movie_recommendation["channel"] = [movie_schedule["channel"][movie_schedule["title"].index(item)] for item in movie_recommendation["show"]]
    return movie_recommendation

def get_recommendation_movie(movie_list,movie_schedule):
    # print "get_recommendation_movie"
    # GET MOVIE DETAILS
    user_movie_persona['movies'] = generate_movie_persona(movie_list)
    # pprint.pprint(user_movie_persona)

    # PERSONA SCORING
    persona_feature_score = movie_feature_scoring(user_movie_persona['movies'])

    # EVALUATE MOVIES
    return movie_schedule_evaluation(movie_schedule,movie_list,persona_feature_score)

def movie_main(access_token):
    # print "movie_main"
    # GET MOVIE LIST
    user_movie_list = generate_movie_list(access_token)
    # print user_movie_list
    # user_movie_list = ["titanic","minions","inception","the wolverine","final destination 2","taare zameen par","sholay","despicable me","pather panchali","megamind","fight club","moneyball","catch me if you can","anand","a beautiful mind"]
    # user_movie_list = ['Three Bolly', 'Pursuit of Happyness', 'An Inconvenient Truth', 'Inside Out', 'The Theory of Everything Movie', u'WALL\u2022E', 'Back to the Future Trilogy', 'Minions', 'Inception', 'Maker', 'Dil Chahta Hai']

    # GET CURRENT TV SCHEDULE
    channel_name = ["HBO","Star Movies","Zee Cinema","Movies OK","Jalsha Movies","MAX","Sony MAX 2","movies now","star world", "Star plus", "star jalsa", "SAB tv", "Sony Entertainment tv","Colors", "Zee Tv"]
    tv_movies_soaps_schedule = get_current_running_movies_soaps(channel_name)
    # pprint.pprint(tv_movies_soaps_schedule)
    tv_movies_schedule = filter_movies(tv_movies_soaps_schedule)

    # GET MOVIE RECOMMENDATION
    movie_recommendation = get_recommendation_movie(user_movie_list,tv_movies_schedule)
    return movie_recommendation
    
def get_all_channel_all_show_subgenre(all_channel):
    # print "get_all_channel_all_show_subgenre"
    show_types = []
    current_time = time.time()
    for item in all_channel:
        try: 
            day,month,year = get_date(current_time)
            for genre in get_day_channel_schedule(item,day,month,year,"subgenre"):
                show_types.append(genre)
            show_types = list(set(show_types))
        except: pass
    return show_types

def get_channel_type(channel_name):
    # print "get_channel_type"
    try:
        current_time = time.time()
        day,month,year = get_date(current_time)
        counts = Counter(get_day_channel_schedule(channel_name,day,month,year,"subgenre")).most_common(1)
        # print counts[0][0].lower()
        if counts[0][0].lower() in [genre.lower() for genre in movies_soaps]: return "movies_soaps"
        if counts[0][0].lower() in [genre.lower() for genre in news]: return "news"
        if counts[0][0].lower() in [genre.lower() for genre in sports]: return "sports"
        if counts[0][0].lower() in [genre.lower() for genre in others]: return "others"    
    except: return "error"

def get_current_running_movies_soaps(channel_name):
    # print "get_current_running_movies_soaps"
    current_time = time.time()
    day,month,year = get_date(current_time)
    shows = {"title":[],"duration":[],"subgenre":[],"channel":[]}
    duration = []
    for channel in channel_name:
        # print channel
        show = get_day_channel_schedule(channel,day,month,year,"all")
        # print start
        show_index = [index for index,timing in enumerate(show["start"]) if get_time(show["stop"][index]) > current_time][0]
        # print "TITLE",show["title"][show_index]
        # print "START",int(show["start"][show_index])
        # print "STOP",int(show["stop"][show_index])
        # print "DURATION",int(show["duration"][show_index])
        # print "LEFT",int((get_time(show["stop"][show_index])-current_time)/60),"mins",int((get_time(show["stop"][show_index])-current_time)%60),"secs"
        shows["title"].append(show["title"][show_index])
        shows["duration"].append((get_time(show["stop"][show_index])-get_time(show["start"][show_index]))/60)
        shows["subgenre"].append(show["subgenre"][show_index])
        shows["channel"].append(channel)
    return shows

def get_time(date):
    # print "get_time"
    #return time.mktime(datetime.datetime.strptime(date,"%Y%m%d").timetuple())
    return time.mktime(datetime.datetime.strptime(date,"%Y%m%d%H%M").timetuple())

def get_date(time):
    # print "get_date"
    temp = datetime.datetime.fromtimestamp(time)
    return temp.strftime("%d"),temp.strftime("%m"),temp.strftime("%Y")

def filter_movies(tv_movies_soaps_schedule):
    # print "filter_movies"
    tv_movies_schedule = {"title":[],"channel":[]}
    for index in range(len(tv_movies_soaps_schedule["title"])):
        if tv_movies_soaps_schedule["duration"][index] > 60.0 :
            tv_movies_schedule["title"].append(tv_movies_soaps_schedule["title"][index])
            tv_movies_schedule["channel"].append(tv_movies_soaps_schedule["channel"][index])
    return tv_movies_schedule

def get_cast_id(movie):
    # print "get_cast_id"
    cast_details = {"name":[],"id":[]}
    cast = get_movie_details(movie)[3].split(", ")
    search = tmdb.Search()
    for item in cast:
        response = search.person(query=item)["results"][0]
        print cast_details["name"].append(response["name"]),cast_details["id"].append(response["id"])
    return cast_details

def get_all_channel_id(all_channel):
    # print "get_all_channel_id"
    current_time = time.time()
    day,month,year = get_date(current_time)
    channel_id = []
    for item in all_channel: 
        print item
        schedule_url_channel = item+","
        schedule_url_start_time = "&fromdatetime="+year+month+day+"0000"
        schedule_url_end_time = "&todatetime="+year+month+day+"0001"
        schedule_url = schedule_url_prefix+schedule_url_channel+schedule_url_start_time+schedule_url_end_time+schedule_url_suffix
        # print schedule_url
        response = urllib.urlopen(schedule_url)
        channel_id.append(json.loads(response.read())['ScheduleGrid']['channel'][0]['channelid'])
    return channel_id

def get_serial_details(serial_title):
    try:
        serial = omdb.title(serial_title)
        # print serial
        db = api.TVDB('B43FF87DE395DF56')
        result = db.search(serial_title, 'en')
        return serial['title'],serial['runtime'],serial['genre'],serial['actors'],serial['language'],serial['imdb_rating'],result[0].Network
    except:
        return "NF",serial_title

def serial_feature_scoring(serial_data):
    # print "serial_feature_scoring"
    serial_feature_dict = {"title":[],"language":[],"genre":[],"channel":[],"duration":[]}
    # print serial_data
    for serial in serial_data:
        if isinstance(serial, str):
            pass
        else:
            serial_feature_dict["title"].append(serial['title'])
            serial_feature_dict["channel"].append(serial['channel'])
            # for item in serial['actors'].split(", "): serial_feature_dict["actors"].append(item)
            for item in serial['genre'].split(", "): serial_feature_dict["genre"].append(item)
            serial_feature_dict["language"].append(serial['language'].split(", ")[0])
            serial_feature_dict["duration"].append(serial['duration'])
            # print serial_feature_dict["language"]
    return serial_feature_dict

def filter_serial(tv_movies_soaps_schedule):
    # print "filter_serial"
    tv_serial_schedule = {"title":[],"channel":[]}
    for index in range(len(tv_movies_soaps_schedule["title"])):
        if tv_movies_soaps_schedule["duration"][index] <= 60.0 :
            tv_serial_schedule["title"].append(tv_movies_soaps_schedule["title"][index])
            tv_serial_schedule["channel"].append(tv_movies_soaps_schedule["channel"][index])
    return tv_serial_schedule

def serial_schedule_evaluation(serial_schedule,serial_list,persona_score):
    # print "serial_schedule_evaluation"
    final_score = {}
    serial_recommendation = {"show":[],"channel":[]}
    features = {0:'channel',1:'duration',2:'genre',3:'language'}
    weight = [1,2,3,4]
    for channel,serial in enumerate(serial_schedule["title"]):
        score = 1
        if serial in serial_list: score = 2
        serial_details = generate_serial_persona([serial])
        # print serial_details
        parsed_data = serial_feature_scoring(serial_details)
        for index in range(4): score = score * eval_feature(persona_score[features[index]],parsed_data[features[index]],weight[index])
        # final_score.append(score)
        # print serial,score
        final_score[serial_schedule["channel"][channel]] = score
    serial_recommendation["channel"] = sorted(final_score, key=lambda key: final_score[key], reverse=True)
    # print ranked_show
    # print final_score
    serial_recommendation["show"] = [serial_schedule["title"][serial_schedule["channel"].index(item)] for item in serial_recommendation["channel"]]
    return serial_recommendation

def serial_main(access_token):
    # print "serial_main"
    # GET SERIAL LIST
    user_serial_list = generate_serial_list(access_token)
    # print user_serial_list
    # user_serial_list = ["titanic","minions","inception","the wolverine","final destination 2","taare zameen par","sholay","despicable me","pather panchali","megamind","fight club","moneyball","catch me if you can","anand","a beautiful mind"]

    # GET CURRENT TV SCHEDULE
    channel_name = ["HBO","Star Movies","Zee Cinema","Movies OK","Jalsha Movies","MAX","Sony MAX 2","movies now","star world", "Star plus", "star jalsa", "SAB tv", "Sony Entertainment tv","Colors", "Zee Tv"]
    tv_movies_soaps_schedule = get_current_running_movies_soaps(channel_name)
    # pprint.pprint(tv_movies_soaps_schedule)
    tv_serial_schedule = filter_serial(tv_movies_soaps_schedule)

    # GET MOVIE RECOMMENDATION
    serial_recommendation = get_recommendation_serial(user_serial_list,tv_serial_schedule)
    return serial_recommendation

def get_recommendation_serial(serial_list,serial_schedule):
    # print "get_recommendation_serial"
    # GET SERIAL DETAILS
    user_serial_persona['serial'] = generate_serial_persona(serial_list)
    # pprint.pprint(user_serial_persona)

    # PERSONA SCORING
    persona_feature_score = serial_feature_scoring(user_serial_persona['serial'])

    # EVALUATE SERIAL
    return serial_schedule_evaluation(serial_schedule,serial_list,persona_feature_score)

def get_serial(access_token):
    # print "get_movies"
    fb_graph_url = "https://graph.facebook.com/v2.5/me?fields=id,name,television{network,directed_by,name,release_date}&access_token="+access_token
    try:
        api_request = urllib2.Request(fb_graph_url)
        api_response = urllib2.urlopen(api_request)
        try: return json.loads(api_response.read())
        except (ValueError, KeyError, TypeError): return "JSON error"
    except IOError, e: return e

def get_video_watches(access_token):
    # print "get_video_watches"
    fb_graph_url = "https://graph.facebook.com/v2.5/me?fields=id,name,video.watches.limit(100)&access_token="+access_token
    try:

        api_request = urllib2.Request(fb_graph_url)
        api_response = urllib2.urlopen(api_request)
        try: return json.loads(api_response.read())
        except (ValueError, KeyError, TypeError): return "JSON error"
    except IOError, e: return e

def movie_serial_watched(access_token):
    data = get_video_watches(access_token)
    videos_watched = {"tv_show":[],"movie":[]}
    # pprint.pprint(data['video.watches']['data'])
    for item in data['video.watches']['data']:
        try:
            if item['data'].keys()[0] == 'tv_show':
                videos_watched['tv_show'].append(item['data']['tv_show']['title'])
                # print item['data']['tv_show']['title']
            if item['data'].keys()[0] == 'movie':
                videos_watched['movie'].append(item['data']['movie']['title'])
                # print item['data']['movie']['title']
        except:
            print item
    return videos_watched

def generate_serial_list(access_token):
    try:
        # FETCH DATA FROM FB LIKES
        page_data = get_movies(access_token)
        # print page_data
        item_name2 = [item['name'] for item in page_data['movies']['data']]
    except:
        item_name2 = []

    # FETCH DATA FROM VIDEOS LIKED
    try:
        videos_watched = movie_serial_watched(access_token)
        item_name3 = videos_watched['tv_show']
    except:
        item_name3 = []

    return list(set(item_name2+item_name3))

def generate_serial_persona(serial_list):
    # print "generate_serial_persona"
    temp_persona = []
    for serial in serial_list:
        # serial = re.sub(r'\([^)]*\)', '', serial)
        serial_details = get_serial_details(serial)
        if len(serial_details) == 2:
            temp_persona.append(serial)
            # print serial,"Not found in tvdb"
        else:
            temp_persona.append(generate_serial_doc(serial,serial_details))
        # # print "SD",serial_details
        # if serial_details == "NF":
        #     search = tmdb.Search()
        #     response = search.serial(query=serial)
        #     data = search.results
        #     if len(data) == 0: 
        #         # print "SERIAL",serial
        #         temp_persona.append(serial)
        #     else:
        #         serial_details_original = get_serial_details(data[0]['title'])
        #         temp_persona.append(generate_doc(serial,serial_details_original))
        # else:
        #     temp_persona.append(generate_doc(serial,serial_details))
    return temp_persona    

def generate_serial_doc(serial_title,serial_data):
    # print "generate_movie_doc"
    temp = {"title":serial_title,"duration":serial_data[1],"genre":serial_data[2],"language":serial_data[4],"channel":serial_data[6]}
    # persona.append(temp)
    # return persona
    return temp

def get_live_sports(channel_list):
    for item in channel_list:
        channel_schedule = get_day_channel_schedule(item,"10","02","2016","all")
        # print channel_schedule
        for index,show in enumerate(channel_schedule["title"]):
            # print show
            if (show.find("live") != -1) or (show.find("Live") != -1):
                print item,channel_schedule["title"][index],channel_schedule["subgenre"][index],channel_schedule["start"][index],channel_schedule["stop"][index]

def get_favourite_athletes(access_token):
    # print "get_movies"
    fb_graph_url = "https://graph.facebook.com/v2.5/me?fields=id,name,favorite_athletes&access_token="+access_token
    try:
        api_request = urllib2.Request(fb_graph_url)
        api_response = urllib2.urlopen(api_request)
        try: return json.loads(api_response.read())
        except (ValueError, KeyError, TypeError): return "JSON error"
    except IOError, e: return e

def get_favorite_teams(access_token):
    # print "get_movies"
    fb_graph_url = "https://graph.facebook.com/v2.5/me?fields=id,name,favorite_teams&access_token="+access_token
    try:
        api_request = urllib2.Request(fb_graph_url)
        api_response = urllib2.urlopen(api_request)
        try: return json.loads(api_response.read())
        except (ValueError, KeyError, TypeError): return "JSON error"
    except IOError, e: return e

# USER INPUT THROUGH COMMAND LINE
# print 'Number of arguments:', len(sys.argv), 'arguments.'
# print 'Argument List:', sys.argv[1]
# access_token = sys.argv[1]

# if check_access_token_validity(access_token) == "valid":
#     print check_access_token_validity(access_token)
#     print "movie recommendation",movie_main(access_token)
#     print "serial recommendation",serial_main(access_token)    
# else:
#     print check_access_token_validity(access_token)

######################################################### TEST ####################################################
# print movie_main(access_token)
# print serial_main(access_token)
# print get_favorite_teams(access_token)
# print get_favourite_athletes(access_token)
# channel_list = ["star sports 1","star sports 2","star sports 3","star sports 4","star sports HD 1","star sports HD 2","ten sports","ten action"]
# print get_current_running_movies_soaps(channel_list)

# print get_current_running_movies_soaps(["HBO","Star Movies","Zee Cinema","Movies OK","Jalsha Movies","MAX","Sony MAX 2","movies now","star world", "Star plus", "star jalsa", "SAB tv", "Sony Entertainment tv","Colors", "Zee Tv"])
# print generate_movie_doc("Khullam Khulla Pyaar Karen",get_movie_details("Khullam Khulla Pyaar Karen"))
# title = ['I, Frankenstein', 'Night At The Museum: Secret Of The Tomb', 'The Real Tiger', 'Khullam Khulla Pyaar Karen', 'Challenge', 'Pratighat - A Revenge', 'Zamaane Ko Dikhana Hai', 'The Three Musketeers', 'Repeat After Me', 'Diya Aur Baati Hum', 'Aaj Aari Kaal Bhaab', 'Taarak Mehta Ka Ooltah Chashmah', 'Crime Patrol Dial 100', 'Krishndasi', 'Sarojini']
# print get_movie_details("the real tiger")
# search = tmdb.Search()
# response = search.movie(query="Blackadder")
# data = search.results
# print data
# for item in title:
#     print item,generate_movie_doc(item,get_movie_details(item))
# print movie_serial_watched(access_token)
# print generate_movie_list(access_token)
# serial_list = generate_serial_list(access_token)
# print serial_list
# for item in serial_list:
#     print get_serial_details(item)
# print get_current_running_movies_soaps(["star plus","star movies","zee cinema","star jalsa","star world"])
# print filter_serial(get_current_running_movies_soaps(["star plus","star movies","zee cinema","star jalsa","star world"]))
# print get_serial_details("dreamworks dragons")
# for item in get_movies(access_token)['movies']['data']:
#     try: print item['name']
#     except: print "none"
#     try: print item['network']
#     except: print "none"
#     try: print item['directed_by']
#     except: print "none"
#     try: print item['release_date']
#     except: print "none"       
#     print ""     
# item['directed_by'],item['network'],item['release_date']

# search = tmdb.Search()
# response = search.movie(query="Suicide Squad")
# data = search.results
# print data
# print len(data),data[0]['release_date'],data[1]['release_date'],data[2]['release_date']
# print get_movie_details("Suicide Squad")
# get_genre()
# print get_all_channel_id(all_channel)

# for index,item in enumerate(all_channel): print index,item,get_channel_type(item)

# pprint.pprint( get_day_channel_schedule("star sports 1","04","02","2016","all"))
# print get_day_channel_schedule("star plus","04","02","2016","subgenre")

# print movie_main(access_token)

# vals = [[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,1,0,1],[1,1,0,1],[1,1,0,1],[0,0,0,1]]
# count = [0,0,0,0]
# for item in range(1,len(vals)):
#     for index in range(4):
#         count[index] += vals[item-1][index]^vals[item][index]
        
# print count
##########################################################################################################################################################################

# form = {"imdb_id": "","show_name": "","show_type": "","show_genre": [],"show_language": "","show_plot": "","show_release_Date": "","show_imdb_rating": "","show_actors": [],"show_director": [],"show_time": "","show_img": "","live_tv": "false"}

# ENGLISH = ["E.T.","Inception","Star Wars","X-Men","Raiders of the Lost Ark","Gladiator","Casino Royale","Moneyball","Harry Potter And The Chamber Of Secrets","Mission: Impossible","Pulp Fiction","The Godfather","Catch Me If You Can","How To Train Your Dragon","Frozen","Kung Fu Panda","The Avengers","The Dark Knight","The Matrix","The Shawshank Redemption"]
# HINDI = ["Sholay","Agneepath","A Wednesday","Deewar","Dil Chahta Hai","Golmaal","The Lunchbox","Bajrangi Bhaijaan","Dilwale Dulhaniya Le Jayenge","Straight from the Heart","Parineeta","Andaz Apna Apna","Hera Pheri","3 Idiots","Lagaan","Kuch Kuch Hota Hai","Welcome","Lagaan","Dabangg","Guru"]
# BENGALI = ["Pather Panchali","The Golden Fortress","Abar Byomkesh","Autograph","The Cloud-Capped Star","Chhadmabeshi","80 te Asio Na","Bhooter Bhabishyat","Charmurti","Buno Haansh","Charulata","Unishe April","The Companion","Paglu","Dui Prithibi","M.L.A. Fatakesto","Apur Panchali","Heerak Rajar Deshe","Deya Neya","The Golden Thread"]
# MARATHI = ["Natsamrat","Katyar Kaljat Ghusali","Mumbai Pune Mumbai 2","Balkadu","Dombivli Fast","Mee Shivajiraje Bhosale Boltoy","Online Binline","Dagadi Chaawl","Coffee Ani Barach Kahi","Timepass","Deool Band","Fandry","Double Seat","Jogwa","Bandh Nylon Che","Aaram Haram Aahe!","Gojiri","Shwaas","TuHiRe","Welcome Zindagi"]
# ORIYA = ["ACP Sagarika","Pagal Premi","Balunga Toka","Sala Budha","Galpa Helebi Sata","Rangila Toka","Mu Premi Mu Pagala","Akashe Ki Ranga Lagila","Suna Panjuri","Paradesi Babu","Super Michhua","Paradeshi Chadhei","Dhauli Express","Aw Aakare Aa","Samaya","Pilata Bigidigala","Matric Fail","Kabi Samrat Upendra Bhanja","Sautuni","Puja Pain Phulatie"]
# KANNADA = ["Hannele Chiguridaga","Bahuparak","Jagajyothi Basaveshwara","Paachi: Paapi Chiraayu","Bombay Mittai","Kanasu Kannu Theredaga","Care Of Footpath 2","Bangalore 560023","Vaasthu Prakaara","Kendasampige","Shivalinga","Buguri","Endendigu","Rhaatee","Beru","Vascodigama","Lodde","Sandhya Raga","RangiTaranga","Bullet Basya"]
# MALAYALAM = ["Perariyathavar","Namukku Parkkan Munthiri Thoppukal","An Off-Day Game","Devasuram","Ullam","Sandesham","Kireedam","Pathemari","Vigathakumaran","Janmadinam","The Ornate Lock","Premam","Bangalore Days","Nadodikkattu","Ennu Ninte Moideen","Butterflies Of The Spraying Rain","Aranazhikaneram","Kilukkam","Etha Oru Snehagatha","In Harihar Nagar"]
# TAMIL = ["Kuruthipunal","Michael Madana Kamarajan","Mouna Ragam","Mahanadi","Anima And Persona","Jigarthanda","Mohammed-Bin-Tughlaq","Enakkul Oru Devathai","Thalapathi","The Chieftain's Son","Love is God","Vishwaroopam","Papanasam","Kaakkaa Muttai","Thillu Mullu","Nayakan","Thani Oruvan","Thanga Padhakkam","Vere Vazhi Ille","Soodhu Kavvum"]
# TELUGU = ["Atharintiki Daaredi","Sagara Sangamam","Kshana Kshanam","Swarnakamalam","Race Gurram","Peda Rayudu","Ninne Pelladatha","Seetharamaiah Gari Manavaralu","Chantabbai","Sankarabharanam ","Gabbar Singh","Daana Veera Soora Karna","Vikramarkudu","Magadheera","Bommarillu","Eega","Pokiri","Shiva","Drushyam","Baahubali: The Beginning"]
# GUJARATI = ["Ek Var Piyu Ne Malva Aavje","Premji: Rise of a Warrior","Happy Familyy Pvt Ltd","Chhello Divas","Bey Yaar","Bas Ek Chance","Gujjubhai the Great","Romance Complicated","Veer Hamirji - Somanath ni Sakhate","Kevi Rite Jaish","Jagat Jogini Maa Khodiyar","Kashino Dikro","Whisky Is Risky","Amdavad No Rikshawalo","Saptapadii","Chaki Kahe Chaka Jo Baka","Aa Te Kevi Dunniya","Vitamin She","Dholi Taro Dhol Waage","Hun Hunshi Hunshilal"]
# ASSAMESE = ["Kothanodi","Local Kung Fu","Marksheet","Halodhia Choraye Baodhan Khai","Ride On The Rainbow","Adomya","Ajeyo","Ito Sito Bahuto","Hkhagoroloi Bohu Door","Haladhar","Aai Kot Nai","Criminal Hunter","Jatinga Ityadi","Rowd","Bakor Putek","Baandhon","Duranir Rong","A Weekend","Turdaksok Mimag","Kalsandhya"]
# PUNJABI = ["Khalsa Mero Roop Hai Khaas","Yaari Jatt Di","Do Lachhiyan","Eh Janam Tumhare Lekhe","Angrej","Yaar Mera Rab Warga","Chaar Sahibzaade","Judge Singh LLB","Ramta Jogi","Kankan De Ohle","Haani","Mitti","Punjab 1984","Nanak Dukhiya Sub Sansar","Chann Pardesee","Ek Noor","Carry On Jatta","Channo Kamli Yaar Di","Do Madari","Jatt Jeona Mour"]

# ENGLISH = ["Friends","Sherlock","The Big Bang Theory","Breaking Bad","House Of Cards","Mr. Bean","Dreamworks Dragons","Homeland","Tom and Jerry","Castle","Two and a Half Men","Narcos","Agents Of S.H.I.E.L.D.","Modern Family","The Flash","Orange Is The New Black","Once Upon A Time","Vampire Diaries","Game Of Thrones","Dragon Ball Z"]
# HINDI = ["Kaun Banega Crorepati","Satyamev Jayate","Bhabi Ji Ghar Par Hai","Khichdi","Crime Patrol","C.I.D.","Shriman Shrimati","Alif Laila","Kumkum Bhagya","Mahabharat","Ramayan","Mahabharat","Naagin","Sasural Simar Ka","Diya Aur Baati Hum","Aahat","Comedy Nights with Kapil","Yeh Hai Mohabbatein","Saath Nibhana Saathiya","Taarak Mehta Ka Ooltah Chashmah"]
# BENGALI = ["Adaalat","CID Kolkata Bureau","No 1 Didi Na Dada","Aamar Durga","Mirakkel 2015","Rajjotok","Tomay Amay Miley","Tumi Asbe Bole","Chokher Tara Tui","Bojhena Shey Bojhena","Bodhuboron","Rannaghar","Deep Jwele Jaai","Dwiragamon","Dadagiri Unlimited","Goyenda Ginni","Maa Durga","Sadhok Bamakhyapa","Tumi Ele Tai","Ichche Nodee"]
# MARATHI = ["Mejwani Paripoorna Kitchen","Asava Sundar Swapnancha Bangla","Saraswati","Jai Malhar","Nanda Saukhya Bhare","Pasant Aahe Mulgi","Mazhe Pati Saubhagyavati","Chala Hawa Yeu Dya","Ka Re Durava","Runji","Priti Pari Tujvari","Lakshya","Durvaa","Devyani","Yek Number","Kamla","Aali Lahar Kela Kahar","Ganpati Bappa Morya","Assa Sasar Surekh Bai","Tu Majha Saangaati"]
# ORIYA = ["Tupur Tapur","Rajkanya","Durga","Udaan","Kumkum","Kanyadana","Sindura Bindu","Ashok Samrat","Sahanai","Rani","Nei Jare Megha Mote","Aina","To Aganara Tulasi Mun","Bhakti Puspanjali","Aeita Arambha","Mou Mana Tori Pai","Tarang Parivaar Maha Muqabila","Sadhaba Bohu","Kisti Barabar","Jai Maa Laxmi"]
# KANNADA = ["Dance Dance","Love Lovike","Anuroopa","Milana","Amratavarshini","Avanu Matte Shravani","Amma","Durga","Manedevaru","Gandhari","Om Shakthi Om Shanthi","Akka","Agnisakshi","Nagini","Punar Vivaha","Mahadevi","Mr & Mrs Range Gowda","Shrirasthu Shubhamasthu","Gruhalakshmi","Jothe Jotheyalli"]
# MALAYALAM = ["Sundari","Ponnambili","Back Benchers","Manjurukum Kaalam","Kathayallithu Jeevitham","Pranayam","Comedy Stars","Parasparam","Sthreedhanam","Chandanamazha","Karutha Muthu","Jeevitham Saakshi","Karyam Nisaram","Manasa Myna","Megha Sandhesham","Sivakami","Punarjani","Chechiyamma","My Marumakan","Indumukhi Chandramathi"]
# TAMIL = ["Poovizhi Vasalile","Abirami","Odi Vilayadu Pappa","Romapuri Paandiyan","Kannammaa","Kalaignarin Ramanujar","Pasamalar","Kula Deivam","Azhagi","Aathira","Vani Rani","Priyamanaval","Vamsam","Deiva Magal","Kalathu Veedu","Kalyanam Mudhal Kaadhal Varai","Saravanan Meenatchi","Deivam Thandha Veedu","Aandaal Azhagar","Seethaiyin Raman"]
# TELUGU = ["Sashirekha Parinayam","Seethamalakshmi","Ramulamma","Chinnari Pelli Kuturu","Mangammagari Manavaralu","Amma Na Kodala","America Ammai","Muddha Mandaram","Rama Seetha","Varudhini Parinayanam","Sravana Sameeralu","Aadavari Matalaku Arthale Verulee","Atho Athamma Kuthuro","Comedy Time","Ranivasam","Srimathi Oka Bahumathi","Idhi Oka Prema Katha","Kalusukovalaani","Na Mogudu","Agnipoolu"]
# GUJRATI = ["Sankat Mochan Hanumaan","Aa Mama Nu Ghar Ketle","Ek Dal Na Pankhi","Jara Juo Jagi Ne","1760 Saasumaa","Tamara Bhai Full To Fatak","Kunvara Corporation","Shyamali","Harta Farta","Araddhya Pappa Nu Sapnu","Je Ichhu E Karnari Hoon","Morari Bapu","Rasoi Show","Flavours of Gujarat","Food Thi Gujarati","Kanho Banyo Common Man","Suri Lavvse Sapna Ni Savar","Kumkum Na Pagla Padya","Preet, Piyu Ane Pannaben","Daily Bonus"]
# ASSAMESE = ["Adajhya","Brahmaputra Ke Kinare","Beyond The Flowers","Bandhan Tute Na","Prantore Prantore","Hello Dispur","Mritunjaya","Arunabh Prabin","Din Pratidin","Dharti Ke Goad Mein","Debi Choudhurani","Morning Tunes","Pushpanjali","Borala Kai","Nandini","Geetor Godhuli","Jonali LLB","Mayabini Rati K","Oi Khapla","Bharghar"]
# PUNJABI = ["Ki Haal Chaal Hai","Campus Punjabi","Bach Ke Mod Ton","Power Punch","Living Treasure","Chamkade Sitare","Simran","Des Pardes","Fuffad Da Funda","Nidar","Tashan De Peg","Gyan Da Sagar","Dil Khol Ke Bol","Shurlian","Amrit Dhara","Mera Pind Mere Khet","Bhai Guriqbal Singh Ji","Dus Da Dum","Meri Awaaz","Dhol Dhamaka"]

# NEWS_ENGLISH = ["Times Now","India Today"],[12751,12769]
# NEWS_HINDI = ["Aaj Tak","Zee News"],[12562,12580]
# NEWS_BENGALI = ["24 Ghanta","Kolkata TV"],[12671,12653]
# NEWS_MARATHI = ["ABP Majha","Mi Marathi"],[12858,12638]
# NEWS_ORIYA = ["Odisha TV","Kanak TV"],[12688,12973]
# NEWS_KANNADA = ["TV9 Kannada","Suvarna News"],[12622,12692]
# NEWS_MALAYALAM = ["Mathrubhumi News","Asianet News"],[12776,12717]
# NEWS_TAMIL = ["Kalaignar Seithigal","Captain News"],[13147,13011]
# NEWS_TELUGU = ["ABN Andhra Jyothi","Sakshi TV"],[12991,12748]
# NEWS_GUJRATI = ["TV9 Gujarati","Sandesh News"],[12680,12749]
# NEWS_ASSAMESE = ["Pratidin Time","DY 365"],[12929,12910]
# NEWS_PUNJABI = ["PTC News","Day And Night News"],[12726,13083]
# NEWS_OTHERS = ["NDTV Profit","CNBC Awaaz"],[12728,13004]

# SPORTS = ["cricket","football","tennis","kabaddi","basketball","golf","polo","hockey","badminton","wwe/wwf","chess","table tennis","archery","racing","volleyball","wrestling"]
# EVENTS = ["Asia Cup 2016","World Cup T20 2016","Hockey India League","I-League","Pro Kabaddi League","Barclays Premier League","La Liga","Bundesliga","Seria A","Champions League","Atp World Tour"]

# data = []
# arr = []
# for item in data:
    # data = get_movie_details(item)
    # print item,data[1],data[4].split(",")[0]
    # form['show_name'],form['show_genre'],form['show_language'] = item,label[index],'Punjabi'
    # form['show_name'],form['show_genre'],form['show_language'],form['show_type'],form['show_release_Date'],form['show_director'],form['show_actors'],form['imdb_id'],form['show_imdb_rating'] = item,data[1],data[4].split(",")[0],'movie',data[0],data[2],data[3],data[5],data[6]
    # print item,form['show_language']
    # arr.append(item)
    # print form

# print json.dumps(arr)

# import pycountry
# country_list = pycountry.countries
# print country_list
# from iso3166 import countries
# for country in countries: 
#     try: print country.name
#     except: pass

# import math
# from random import randint,sample
# a1 = [100+item for item in range(20)]
# a2 = [200+item for item in range(20)]
# a3 = [300+item for item in range(20)]
# a4 = [400+item for item in range(20)]
# a5 = [500+item for item in range(20)]
# a6 = [600+item for item in range(20)]

# num_lang = 3
# total = 5
# per_num = int(math.ceil(float(total)/num_lang))

# b1 = [a1[randint(0,19)] for item in range(per_num)]
# b2 = [a2[randint(0,19)] for item in range(per_num)]
# b3 = [a3[randint(0,19)] for item in range(per_num)]
# b4 = [a4[randint(0,19)] for item in range(per_num)]
# b5 = [a5[randint(0,19)] for item in range(per_num)]
# b6 = [a6[randint(0,19)] for item in range(per_num)]

# semifinal = b1+b2+b3
# final = [semifinal[item] for item in sample(range(len(semifinal)), total)]
# print final

# HINDI = ["Straight From The Heart"]["Hum Dil De Chuke Sanam"]
# BENGALI = ["The Golden Fortress","The Cloud-Capped Star","The Companion","The Golden Thread"]["Sonar Kella","Meghe Dhaka Tara","Dosar","Subarnarekha"]
# MALAYALAM = ["The Ornate Lock","Butterflies Of The Spraying Rain"]["Manichithrathazhu","Thoovanathumbikal"]
# TAMIL = ["Anima And Persona","The Chieftain's Son","Love is God"]["Aaranya Kaandam","Thevar Magan","Anbe Sivam"]
# ASSAMESE = ["Ride On The Rainbow"]["Konikar Ramdhenu"]

# def get_page_posts(access_token,page_id):
#     fb_graph_url = "https://graph.facebook.com/v2.5/"+str(page_id)+"/posts?limit=100&access_token="+access_token
    
#     try:
#         api_request = urllib2.Request(fb_graph_url)
#         api_response = urllib2.urlopen(api_request)
#         try: return json.loads(api_response.read())
#         except (ValueError, KeyError, TypeError): return "JSON error"
#     except IOError, e: return e

# access_token = "CAACEdEose0cBAMsHBhc1ZBUzWJj97Y0O5eKfUxzhkutPax8o0aDqIvKoZBJSVMo0XXzRjN5vCVXs8R0KOLDJHdfRd5yQWFlk2fhLZAy5M9xKETc2NawPVEFItF9AIYRsq1wgjk5w8LnYxnS02O07B2TBlyGZA3YRXZA946E6HmmU5P3jhoJcqKm8aNGTPJDHZBGZCJ7aeZBZAGG5M4ZASPq6SA"
# page_id = 140954695932203
# all_data = get_page_posts(access_token,page_id)
# posts = all_data['data']
# page_next = all_data['paging']['next']
# page_prev = all_data['paging']['previous']
# print posts




