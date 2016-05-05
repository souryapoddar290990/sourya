import requests,time,csv,pprint,sys,xlwt,datetime,MySQLdb
from bs4 import BeautifulSoup
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

def serial_search(url_temp):
    serial = raw_input('Please enter serial name: ')
    url_page0 = url_temp + 'api/GetSeries.php?seriesname=' + serial
    text0 = BeautifulSoup(requests.get(url_page0).text)
    search_list = text0.findAll('series')
    serial_list = []
    for index,serials in enumerate(search_list): serial_list.append([search_list[index].find('seriesid').text,search_list[index].find('seriesname').text])
    return len(serial_list),serial_list

def serial_finalize(serial_list,flag0,series_id):
    for index,item in enumerate(serial_list): print index+1,item[1]
    series_id_temp = int(raw_input('Please enter serial option: '))-1
    if series_id_temp >=0 and series_id_temp<flag0: return 1, serial_list[series_id_temp][0]
    else: return 0, 0

def serial_details_display(url_temp,series_id):
    url_page1 = url_temp + '?tab=series&id=' + series_id + '&lid=7'
    text1 = BeautifulSoup(requests.get(url_page1).text)
    summary = text1.select('#content')[0].findAll(text=True)[2].replace("\t","").replace("\n","").encode('utf-8')
    serial = text1.select('#content')[0].findAll(text=True)[1].replace("\t","").replace("\n","").encode('utf-8')
    network = text1.select('#content')[1].findAll(text=True)[36].replace("\t","").replace("\n","").encode('utf-8')
    if len(network) == 0: print serial,"\n","No Data","\n"+summary
    else: print series_id,"\n",serial,"\n",network,"\n"+summary
    return serial	

def episodes_download(serial,url_temp,series_id):
	url_page2 = url_temp + '?tab=seasonall&id=' + series_id + '&lid=7'
	text2 = BeautifulSoup(requests.get(url_page2).text)
	filename = serial.title() + ".xls"
	book = xlwt.Workbook(encoding="utf-8")
	sheet1 = book.add_sheet("All")
	row_num_count = 0
	for row_num in range(1,len(text2.select("#listtable tr"))):
		table_row = text2.select("#listtable tr")[row_num]
		table_cells = table_row.findAll('td')
		relative_link_to_episodes = table_cells[0].find('a')['href']
		try:
			season,episode = int(table_cells[0].find('a').text.strip().split(" x ")[0]),int(table_cells[0].find('a').text.strip().split(" x ")[1])
			name = table_cells[1].find('a').text.strip().title()
			date = table_cells[2].text.strip().split("-")
			day,month,year = int(date[2]),int(date[1]),int(date[0])
			absolute_link_to_episodes = url_temp + relative_link_to_episodes
			text3 = BeautifulSoup(requests.get(absolute_link_to_episodes).text)
			summary = text3.select("#datatable tr")[7].findAll('td')[1].findAll('textarea', {'name':'Overview_7'})[0].text.strip()
			sheet1.write(row_num_count,0,serial)
			sheet1.write(row_num_count,1,season)
			sheet1.write(row_num_count,2,episode)
			sheet1.write(row_num_count,3,name)
			sheet1.write(row_num_count,4,day)
			sheet1.write(row_num_count,5,month)
			sheet1.write(row_num_count,6,year)
			sheet1.write(row_num_count,7,summary)
			row_num_count += 1
		except:pass
	book.save(filename)

def episodes_view(serial,url_temp,series_id):
	url_page2 = url_temp + '?tab=seasonall&id=' + series_id + '&lid=7'
	text2 = BeautifulSoup(requests.get(url_page2).text)
	for row_num in range(1,len(text2.select("#listtable tr"))):
		try:
			table_row = text2.select("#listtable tr")[row_num]
			table_cells = table_row.findAll('td')
			relative_link_to_episodes = table_cells[0].find('a')['href']
			season,episode = int(table_cells[0].find('a').text.strip().split(" x ")[0]),int(table_cells[0].find('a').text.strip().split(" x ")[1])
			name = table_cells[1].find('a').text.strip().title()
			date = table_cells[2].text.strip().split("-")
			date_new = date[2]+"/"+date[1]+"/"+date[0]
			absolute_link_to_episodes = url_temp + relative_link_to_episodes
			text3 = BeautifulSoup(requests.get(absolute_link_to_episodes).text)
			summary = text3.select("#datatable tr")[7].findAll('td')[1].findAll('textarea', {'name':'Overview_7'})[0].text.strip()
			# print season,episode,name,date_new,summary
			print 'insert into t1 values ("'+serial.title()+'","'+name.title()+'",'+str(season)+','+str(episode)+',"No","No","No",'+str(date[2])+','+str(date[1])+','+str(date[0])+',"'+summary+'","N","N");'
		except: pass

def main_funct():
	url_temp, flag0, flag1, flag2, series_id = 'http://thetvdb.com/', 0, 0, 0, 0
	while flag2 == 0:
		while flag0 == 0: flag0, serial_list = serial_search(url_temp)
		while flag1 == 0: flag1, series_id = serial_finalize(serial_list,flag0,series_id)
		serial = serial_details_display(url_temp,series_id)
		while flag2 == 0:
			print 1, "View episodes"
			print 2, "Download episodes"
			print 3, "Return to search"
			print 4, "Exit"
			option = int(raw_input("select option: "))
			if option >= 1 and option <= 4: flag2 = option
		if flag2 == 1: episodes_view(serial,url_temp,series_id)
		if flag2 == 2: episodes_download(serial,url_temp,series_id)
		if flag2 == 3: flag0, flag1, flag2 = 0, 0, 0	
		if flag2 == 4: return 0

# main_funct()

def episodes_view_future():
	info = raw_input('Please enter details: ').split(",")
	url_temp,serial,season_exist,episode_exist,series_id = 'http://thetvdb.com/',info[0],int(info[1]),int(info[2]),info[3]
	url_page2 = url_temp + '?tab=seasonall&id=' + series_id + '&lid=7'
	text2 = BeautifulSoup(requests.get(url_page2).text)
	for row_num in range(1,len(text2.select("#listtable tr"))):
		try:
			table_row = text2.select("#listtable tr")[row_num]
			table_cells = table_row.findAll('td')
			relative_link_to_episodes = table_cells[0].find('a')['href']
			season,episode = int(table_cells[0].find('a').text.strip().split(" x ")[0]),int(table_cells[0].find('a').text.strip().split(" x ")[1])
			if season < season_exist: pass
			if (season == season_exist and episode > episode_exist) or (season > season_exist):
				name = table_cells[1].find('a').text.strip().title()
				date = table_cells[2].text.strip().split("-")
				date_new = date[2]+"/"+date[1]+"/"+date[0]
				absolute_link_to_episodes = url_temp + relative_link_to_episodes
				text3 = BeautifulSoup(requests.get(absolute_link_to_episodes).text)
				try: summary = text3.select("#datatable tr")[7].findAll('td')[1].findAll('textarea', {'name':'Overview_7'})[0].text.strip()
				except: summary = ""
				print 'insert into t1 values ("'+serial.title()+'","'+name.title()+'",'+str(season)+','+str(episode)+',"No","No","No",'+str(date[2])+','+str(date[1])+','+str(date[0])+',"'+summary+'","N","N");'
		except Exception,e: print e

# episodes_view_future()

def get_date(time):
	temp = datetime.datetime.fromtimestamp(time)
	return temp.strftime("%d"),temp.strftime("%m"),temp.strftime("%Y")

def episodes_today(serial,url_temp,series_id,today):
	doc = []
	url_page2 = url_temp + '?tab=seasonall&id=' + series_id + '&lid=7'
	text2 = BeautifulSoup(requests.get(url_page2).text)
	for row_num in range(1,len(text2.select("#listtable tr"))):
		try:
			table_row = text2.select("#listtable tr")[row_num]
			table_cells = table_row.findAll('td')
			season,episode = int(table_cells[0].find('a').text.strip().split(" x ")[0]),int(table_cells[0].find('a').text.strip().split(" x ")[1])
			date = table_cells[2].text.strip()
			if date == today: doc.append(serial+','+str(season)+','+str(episode))
			else: pass
		except Exception,e: pass
	return doc

def serial_mail():
	current_time = time.time()-86400
	day,month,year = get_date(current_time)	
	today = str(year)+'-'+str(month)+'-'+str(day)
	# print today
	kickass = 'http://kickass.to/usearch/'
	db=MySQLdb.connect(host="localhost",port=3306,user="root",passwd="290990",db="tv")
	cursor = db.cursor()
	query = "select serial,tvdb_id,name from t3"
	cursor.execute(query)
	data = cursor.fetchall()
	msg = '<html><body><table style="font-family:Segoe UI;border:1px solid black"><tr><td>SERIAL</td><td>SEASON</td><td>EPISODE</td><td>NAME</td><td>LINK</td><tr>'
	for item in data:
		# print item
		doc = episodes_today(item[0],"http://thetvdb.com/",str(item[1]),today)
		for vals in doc:
			val = vals.split(",")
			serial,season,episode = val[0],int(val[1]),int(val[2])
			if season < 10: season_text = '0'+str(season)
			else: season_text = str(season)
			if episode < 10: episode_text = '0'+str(episode)
			else: episode_text = str(episode)				
			search = kickass+serial+' S'+season_text+'E'+episode_text+' 720p'
			# print serial,season,episode
			# print search
			msg += '<tr><td>'+serial+'</td><td>'+str(season)+'</td><td>'+str(episode)+'</td><td>'+item[2]+'</td><td><a href="'+search+'">kickass</a></td></tr>'
	msg += '</table></body></html>'
	return msg

def send_mail():
	fromaddr = 'souryapoddar290990@gmail.com'
	toaddr = ["aryapoddar290990@gmail.com","souryapoddar290990@gmail.com"]
	password = "souryaindia"
	subject = "SERIAL UPDATE"
	body = serial_mail()
	# print body
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = ",".join(toaddr)
	msg['Subject'] = subject
	msg.attach(MIMEText(body, 'html'))
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr,password)
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

send_mail()

def send_push():
	from pushbullet import Pushbullet
	API_KEY = 'o.nYHrQiyqBr2NTj59HaQFSSGsgoLDYQrv'
	API_KEY = 'o.gmWPEjdjJvbZRqnTvCc7sHkonggCW48I'
	pb = Pushbullet(API_KEY)
	current_time = time.time()-86400
	day,month,year = get_date(current_time)	
	today = str(year)+'-'+str(month)+'-'+str(day)
	kickass = 'http://kickass.to/usearch/'
	db=MySQLdb.connect(host="localhost",port=3306,user="root",passwd="290990",db="tv")
	cursor = db.cursor()
	query = "select serial,tvdb_id,name from t3"
	cursor.execute(query)
	data = cursor.fetchall()
	title = "Serial"
	text = ""
	for item in data:
		doc = episodes_today(item[0],"http://thetvdb.com/",str(item[1]),today)
		for vals in doc:
			val = vals.split(",")
			serial,season,episode = val[0],val[1],val[2]
			text += serial+' '+season+'.'+episode+'\n'
	push = pb.push_note(title,text)

# send_push()



