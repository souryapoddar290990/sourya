import facebook,os,sys,urllib2,json,pprint,omdb,requests,time,datetime
import numpy as np
from nsetools import Nse
from yahoo_finance import Share
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

# access_token = "CAACEdEose0cBACcbcO3W950l2rnlRW3N2nBtlTitjewLIuBhIvT7Os19AZAAz8spALhohbjMKfRZBIukCAITnRY4LuApYUYp0sIl0ZASXRBrMFgZBflj6pXX69SdlF0HZCKTGmiFREY4vZAdS57UhN4qLOjEThYrU0NvDrT0Mn8bSm0cwGw7iYbu00kdJdkTpuyXfmdBznQwZDZD"
# graph = facebook.GraphAPI(access_token)
# profile = graph.get_object("me")
# friends = graph.get_connections("me", "friends")
# graph.put_object("me", "feed", message="I am writing on my wall!")

# count = 0
# while(1):
#     count += 1
#     nse = Nse()
#     # print nse
#     q = nse.get_quote('SBIN')
#     print count,q
#     time.sleep(15)
# nifty_quote = nse.get_index_quote('NIFTY BANK')
# pprint.pprint(nifty_quote)
# all_stock_codes = nse.get_stock_codes()
# pprint.pprint(all_stock_codes)
# index_codes = nse.get_index_list()
# pprint.pprint(index_codes)
# adv_dec = nse.get_advances_declines()
# pprint.pprint(adv_dec)
# top_gainers = nse.get_top_gainers()
# pprint.pprint(top_gainers)
# top_losers = nse.get_top_losers()
# pprint.pprint(top_losers)
# print nse.is_valid_code('INFY')
# print nse.is_valid_index('NIFTY BANK')


# def get_google_data(symbol, period, window):
#     url_root = 'http://www.google.com/finance/getprices?i='
#     url_root += str(period) + '&p=' + str(window)
#     url_root += 'd&f=d,o,h,l,c,v&df=cpct&q=' + symbol
#     print url_root
#     response = urllib2.urlopen(url_root)
#     data = response.read().split('\n')
#     pprint.pprint(data)
#     #actual data starts at index = 7 first line contains full timestamp, every other line is offset of period from timestamp
#     parsed_data = []
#     anchor_stamp = ''
#     end = len(data)
#     for i in range(7, end):
#         cdata = data[i].split(',')
#         if 'a' in cdata[0]:
#             #first one record anchor timestamp
#             anchor_stamp = cdata[0].replace('a', '')
#             cts = int(anchor_stamp)
#         else:
#             try:
#                 coffset = int(cdata[0])
#                 cts = int(anchor_stamp) + (coffset * period)
#                 parsed_data.append((dt.datetime.fromtimestamp(float(cts)), float(cdata[1]), float(cdata[2]), float(cdata[3]), float(cdata[4]), float(cdata[5])))
#             except: pass
#     df = pd.DataFrame(parsed_data)
#     df.columns = ['ts', 'o', 'h', 'l', 'c', 'v']
#     df.index = df.ts
#     # del df['ts']
#     return df

# def get_timestamp(date):
#     return time.mktime(datetime.datetime.strptime(str(date),"%Y-%m-%d %H:%M:%S").timetuple())

# def get_day_transaction(data,ts,prev_trans):
#     print "day_start"
#     temp_prev_trans = prev_trans
#     start_val = data[0]
#     transactions = {"buy_qty":0,"sell_qty":0,"buy_val":0,"sell_val":0,"brokerage":0}
#     trans_perc,block_amount = 2.0,5000
#     for i in range(1,len(ts)):

#         if i == len(ts)-1:
#             if abs((data[i]-prev_trans)*100/prev_trans)<=2:
#                 print "<<<<<<<<<<<<<<<<<<<<<<<<< SQUARE OFF >>>>>>>>>>>>>>>>>>>>>>>>>>>"
#                 square = transactions["buy_qty"]-transactions["sell_qty"]
#                 if square>0:
#                     transactions["sell_qty"] += abs(square)
#                     transactions["sell_val"] += abs(square)*data[i]
#                     print  "SELL",abs(square),data[i]
#                 if square<0:
#                     transactions["buy_qty"] += abs(square)
#                     transactions["buy_val"] += abs(square)*data[i]
#                     print  "BUY",abs(square),data[i]                    
#                 transactions["brokerage"] = (transactions["buy_val"]+transactions["sell_val"])*0.0005
#             else:
#                 transactions["brokerage"] = (transactions["buy_val"]+transactions["sell_val"])*0.005

#         else:                    
#             incr = (data[i]-temp_prev_trans)*100/temp_prev_trans
#             if abs(incr) >= trans_perc:
#                 trans_perc = 0.25
#                 temp_prev_trans = data[i]
#                 if incr < 0:
#                     buy_qty = int(block_amount/data[i])
#                     transactions["buy_qty"] += buy_qty
#                     transactions["buy_val"] += buy_qty*data[i]
#                     print "BUY",buy_qty,data[i]

#                 if incr > 0:
#                     sell_qty = int(block_amount/data[i])
#                     transactions["sell_qty"] += sell_qty
#                     transactions["sell_val"] += sell_qty*data[i]
#                     print "SELL",sell_qty,data[i]

#     print "day_end"
#     print "TRANSACTION:",transactions
#     print ""
#     return temp_prev_trans,transactions

# def generate_array(comp,time,window):
#     spy = get_google_data(comp, time, window)
#     data = spy['o']
#     ts = spy['ts']
#     array = []
#     start_day = 0
#     for index,item in enumerate(ts):
#         day = str(item).split(" ")[0].split("-")[2]
#         if day != start_day:
#             array.append(index)
#             start_day = day
#     return array,data,ts

# data = get_google_data("SBIN",60,1)

# array,data,ts = generate_array("SBBJ",60,1)
# print array,data,ts
# prev_trans = 1
# all_transactions = {"buy_qty":0,"sell_qty":0,"buy_val":0,"sell_val":0,"brokerage":0}

# for index in range(len(array)-1):
#     prev_trans,day_trans = get_day_transaction(data[array[index]:array[index+1]],ts[array[index]:array[index+1]],prev_trans)
#     all_transactions["buy_qty"] += day_trans["buy_qty"]
#     all_transactions["sell_qty"] += day_trans["sell_qty"]
#     all_transactions["buy_val"] += day_trans["buy_val"]
#     all_transactions["sell_val"] += day_trans["sell_val"]
#     all_transactions["brokerage"] += day_trans["brokerage"]

# print "PROFIT:",all_transactions["sell_val"]-all_transactions["buy_val"]-all_transactions["brokerage"],"HOLDING:",all_transactions["buy_qty"]-all_transactions["sell_qty"]

# company = Share('SBIN.NS')
# pprint.pprint(company.get_historical('2015-07-01', '2016-02-05'))
# print company.get_open()
# print company.get_price()
# print company.get_trade_datetime()
# print company.refresh()
# print company.get_info()
# print company.get_volume()
# print company.get_prev_close()
# print company.get_avg_daily_volume()
# print company.get_stock_exchange()
# print company.get_market_cap()
# print company.get_book_value()
# print company.get_ebitda()
# print company.get_dividend_share()
# print company.get_dividend_yield()
# print company.get_earnings_share()
# print company.get_days_high()
# print company.get_days_low()
# print company.get_year_high()
# print company.get_year_low()
# print company.get_50day_moving_avg()
# print company.get_200day_moving_avg()
# print company.get_price_earnings_ratio()
# print company.get_price_earnings_growth_ratio()
# print company.get_price_sales()
# print company.get_price_book()
# print company.get_short_ratio()




# import MySQLdb
# from random import randint
# db=MySQLdb.connect(host="localhost",port=3306,user="root",passwd="290990",db="practice")
# cursor = db.cursor()
# cursor.execute(query)
# data = cursor.fetchall()
# db.commit()
# pprint.pprint(data)

# count = 0
# name = "sbin"
# while(count < 10):
#     timestamp = time.time()
#     quantity = 0
#     type = "buy"
#     price =randint(0,9)
#     print count,price
#     count += 1
#     if price >= 5:
#         query = 'insert into exp values('+str(timestamp)+',"'+name+'","'+type+'",'+str(quantity)+','+str(price)+')'
#         # print query
#         cursor.execute(query)
#         db.commit()
#     time.sleep(1)

def my_funct(symbol,time,day):
    url_root = 'http://www.google.com/finance/getprices?i='
    url_root += str(time) + '&p=' + str(day)
    url_root += 'd&f=d,o,h,l,c,v&df=cpct&q=' + symbol
    response = urllib2.urlopen(url_root)
    data = response.read().split('\n')
    data_time,data_open,data_high,data_low,data_close,data_volume,start_time,day_open = [],[],[],[],[],[],0,0
    # print data
    for item in range(7,len(data)-1):
        data_item = data[item].split(",")
        if 'a' in data_item[0]:
            start_time = int(data_item[0].replace('a', ''))
            data_time.append(datetime.datetime.fromtimestamp(int(start_time)))
            day_open = float(data_item[1])
        else:
            data_time.append(datetime.datetime.fromtimestamp(start_time+int(data_item[0])*60))
        data_open.append(float(data_item[1]))
        data_high.append(float(data_item[2]))
        data_low.append(float(data_item[3]))
        data_close.append(float(data_item[4]))
        data_volume.append(float(data_item[5]))
        day_close = float(data_item[4])
    # print len(data_open)
    day_high = max(data_high)
    day_low = max(data_low)
    day_volume = int(sum(data_volume))
    day_perc = 100*(day_close-day_open)/day_open
    fig = plt.figure()
    plt.plot(data_time,data_open)
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.title(symbol)
    plt.grid(True)
    plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
    # plt.show()
    fig.savefig(symbol+'.png')
    return day_open,day_close,day_high,day_low,day_volume,round(day_perc,2)

def share_mail(company_list):
    msg = '<html><body><table style="font-family:Segoe UI;border:1px solid black"><tr><td>NAME</td><td>OPEN</td><td>CLOSE</td><td>HIGH</td><td>LOW</td><td>VOLUME</td><td>PERC</td><tr>'
    for item in company_list:
        t1,t2,t3,t4,t5,t6 = my_funct(item,60,1)
        if t6 > 0 : col = "green"
        if t6 < 0 : col = "red"
        msg += '<tr><td>'+item+'</td><td>'+str(t1)+'</td><td>'+str(t2)+'</td><td>'+str(t3)+'</td><td>'+str(t4)+'</td><td>'+str(t5)+'</td><td style="color:'+col+'">'+str(t6)+'</td><tr>'
    msg += '</table></body></html>'
    return msg

fromaddr = 'souryapoddar290990@gmail.com'
toaddr = ["aryapoddar290990@gmail.com","souryapoddar290990@gmail.com"]
password = "souryaindia"
subject = "SHARE UPDATE"
company_list = ["BHEL","COALINDIA","POWERGRID","RPOWER","SBBJ","SBIN","TATASTEEL","VOLTAS"]
path = ''
filename = ''
body = share_mail(company_list)
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = ",".join(toaddr)
msg['Subject'] = subject
msg.attach(MIMEText(body, 'html'))
for item in company_list:
    filename = item+".png"
    attachment = open(path+filename, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr,password)
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()

# from pushbullet import Pushbullet
# API_KEY = 'o.nYHrQiyqBr2NTj59HaQFSSGsgoLDYQrv'
# # API_KEY = 'o.gmWPEjdjJvbZRqnTvCc7sHkonggCW48I'
# pb = Pushbullet(API_KEY)
# print pb.devices
# company_list = ["BHEL","COALINDIA","POWERGRID","RPOWER","SBBJ","SBIN","TATASTEEL","VOLTAS"]
# title = "Share"
# text = ""
# for item in company_list:
#     t1,t2,t3,t4,t5,t6 = my_funct(item,60,1)
#     text = item+' '+str(t1)+' '+str(t2)+' '+str(t3)+' '+str(t4)+' '+str(t6)+"\n"
#     push = pb.push_note(title,text)

