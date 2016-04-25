import facebook,urllib,urllib2,json

def get_page_posts(access_token,page_id):
    fb_graph_url = "https://graph.facebook.com/v2.5/"+str(page_id)+"/posts?limit=100&access_token="+access_token
    
    try:
        api_request = urllib2.Request(fb_graph_url)
        api_response = urllib2.urlopen(api_request)
        try: return json.loads(api_response.read())
        except (ValueError, KeyError, TypeError): return "JSON error"
    except IOError, e: return e

access_token = "CAACEdEose0cBAMsHBhc1ZBUzWJj97Y0O5eKfUxzhkutPax8o0aDqIvKoZBJSVMo0XXzRjN5vCVXs8R0KOLDJHdfRd5yQWFlk2fhLZAy5M9xKETc2NawPVEFItF9AIYRsq1wgjk5w8LnYxnS02O07B2TBlyGZA3YRXZA946E6HmmU5P3jhoJcqKm8aNGTPJDHZBGZCJ7aeZBZAGG5M4ZASPq6SA"
page_id = 140954695932203
all_data = get_page_posts(access_token,page_id)
posts = all_data['data']
page_next = all_data['paging']['next']
page_prev = all_data['paging']['previous']
print posts