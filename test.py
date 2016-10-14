import facebook,os,sys,urllib2,json,pprint,omdb,requests,time,datetime,xlwt,MySQLdb,csv,glob,enzyme,subprocess,re,webbrowser
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import smtplib
# import pyscreenshot as ImageGrab
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from PIL import Image,ImageGrab
from collections import Counter
from iplotter import C3Plotter,ChartsJSPlotter

db=MySQLdb.connect(host="localhost",port=3306,user="root",passwd="290990",db="tv")
cursor = db.cursor()
# query = "select season,episode,summary from t1 where serial = 'How Its Made'"
# cursor.execute(query)
# data = cursor.fetchall()
# for item in data:
# 	text = item[2].replace("This episode demonstrates the production processes for ","").replace(", ","/").replace(" and ","/").replace(".","")
# 	print str(item[0])+"."+str(item[1])+"/"+text

# foldername = "G:/ARYA SOURYA/TELEVISION/"

def get_immediate_subfolders(folder_name):
	paths = glob.glob(folder_name+'/*')
	# for path in paths:
		# print path
	return paths

def get_all_subfolders(folder_name):
	for path, subdirs, files in os.walk(folder_name):
		print subdirs

def get_count_total_runtime(foldername):
	count = 0
	temp = []
	for path, subdirs, files in os.walk(foldername):
		for filename in files:
			print filename
			try:
				f = os.path.join(path, filename)
				if f.endswith(".mkv"): 
					with open(f,'rb') as ff:
						count += 1
						details = enzyme.MKV(ff)
						temp.append(details.info.duration)
			except: print "ERROR",filename
	return count,sum(temp,datetime.timedelta())

def get_all_type_files(foldername,filetype):
	temp = []
	for path, subdirs, files in os.walk(foldername):
		for filename in files:
			try:
				f = os.path.join(path, filename)
				if f.endswith(filetype): 
					temp.append(f)
			except: print "ERROR",filename
	return temp

def get_all_mp3_files(foldername):
	temp = []
	for path, subdirs, files in os.walk(foldername):
		for filename in files:
			try:
				f = os.path.join(path, filename)
				if f.endswith(".mp3"): 
					temp.append(f)
			except: print "ERROR",filename
	return temp

def check_chapters(filename):
	command = "mkvmerge --ui-language en --identify-verbose "
	data = subprocess.check_output(command+'"'+filename+'"')
	if "Chapters" in data : return "YES"
	else: return "NO"

def check_corrupt(filename):
	try:
		with open(filename,'rb') as ff:
			details = enzyme.MKV(ff)
			if details.info.duration: return "NO"
	except: return "YES"

def get_duration(filename):
	with open(filename,'rb') as ff:
		details = enzyme.MKV(ff)
		return details.info.duration

def get_folder_duration(foldername,filetype):
	runtime = []
	for item in get_all_type_files(foldername,filetype): runtime.append(get_duration(item))
	return sum(runtime,datetime.timedelta()),len(runtime)

def get_video_audio_details(filename):
	with open(filename,'rb') as ff:
		details = enzyme.MKV(ff)
		video = details.video_tracks[0]
		audio = details.audio_tracks[0]
		return video.height,video.width,video.codec_id,audio.sampling_frequency,audio.codec_id,details.info.duration

def check_capital(name):
	count = []
	title = re.compile('[^a-zA-Z0-9 ]').sub('',name)
	title = re.sub(' +',' ',title)
	# print title.split(" ")
	for item in title.split(" "):
		if len(item) > 0:
			if item[0].isdigit() == False and item[0] != "":
				if item[0].isupper(): count.append(1)
				else: count.append(0)
	# print count
	if len(count) == sum(count): return 1
	else: return 0

def check_filename(filename,cursor):
	try:
		item = filename.replace("\\","/").replace(foldername,"").replace(".mkv","").replace("/","?").split("?")
		# print item
		serial = item[0]
		season = item[1].replace("SEASON ","")
		episode_name = item[2].split(" - ")
		if episode_name[0].isdigit(): 
			episode = int(episode_name[0])
			name = episode_name[1]
			# print serial,season,episode,name
			query = 'select episode,name from t1 where serial="'+serial+'" and season="'+season+'" and episode="'+str(episode)+'"'
			cursor.execute(query)
			data = cursor.fetchall()
			if len(data) != 1: print "UNAVAILABLE",filename,len(data)
			else:
				if check_capital(data[0][1]) == 0: print "DECAPITALIZED",filename
				text = ""
				if int(data[0][0])<10: text += "0"+str(data[0][0])+" - "+data[0][1]
				else: text += str(data[0][0])+" - "+data[0][1]
				if text != item[2]: print "MISMATCH",filename,text,item[2]
				return 1
		else: 
			b = episode_name[0].split("-")
			query = 'select episode,name from t1 where serial="'+serial+'" and season="'+season+'" and episode in ('+str(int(b[0]))+','+str(int(b[1]))+')'
			cursor.execute(query)
			data = cursor.fetchall()
			if len(data) != 2: print "UNAVAILABLE",filename,len(data)
			else:			
				if data[0][1].replace(" - 1","") == data[1][1].replace(" - 2",""): name = data[1][1].replace(" - 2","")
				else: name = data[0][1]+"-"+data[1][1]
				if check_capital(name) == 0: print "DECAPITALIZED",filename
				text = ""
				text += b[0]+"-"+b[1]+" - "+name
				if text != item[2]: print "MISMATCH",filename,text,item[2]
				return 2

	except Exception,e:
		print "UNCONVENTIONAL",filename,e

def get_size(filename):
	stats = os.stat(filename) 
	return stats.st_size

def check_him_present():
	temp = get_all_type_files(foldername+"HOW ITS MADE/",".mkv")
	duration = []
	number = 0
	for item in temp:
		item_new = item.replace(foldername+"HOW ITS MADE/","").split("\\")[2].replace(".mkv","")
		if check_capital(item_new) == 0: print "DECAPITALIZED FILENAME",item_new
		# print item
		corrupt = check_corrupt(item)		
		if corrupt == "YES": print "CORRUPTED FILE",item
		else:
			number += 1
			runtime = get_duration(item)
			height,width,video_codec,frequency,audio_codec,runtime = get_video_audio_details(item)
			if video_codec != "V_MPEGH/ISO/HEVC": print "VIDEO CODEC",item
			if audio_codec != "A_AAC": print "AUDIO CODEC",item	
			duration.append(runtime)
			chapter = check_chapters(item)
			if chapter == "YES": print "CHAPTER PRESENT",item_new

	query = 'select season,episode,name,summary from t1 where serial="How Its Made"'
	cursor.execute(query)
	data = cursor.fetchall()
	serial = "How Its Made"
	len_data = 0
	for item in data:
		season,episode,name,summary = item[0],item[1],item[2],item[3]
		remove = "This episode demonstrates the production processes for "
		for vid in summary.replace(remove,"").replace(" and",",").replace(".","").split(", "):
			if len(vid) == 0: print "MISSING SUMMARY ENTRY",season,episode
			else:
				len_data += 1
				filename = foldername+"HOW ITS MADE/SEASON "+str(season)+"/"+name+"/"+vid+".mkv"
				if os.path.isfile(filename) == False: print "NO FILE",filename
				if check_capital(vid) == 0: print "DECAPITALIZED SUMMARY",filename
	if len(temp) != len_data: print "COUNT MISMATCH"
	print foldername[:len(foldername)-1]+"\HOW ITS MADE DURATION",str(sum(duration,datetime.timedelta())),"COUNT",str(number)
	print "#####################################################################################"

def health_report(foldername,cursor):
	serial_folders = get_immediate_subfolders(foldername)
	for serial in serial_folders:
		if "HOW ITS MADE" in serial:
			check_him_present()
			continue
		if "OTHERS" in serial: continue
		episodes = get_all_type_files(serial,".mkv")
		duration = []
		number = 0
		query = 'select count(*) from t1 where serial="'+serial.replace(foldername[:len(foldername)-1]+"\\","")+'"'
		cursor.execute(query)
		data_count = cursor.fetchone()
		for episode in episodes:
			corrupt = check_corrupt(episode)
			if corrupt == "YES": print "CORRUPTED FILE",episode
			else:
				if "SEASON" in episode:
					number += check_filename(episode,cursor)
					height,width,video_codec,frequency,audio_codec,runtime = get_video_audio_details(episode)
					# print width,episode
					if video_codec != "V_MPEGH/ISO/HEVC": print "VIDEO CODEC",episode
					if audio_codec != "A_AAC": print "AUDIO CODEC",episode
					duration.append(runtime)
				chapter = check_chapters(episode)
				if chapter == "YES": print "CHAPTER PRESENT",episode
				# print episode,"TIME",runtime,"CHAPTER",chapter
		if int(data_count[0]) != number: print "COUNT MISMATCH"
		print serial,"DURATION",str(sum(duration,datetime.timedelta())),"COUNT",str(number)
		print "#####################################################################################"

# health_report(foldername,cursor)

def check_image_size(filename):
	im = Image.open(filename)
	width, height = im.size
	return width,height

def check_images_present(foldername):
	query = 'select serial,season,episode from t1'
	cursor.execute(query)
	data = cursor.fetchall()
	temp = {"a":[],"b":[]}
	for item in data:
		if int(item[2])<10: filename = "0"+str(item[2])+".png"
		else: filename = str(item[2])+".png"
		location = foldername+"/"+item[0]+"/"+str(item[1])+"/"+filename
		if os.path.isfile(location) == False: print "NO PICS",location
		else:
			a,b = check_image_size(location)
			temp["a"].append(a)
			temp["b"].append(b)
	# print Counter(temp["a"])
	# print Counter(temp["b"])

	return 0

# check_images_present("D:/tc\static\img")

def check_db_filename_summary():
	query = 'select serial,season,episode,name,summary from t1'
	cursor.execute(query)
	data = cursor.fetchall()
	for item in data:
		if check_capital(item[3]) == 0: print item
		if item[4].endswith("\n"): print item[:3]
		print item[1],item[2],item[4]
		# time.sleep(1)

# check_db_filename_summary()

# urlnew = urllib2.urlopen(url)
# content = urlnew.read()
# print content

# data = get_all_type_files("E:\New folder/tv\sam x\SEASON 1",".mkv")
# for item in data:
# 	print get_video_audio_details(item)[0],float(get_video_audio_details(item)[1]),item

def take_screenshot(filename,fname):
	webbrowser.open(filename+'.html')
	time.sleep(1)
	im=ImageGrab.grab(bbox=(433,272,933,552))
	im.save(fname+'.png')

# take_screenshot('1-1')

def generate_him_images():
	query = 'select season,episode,name,summary from t1 where serial="How Its Made" and season=19'
	cursor.execute(query)
	data = cursor.fetchall()
	maxm,epi,sea = 0,0,0
	for item in data:
		filename = str(item[0])+"-"+str(item[1])
		if int(item[1]) < 10: fname = str(item[0])+"/"+"0"+str(item[1])
		else: fname = str(item[0])+"/"+str(item[1])
		f = open(filename+".html","w")
		msg = ''
		summary = item[3]
		summary = summary.replace("This episode demonstrates the production processes for ","").replace(" and",",").replace(".","").split(", ")
		# print item[0],item[1],item[2],len(summary)
		if len(summary) == 4: a,b,c,d = summary[0],summary[1],summary[2],summary[3]
		else: a,b,c,d = summary[0],summary[1],summary[2],""
		# print len(a),len(b),len(c),len(d)
		# if len(a)>maxm: maxm,epi,sea = len(a),item[1],item[0]
		# if len(b)>maxm: maxm,epi,sea = len(b),item[1],item[0]
		# if len(c)>maxm: maxm,epi,sea = len(c),item[1],item[0]
		# if len(d)>maxm: maxm,epi,sea = len(d),item[1],item[0]
		# print maxm,sea,epi
		msg += '<html><head><style>body { background-image: url("him_sample_black.png");background-color:red;background-repeat: no-repeat;background-attachment: fixed;background-position: center; } td#a{font-family:Segoe ui light;width:496px;height:70px;font-size:35px;text-align:center;color:white;}</style><body><table style="border-collapse:collapse;margin-top:186px;margin-left:425px;">'
		msg += '<tr><td id="a">'+a+'</td></tr><tr><td id="a">'+b+'</td></tr><tr><td id="a">'+c+'</td></tr><tr><td id="a">'+d+'</td></tr>'
		msg += '</table></body></html>'

		f.write(msg)
		f.close()
		take_screenshot(filename,fname)

generate_him_images()

def get_tv_statistics():
	query = 'select t2.genre,sum(t2.runtime) from t1 inner join t2 where t1.serial=t2.serial group by t2.genre'
	cursor.execute(query)
	result = cursor.fetchall()
	columns = [['Misc',0]]
	misc_list = ['Game','Musical','Science']
	for item in result:
		if item[0] in misc_list:
			columns[0][1] += item[1]
		else:
			columns.append([item[0],item[1]])
	return columns

# columns = get_tv_statistics()

def get_tv_seen_statistics(key,value):
	query = 'select t2.genre,sum(t2.runtime) from t1 inner join t2 where (t1.serial=t2.serial and t1.'+key+' != "'+value+'") group by t2.genre'
	cursor.execute(query)
	result = cursor.fetchall()
	columns = {'Misc':0}
	misc_list = ['Game','Musical','Science']
	for item in result:
		if item[0] in misc_list:
			columns['Misc'] += item[1]
		else:
			columns[item[0]] = item[1]
	return columns

# seena = get_tv_seen_statistics('seena','No')
# seens = get_tv_seen_statistics('seens','No')
# subs = get_tv_seen_statistics('sub','No')
# pics = get_tv_seen_statistics('pics','N')

def generate_donut_chart(columns,title):
	plotter = C3Plotter()
	chart = {
		'data': {
			'columns':columns,
			'type' : 'donut',
		},
		'donut': {
			'title': title
		}
	}
	plotter.plot_and_save(chart)

# generate_donut_chart(columns,"Show Type Statistics")

def generate_radar_chart(labels,data1,data2):
	plotter = ChartsJSPlotter()

	data = {
		"labels": labels,
		"datasets": [
			{
				"label": "Arya",
				"fillColor": "rgba(255,122,122,0.2)",
				"strokeColor": "rgba(255,122,122,1)",
				"pointColor": "rgba(255,122,122,1)",
				"pointStrokeColor": "#000",
				"pointHighlightFill": "#fff",
				"pointHighlightStroke": "rgba(255,122,122,1)",
				"data": data1
			},
			{
				"label": "Sourya",
				"fillColor": "rgba(122,122,255,0.2)",
				"strokeColor": "rgba(122,122,255,1)",
				"pointColor": "rgba(122,122,255,1)",
				"pointStrokeColor": "#000",
				"pointHighlightFill": "#fff",
				"pointHighlightStroke": "rgba(122,122,255,1)",
				"data": data2
			}
		]
	}

	plotter.plot_and_save(data, chart_type="Radar", w=500, h=500)

def generate_radar_data(param1,param2,labels):
	genres = [item[0] for item in labels]
	total = [item[1] for item in labels]
	data1,data2,data3 = [],[],[]
	for index,genre in enumerate(genres):
		try: data1.append(round(param1[genre]/total[index],2))
		except: data1.append(1)
		try: data2.append(round(param2[genre]/total[index],2))
		except: data2.append(1)	
	generate_radar_chart(genres,data1,data2)

# generate_radar_data(seena,seens,columns)
# generate_radar_data(subs,pics,columns)
# webbrowser.open('chart.html')

def get_serial_rating(serial):
	data0,data1,data2 = [],[],[]
	query = 'select season,count(episode),ROUND(sum(rating)/count(episode),2) from t1 where serial = "'+serial+'" group by season'
	cursor.execute(query)
	result = cursor.fetchall()
	for item in result:
		data0.append(item[0])
		data1.append(item[1])
		data2.append(item[2])
	generate_radar_chart(data0,data1,data2)
	webbrowser.open('chart.html')

# get_serial_rating('Sherlock')
# generate_radar_chart(labels,data1,data2)
# webbrowser.open('chart.html')

# ADD RATINGS IN EPISODE PAGE
# ADD STATISTICS PAGE => RUNTIME AND COUNT BASED ON GENRE/SEEN STATUS BASED ON GENRE/SUB AND PICS STATUS/SERIAL RATING STATUS/TOP RATED SERIAL
# ADD FILTER BASED ON GENRE,RUNTIME 

