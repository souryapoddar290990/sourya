from bs4 import BeautifulSoup
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import facebook,os,sys,urllib2,json,pprint,omdb,requests,time,datetime,xlwt,MySQLdb,csv
import numpy as np
import matplotlib.pyplot as plt

def football_mail():
	url = "http://int.soccerway.com/matches/"
	data = BeautifulSoup(requests.get(url).text)
	search_list = data.findAll('a',href=True)
	msg = '<html><body><table style="font-family:Segoe UI;border:1px solid black"><tr><td>TOURNAMENT</td><td>TEAM 1</td><td>TEAM 2</td><td>MATCH STATUS</td><td>LINK</td></tr>'
	for item in search_list:
		# if ('/international/' in item['href']) or ('/national/' in item['href']) and item.findAll('span') != []:
		if '/national/india' in item['href'] and item.findAll('span') != []:
			link = "http://int.soccerway.com"+item['href']
			# print link
			data = BeautifulSoup(requests.get(link).text)#.select('.match-information-strip')[0].findAll(text=True)[0].strip().split("\n")
			print data
	# 	tournament = data[0].replace(",","")
	# 	team_1 = BeautifulSoup(requests.get(link).text).select('.team-1-name')[0].findAll(text=True)[0].strip()
	# 	team_2 = BeautifulSoup(requests.get(link).text).select('.team-2-name')[0].findAll(text=True)[0].strip()
	# 	match_status = BeautifulSoup(requests.get(link).text).select('.innings-requirement')[0].findAll(text=True)[0].strip()
	# 	msg += '<tr><td>'+tournament+'</td><td>'+team_1+'</td><td>'+team_2+'</td><td>'+match_status+'</td><td><a href="'+link+'">cricinfo</a></td></tr>'
	# msg += '</table></body></html>'
	return "msg"

# fromaddr = 'souryapoddar290990@gmail.com'
# toaddr = ["aryapoddar290990@gmail.com","souryapoddar290990@gmail.com"]
# password = "souryaindia"
# subject = "FOOTBALL UPDATE"
# body = football_mail()
# # print body
# msg = MIMEMultipart()
# msg['From'] = fromaddr
# msg['To'] = ",".join(toaddr)
# msg['Subject'] = subject
# msg.attach(MIMEText(body, 'html'))
# server = smtplib.SMTP('smtp.gmail.com', 587)
# server.starttls()
# server.login(fromaddr,password)
# text = msg.as_string()
# server.sendmail(fromaddr, toaddr, text)
# server.quit()	

# import urllib
# image = urllib.URLopener()
# image.retrieve(link,target)
