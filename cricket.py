from bs4 import BeautifulSoup
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import facebook,os,sys,urllib2,json,pprint,omdb,requests,time,datetime,xlwt,MySQLdb,csv
import numpy as np
import matplotlib.pyplot as plt

def cricket_mail():
	url = "http://www.espncricinfo.com/ci/engine/match/index.html"
	data = BeautifulSoup(requests.get(url).text)
	search_list = data.findAll('a',href=True,text='Live scorecard')
	msg = '<html><body><table style="font-family:Segoe UI;border:1px solid black"><tr><td>TOURNAMENT</td><td>TEAM 1</td><td>TEAM 2</td><td>MATCH STATUS</td><td>LINK</td></tr>'
	for item in search_list:
		try:
			link = "http://www.espncricinfo.com"+item['href']
			data = BeautifulSoup(requests.get(link).text).select('.match-information-strip')[0].findAll(text=True)[0].strip().split("\n")
			tournament = data[0].replace(",","")
			team_1 = BeautifulSoup(requests.get(link).text).select('.team-1-name')[0].findAll(text=True)[0].strip()
			team_2 = BeautifulSoup(requests.get(link).text).select('.team-2-name')[0].findAll(text=True)[0].strip()
			match_status = BeautifulSoup(requests.get(link).text).select('.innings-requirement')[0].findAll(text=True)[0].strip()
			msg += '<tr><td>'+tournament+'</td><td>'+team_1+'</td><td>'+team_2+'</td><td>'+match_status+'</td><td><a href="'+link+'">cricinfo</a></td></tr>'
		except: pass
	msg += '</table></body></html>'
	return msg

def send_mail():
	fromaddr = 'souryapoddar290990@gmail.com'
	toaddr = ["aryapoddar290990@gmail.com","souryapoddar290990@gmail.com"]
	password = "souryaindia"
	subject = "CRICKET UPDATE"
	body = cricket_mail()
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
	# API_KEY = 'o.gmWPEjdjJvbZRqnTvCc7sHkonggCW48I'
	pb = Pushbullet(API_KEY)
	url = "http://www.espncricinfo.com/ci/engine/match/index.html"
	data = BeautifulSoup(requests.get(url).text)
	search_list = data.findAll('a',href=True,text='Live scorecard')
	for item in search_list:
		link = "http://www.espncricinfo.com"+item['href']
		data = BeautifulSoup(requests.get(link).text).select('.match-information-strip')[0].findAll(text=True)[0].strip().split("\n")
		tournament = data[0].replace(",","")
		team_1 = BeautifulSoup(requests.get(link).text).select('.team-1-name')[0].findAll(text=True)[0].strip()
		team_2 = BeautifulSoup(requests.get(link).text).select('.team-2-name')[0].findAll(text=True)[0].strip()
		match_status = BeautifulSoup(requests.get(link).text).select('.innings-requirement')[0].findAll(text=True)[0].strip()
		title = "Cricket"
		text = team_1+" vs "+team_2+"\n"+match_status
		push = pb.push_note(title,text)

# send_push()

# url = 'http://www.espncricinfo.com/ci/engine/match/946815.html'
# data = BeautifulSoup(requests.get(url).text)
# print data



