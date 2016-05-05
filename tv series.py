import os,sys,urllib2,json,pprint,omdb,requests,time,datetime,MySQLdb
import numpy as np
import datetime as dt
from subprocess import call
from bottle import route, run, template, request, redirect, static_file

month_name = {0:"", 1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}
master_username = "aryasourya"
master_password = "123456"

# db=MySQLdb.connect(host="sql6.freemysqlhosting.net",port=3306,user="sql6109617",passwd="VCDwEsfbel",db="sql6109617")
db=MySQLdb.connect(host="localhost",port=3306,user="root",passwd="290990",db="tv")
cursor = db.cursor()
# query = "SELECT * FROM information_schema.tables"
# query = "update t1 set pics='Y' where serial='Coupling'"
# query = "select serial,count(*) from t1 where pics='N' group by serial"
# query = "select season,serial,name,sub from t1 where serial like '%elementary%'"
# query = "SELECT * FROM sql6109617.t2"
# cursor.execute(query)
# data = cursor.fetchall()
# print len(data)

def insert_t2_data():
    db=MySQLdb.connect(host="localhost",port=3306,user="root",passwd="290990",db="tv")
    cursor = db.cursor()
    # query = "CREATE TABLE 't2' ('serial VARCHAR(200) NULL DEFAULT NULL','time INT(2) UNSIGNED ZEROFILL NULL DEFAULT NULL','status VARCHAR(15) NULL DEFAULT NULL','genre VARCHAR(15) NULL DEFAULT NULL','network VARCHAR(40) NULL DEFAULT NULL','theme VARCHAR(2000) NULL DEFAULT NULL','runtime FLOAT NULL DEFAULT NULL')"
    # query = 'INSERT INTO `t2` (`serial`, `time`, `status`, `genre`, `network`, `theme`, `runtime`) VALUES ("24", 60, "Ended", "Thriller", "FOX", "It is a thriller presented in \'real time\' with each minute of airtime that corresponds to a minute in the lives of the characters. \'24\' employs fast-paced and complex stories, and often contains unexpected plot twists. Though each day\'s events typically involve investigation of leads on terrorists, tracking suspects, and averting attacks, each season is made up of various interwoven story threads. The exact objective of the day evolves over the course of the season as the antagonists adapt, contingencies arise, and larger scale operations unfold.", 41)'
    # query = "TRUNCATE TABLE t2"
    query = "select * from t2 order by serial"
    cursor.execute(query)
    data = cursor.fetchall()
    for item in data:
        summary = item[5].replace('"',"'")
        output = '"'+item[0]+'",'+str(item[1])+',"'+item[2]+'","'+item[3]+'","'+item[4]+'","'+summary+'",'+str(int(item[6]))
        prefix = "INSERT INTO `t2` (`serial`, `time`, `status`, `genre`, `network`, `theme`, `runtime`) VALUES ("
        query = prefix+output+")"
        query = query.replace("'","\'")
        # print query
        db=MySQLdb.connect(host="sql6.freemysqlhosting.net",port=3306,user="sql6109617",passwd="VCDwEsfbel",db="sql6109617")
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()

def insert_t1_data():
    db=MySQLdb.connect(host="localhost",port=3306,user="root",passwd="290990",db="tv")
    cursor = db.cursor()
    # query = "CREATE TABLE `t1` (`serial` VARCHAR(200) NOT NULL DEFAULT '',`name` VARCHAR(200) NULL DEFAULT NULL,`season` INT(5) NOT NULL DEFAULT '0',`episode` INT(5) NOT NULL DEFAULT '0',`seena` ENUM('Yes','No') NULL DEFAULT NULL,`seens` ENUM('Yes','No') NULL DEFAULT NULL,`sub` ENUM('Yes','No','NA') NULL DEFAULT NULL,`day` INT(11) NULL DEFAULT NULL,`month` INT(15) NULL DEFAULT NULL,`year` INT(11) NULL DEFAULT NULL,`summary` VARCHAR(4000) NULL DEFAULT NULL,`pics` ENUM('Y','N') NULL DEFAULT NULL,`ppt` ENUM('Y','N') NULL DEFAULT NULL,PRIMARY KEY (`serial`, `season`, `episode`))COLLATE='latin1_swedish_ci'ENGINE=InnoDB"
    # query = "INSERT INTO `t1` ()"
    # query = "TRUNCATE TABLE t1"
    query = "select * from t1 order by serial,season,episode"
    cursor.execute(query)
    data = cursor.fetchall()
    db=MySQLdb.connect(host="sql6.freemysqlhosting.net",port=3306,user="sql6109617",passwd="VCDwEsfbel",db="sql6109617")
    cursor = db.cursor()
    for item in data:
        try:
            summary = item[10].replace('"',"'")
            output = '"'+item[0]+'","'+item[1]+'",'+str(item[2])+','+str(item[3])+',"'+item[4]+'","'+item[5]+'","'+item[6]+'",'+str(item[7])+','+str(item[8])+','+str(item[9])+',"'+item[10]+'","'+item[11]+'","'+item[12]
            prefix = "INSERT INTO `t1` (`serial`, `name`, `season`, `episode`, `seena`, `seens`, `sub`, `day`, `month`, `year`, `summary`, `pics`, `ppt`) VALUES ("
            query = prefix+output+'")'
            query = query.replace("'","\'")
            print item[0]
            cursor.execute(query)
            db.commit()
        except Exception,e : print e,item

@route('/<filename:re:.*\.js>')
def stylesheets(filename):
    return static_file(filename, root='static/js')

@route('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='static/css')

@route('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='static/img')

@route('/<filename:re:.*\.(mp4|mkv|lnk)>')
def videos(filename):
    return static_file(filename, root='static/vid')

def show_others():
    temp = datetime.datetime.fromtimestamp(time.time())
    day,month,year = temp.strftime("%d"),temp.strftime("%m"),temp.strftime("%Y")

    querya = "select count(t1.name),t2.runtime*count(t1.name) from t1,t2 where (t1.day+t1.month*30+t1.year*365)<=("+day+"+"+month+"*30+"+year+"*365)&&t1.seena='No'&&(t1.serial=t2.serial) group by t1.serial"
    cursor.execute(querya)
    adatas = cursor.fetchall()
    adata1,aepi,aday,ahr,amin = 0,0,0,0,0
    try:
        for adata in adatas:
            aepi += adata[0]
            adata1 += adata[1]

        aday += int(adata1/1440)
        ahr = int((adata1/60)%24)
        amin = int(adata1%60)
    except: aepi,aday,ahr,amin = 0,0,0,0

    querys = "select count(t1.name),t2.runtime*count(t1.name) from t1,t2 where (t1.day+t1.month*30+t1.year*365)<=("+day+"+"+month+"*30+"+year+"*365)&&t1.seens='No'&&(t1.serial=t2.serial) group by t1.serial"
    cursor.execute(querys)
    sdatas = cursor.fetchall()
    sdata1,sepi,sday,shr,smin = 0,0,0,0,0
    try:
        for sdata in sdatas:
            sepi += sdata[0]
            sdata1 += sdata[1]

        sday += int(sdata1/1440)
        shr = int((sdata1/60)%24)
        smin = int(sdata1%60)    
    except: sepi,sday,shr,smin = 0,0,0,0

    msg = '<table id="htab"><tr><td id="tv">&nbsp;</td><td id="shows">&nbsp</td></tr></table>'
    msg += '<div id="stat"><table id="stat"><tr><td id="td16">viewers</td><td id="td15">episodes</td><td id="td15">days</td><td id="td15">hours</td><td id="td15">minutes</td></tr><tr><td id="td11">Arya</td><td id="td18">'+str(aepi)+'</td><td id="td12">'+str(aday)+'<td id="td12">'+str(ahr)+'<td id="td12">'+str(amin)+'</td></tr><tr><td id="td13">Sourya</td><td id="td14">'+str(sepi)+'</td><td id="td14">'+str(sday)+'<td id="td14">'+str(shr)+'<td id="td14">'+str(smin)+'</td></tr></table></div>'
    msg += '<div id="extra1"><a href="/left/na/na" id="ue"><img src="uwe.png"></a></div><div id="extra2"><a href="" id="ue"><img src="uce.png"></a></div>'
    return msg

def get_serial_list():
    query = "select * from t2 order by serial"
    cursor.execute(query)
    data = cursor.fetchall()
    print "data",data
    count,msg = 0,""
    for index,item in enumerate(data):
        if int(index/6) == count:
            msg += '<div id="sertab'+str(count+1)+'"><table id="tabser">'
            count += 1
        msg += '<tr><td><a href="/serial/'+item[0]+'"><img src="'+item[0]+'/3.jpg"></a></td></tr><tr><td id="hblnkr"></td></tr>'
        if int((index+1)/6) == count:
            msg += '</table></div>'
    print msg
    return msg

def check_login(username, password):
    if (username == master_username) and (password == master_password):
        return 1

@route('/login')
def login():
    return '<form action="/login" method="post">Username: <input name="username" type="text" />Password: <input name="password" type="password" />            <input value="Login" type="submit" />        </form>'
        
@route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        # return "<p>Your login information was correct.</p>"
        return redirect('/show')
    else:
        return "<p>Login failed.</p>"

@route('/show')
def main():
    msg = '<html><head><link rel="stylesheet" href="style.css" type="text/css" ><link rel="shortcut icon" type="image/x-icon" href="logo_tv.png" /><title>Shows</title></head><body id="shows">'+show_others()+get_serial_list()+'<body><html>'
    return msg

@route('/serial/<name>')
def serial(name):
    query = "select * from t2 where serial='"+name+"'"
    cursor.execute(query)
    data = cursor.fetchone()
    serial,runtime,status,genre,network,theme = data[0],str(data[1]),data[2],data[3],data[4],data[5]
    
    query = "select season from t1 where serial='"+name+"' group by season order by season desc"
    cursor.execute(query)
    seasons = cursor.fetchone()[0]
    
    query="select day,month,year from t1 where serial='"+name+"' limit 0,1";
    cursor.execute(query)
    date = cursor.fetchone()
    day,month,year = date[0],date[1],date[2]
    if day == 0: release_date = "N/A"
    if day>0 and day<10: day="0"+str(day)
    release_date = str(day)+" "+month_name[month]+" "+str(year)
    
    temp = datetime.datetime.fromtimestamp(time.time())
    day,month,year = temp.strftime("%d"),temp.strftime("%m"),temp.strftime("%Y")
    query="select count(*) from t1 where (day+month*30+year*365)<=("+day+"+"+month+"*30+"+year+"*365)&&serial='"+name+"'";
    cursor.execute(query)
    episodes = str(cursor.fetchone()[0])

    msg = '<html><head><title>Serial</title><link rel="stylesheet" href="../style.css" type="text/css" ><link href="../jquery.mCustomScrollbar.css" rel="stylesheet" /><script src="../jquery.min.js"></script><script src="../jquery.mCustomScrollbar.concat.min.js"></script><script src="../serial_2_scroll.js"></script></head><body background="../'+name+'/1.jpg" style="background-size:1366px 768px;background-attachment:fixed;background-repeat:no-repeat;"><table id="stab"><tr><td><a href="/show"><img src="../wback.png" width="44" height="44" onMouseOver=src="../wwback.png" onMouseOut=src="../wback.png" onMouseDown=src="../bbback.png"></a></td><td id="td0">'+name+'</td></tr></table><div style="width:374px;height:550px;margin-top:40px;margin-left:65px;border:1px white solid;"><img src="../'+name+'/2.jpg"></div>'
    msg += '<div id="serial1"><table id="tab10"><tr><td id="td25">Information</td><td></td></tr><tr><td></td></tr><tr><td id="td24">Status:</td><td id="td26">'+status+'</td></tr><tr><td id="td24">Genre:</td><td id="td26">'+genre+'</td></tr><tr><td id="td24">Network:</td><td id="td26">'+network+'</td></tr><tr><td id="td24">Runtime:</td><td id="td26">'+runtime+' mins</td></tr><tr><td id="td24">Seasons:</td><td id="td26">'+str(seasons)+'</td></tr><tr><td id="td24">Episodes:</td><td id="td26">'+episodes+'</td></tr><tr><td id="td24">Started:</td><td id="td26">'+release_date+'</td></tr></table><table id="tab10"><tr><td></td><td></td></tr><tr><td id="td23">Theme</td><td></td></tr><tr><td id="td22">'+theme+'</td></tr></table></div>'
    msg += '<div id="serial2"><table id="tab11">'
    for season in range(seasons):
        if season<9: pre_season="0"+str(season+1)
        else: pre_season = str(season+1)
        msg += '<tr><td id="td20"><a href="/season/'+name+'/'+str(season+1)+'/'+'1"">Season <span>'+pre_season+'</span></a></td></tr><tr><td id="td21"></td></tr>'
    msg += '</table></div>'
    return msg

@route('/season/<name>/<season>/<episode>')
def season(name,season,episode):
    msg = '<html><head><title>Season</title><link rel="stylesheet" href="../../../style.css" type="text/css" ><link href="../../../jquery.mCustomScrollbar.css" rel="stylesheet" /><script src="../../../jquery.min.js"></script><script src="../../../jquery.mCustomScrollbar.concat.min.js"></script><script src="../../../ssn_scroll.js"></script></head>'
    msg += '<body background="../../../'+name+'/1.jpg" style="background-size:1366px 768px;background-attachment:fixed;background-repeat:no-repeat;"><table id="stab"><tr><td><a href="/serial/'+name+'"><img src="../../../wback.png" width="44" height="44" onMouseOver=src="../../../wwback.png" onMouseOut=src="../../../wback.png" onMouseDown=src="../../../bbback.png"></a></td><td id="td0">'+name+'</td><td id="td">Season '+str(season)+'</td></tr></table>'
    msg += '<div id="ssn">'
    query = "select name,episode,day,month,year from t1 where serial='"+name+"' and season="+str(season)
    cursor.execute(query)
    data = cursor.fetchall()
    for item in data:
        episode_name,episode_num,day,month,year = item[0],item[1],item[2],item[3],item[4]
        if day==0: day,month,year = "","",""
        else:
            if day<10: day="0"+str(day)
            month=month_name[month]

        if episode_num<10: episode_nums = "0"+str(episode_num)
        else: episode_nums = str(episode_num)

        msg += '<a href="/season/'+name+'/'+str(season)+'/'+str(episode_num)+'"><table background="../../../'+name+'/'+str(season)+'/'+str(episode_nums)+'.png" style="border-collapse:collapse; background-size:312px 176px;"><tr><td id="td6"></td></tr><tr><td id="td7">'+episode_nums+' - '+episode_name+'</td></tr><tr><td id="td8">'+str(day)+' '+month+' '+str(year)+'</td></tr></table></a><table><tr><td id="td9"></td></tr></table>'
    msg += '</div>'

    query = "select name,seena,seens,sub,day,month,year,summary from t1 where serial='"+name+"' and season='"+str(season)+"' and episode='"+str(episode)+"'";
    cursor.execute(query)
    data = cursor.fetchone()
    epi_name,epi_seena,epi_seens,epi_sub,epi_day,epi_month,epi_year,epi_summary = data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]
    if epi_day == 0: epi_day,epi_month,epi_year = "","",""
    else:
        if epi_day<10: epi_day="0"+str(epi_day)
        epi_month=month_name[epi_month]

    if int(episode)<10: episode_nums = "0"+str(episode)
    else: episode_nums = str(episode)

    msg += '<div id="content"><table id="etab"><tr><td colspan="3" id="td1">'+epi_name+'</td></tr>'
    msg += '<tr><td rowspan="6" id="td10"><a href="../../../'+name+'/'+str(season)+'/'+episode_nums+' - '+epi_name+' - Shortcut.lnk" download><img src="../../../'+name+'/'+str(season)+'/'+str(episode_nums)+'.png"><span id="download">Click to download</span></a></td>'
    msg += '<td id="td2">Aired On:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td><td id="td3" colspan="2">'+str(epi_day)+' '+month+' '+str(year)+'</td></tr><tr><td id="td2">Season:</td><td id="td3">'+str(season)+'</td></tr><tr><td id="td2">Episode:</td><td id="td3">'+str(episode)+'</td></tr>'
    msg += '<tr><td id="td2">Arya:</td><td id="td3">'+epi_seena+'</td><td><a href="../../../bypass/'+name+'/'+str(season)+'/'+str(episode)+'/seena/'+epi_seena+'"><img src="../../../'+epi_seena.lower()+'.png"></a></td></tr>'
    msg += '<tr><td id="td2">Sourya:</td><td id="td3">'+epi_seens+'</td><td><a href="../../../bypass/'+name+'/'+str(season)+'/'+str(episode)+'/seens/'+epi_seens+'"><img src="../../../'+epi_seens.lower()+'.png"></a></td></tr>'    
    msg += '<tr><td id="td2">Subtitle:</td><td id="td3">'+epi_sub+'</td><td><a href="../../../bypass/'+name+'/'+str(season)+'/'+str(episode)+'/sub/'+epi_sub+'"><img src="../../../'+epi_sub.lower()+'.png"></a></td></tr>'
    msg += '</table><table><tr><td id="td4">Summary</td></tr><tr><td id="td5">'+epi_summary+'</td></tr></table></div>'

    msg += '</body></html>'
    return msg

@route('/bypass/<name>/<season>/<episode>/<types>/<val>')
def change_flag(name,season,episode,types,val):
    if val == "Yes": val_rev = "No"
    if val == "No": val_rev = "Yes"
    query = 'update t1 set '+types+'="'+val_rev+'" where serial="'+name+'" and season="'+str(season)+'" and episode="'+str(episode)+'"';
    cursor.execute(query)
    db.commit()
    return redirect('/season/'+name+'/'+str(season)+'/'+str(episode))

@route('/setseen/<name>/<season>/<episode>/<types>')
def set_seen(name,season,episode,types):
    query = 'update t1 set '+types+'="Yes" where serial="'+name+'" and season="'+str(season)+'" and episode="'+str(episode)+'"';
    cursor.execute(query)
    db.commit()
    return redirect('../../../../left/'+name+'/'+types)

@route('/left/<name>/<user>')
def left(name,user):
    msg = '<html><head><title>Left</title><link rel="stylesheet" href="../../../style.css" type="text/css" ><link href="../../../jquery.mCustomScrollbar.css" rel="stylesheet" /><script src="../../../jquery.min.js"></script><script src="../../../jquery.mCustomScrollbar.concat.min.js"></script><script src="../../../left_scroll.js"></script></head><body id="left">'
    temp = datetime.datetime.fromtimestamp(time.time())
    day,month,year = temp.strftime("%d"),temp.strftime("%m"),temp.strftime("%Y")
    query = "select serial,count(*) from t1 where (day+month*30+year*365)<=("+day+"+"+month+"*30+"+year+"*365) and seena='No' group by serial"
    cursor.execute(query)
    datas = cursor.fetchall()

    msg += '<table id="stab"><tr><td><a href="/show"><img src="../../../bback.png" width="44" height="44" onMouseOver=src="../../../wbbback.png" onMouseOut=src="../../../bback.png" onMouseDown=src="../../../bbback.png"></a></td><td id="tv">Unwatched</td><td id="shows">Episodes</td></tr></table><div id="serltab1"><table id="tabser"><tr><td>Arya</td></tr><tr><td id="blank"></td></tr></table><div id="leftarya">'
    for data in datas:
        msg += '<a href="../../left/'+str(data[0])+'/seena"><table id="left"><tr id="left"><td id="td27"><img src="../../../'+str(data[0])+'/3.jpg" height="56" width="304"></td><td id="td28">'+str(data[1])+'</td></tr></table></a>'
    msg += '</div></div>'
    
    query = "select serial,count(*) from t1 where (day+month*30+year*365)<=("+day+"+"+month+"*30+"+year+"*365) and seens='No' group by serial"
    cursor.execute(query)
    datas = cursor.fetchall()

    msg += '<div id="serltab2"><table id="tabser"><tr><td>Sourya</td></tr><tr><td id="blank"></td></tr></table><div id="leftsourya">'
    for data in datas:
        msg += '<a href="../../left/'+str(data[0])+'/seens"><table id="left"><tr id="left"><td id="td29">'+str(data[1])+'</td><td id="td27"><img src="../../../'+str(data[0])+'/3.jpg" height="56" width="304"></td></tr></table></a>'

    msg += '</div></div>'

    if name == 'na': return msg+'</body></html>'

    msg += '<div id="contentleft"><table style="border-collapse:collapse;">'
    query = "select name,season,episode from t1 where (day+month*30+year*365)<=("+day+"+"+month+"*30+"+year+"*365) and serial='"+name+"'&&"+user+"='No'";
    cursor.execute(query)
    datas = cursor.fetchall()
    for data in datas:
        if data[2]<10: epis = "0"+str(data[2])
        else: epis = str(data[2])
        msg += '<tr style="font-family:Segoe UI Light"><td style="padding:0px 10px 0px 20px;"><a href="../../../season/'+name+'/'+str(data[1])+'/'+str(data[2])+'" style="text-decoration:none;color:#008dd5;">'+data[0]+'</a></td><td style="color:#d6ac30;">'+str(data[1])+'<span style="color:#008ddf;">-</span><span style="color:black;">'+epis+'</span></td><td style="padding-left:15px;"><a href="../../../setseen/'+name+'/'+str(data[1])+'/'+str(data[2])+'/'+user+'"><img src="../../../no.png"></td></a></tr>'
    msg += '</table></div></body></html>'

    return msg

@route('/tasks')
def taskmanager():
    task_type = ['None','Download','Convert','Subtitle','Watch','Dataentry','Sound','Seagate','WD','Tele','Mega','Drive']
    task_assigned = ['None','Arya','Sourya']

    msg = '<html><script type="text/javascript" src="https://code.jquery.com/jquery-latest.min.js"></script><script src="jquery.datetimepicker.js"></script><script src="date.js"></script><script src="https://code.jquery.com/jquery-1.10.2.js"></script><script src="https://code.jquery.com/ui/1.11.4/jquery-ui.js"></script><link rel="stylesheet" type="text/css" href="jquery.datetimepicker.css"><link rel="stylesheet" href="https://code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css"><body>'
    msg += '<h3>INCOMPLETE TASK</h3>'
    msg += '<form method="post" action="http://localhost:8080/tasks"><table><tr>'
    msg += '<td>Description&nbsp;<input id="title" name="title"></td>'
    msg += '<td>Type&nbsp;<select name="type" id="type">'
    for item in task_type: msg += '<option value="'+item+'">'+item+'</option>'
    msg += '</select></td>'

    msg += '<td>Asignee&nbsp;<select name="assigned" id="assigned">'
    for item in task_assigned: msg += '<option value="'+item+'">'+item+'</option>'
    msg += '</select></td>'
    msg += '<td>Date&nbsp;<input id="datepicker" name="datepicker"></td>'
    # msg += '<td><p id="submit">Submit</p></td>'
    msg += '<td><input type="submit"/></td>'
    msg += '</tr></table></form>'
    query1 = 'select * from taskmanager where status="Pending"'
    cursor.execute(query1)
    data1 = cursor.fetchall()
    # print data
    msg += '<table>'
    msg += '<tr><td>Created</td><td>Title</td><td>Type</td><td>Date</td><td>Assigned</td><td>Status</td></tr>'
    for item in data1:
        msg += '<tr><td>'+str(item[0])+'</td><td>'+item[3]+"</td><td>"+item[1]+'</td><td>'+str(item[5])+'/'+str(item[6])+'/'+str(item[7])+'</td><td>'+item[4]+'</td><td><a href="/update_task/1/'+str(item[0])+'">done</a></td></tr>'
    msg += '</table>'
    msg += '<h3>COMPLETED TASK</h3>'
    query2 = 'select * from taskmanager where status="Finished"'
    cursor.execute(query2)
    data2 = cursor.fetchall()
    # print data
    msg += '<table>'
    msg += '<tr><td>Finished</td><td>Title</td><td>Type</td><td>Date</td><td>Assigned</td><td>Status</td></tr>'
    for item in data2:
        msg += '<tr><td>'+str(item[8])+'</td><td>'+item[3]+"</td><td>"+item[1]+'</td><td>'+str(item[5])+'/'+str(item[6])+'/'+str(item[7])+'</td><td>'+item[4]+'</td><td><a href="/update_task/2/'+str(item[0])+'">delete</a></td></tr>'
    msg += '</table>'    
    msg += '</body></html>'
    
    return msg

@route('/update_task/<types>/<timestamp>')
def update_task(types,timestamp):
    if types == "1": query = 'update taskmanager set status="Finished",finished_timestamp=now() where create_timestamp="'+timestamp+'"'
    if types == "2": query = 'delete from taskmanager where create_timestamp="'+timestamp+'"' 
    cursor.execute(query)
    db.commit()    
    return redirect('/tasks')

@route('/tasks', method='POST')
def get_task_details():
    entry_title = request.forms.get('title')
    entry_type = request.forms.get('type')
    entry_assigned = request.forms.get('assigned')
    entry_date = request.forms.get('datepicker').split("/")
    # print entry_title,entry_type,entry_status,entry_assigned,entry_date[1],entry_date[0],entry_date[2]
    query = 'insert into taskmanager values(now(),"'+entry_type+'","Pending","'+entry_title+'","'+entry_assigned+'",'+entry_date[1]+','+entry_date[0]+','+entry_date[2]+',"")'
    print query
    cursor.execute(query)
    db.commit()
    return redirect('/tasks')

run(host='localhost', port=8080)

def null_input(var):
   if var == "":
       var = "is not null"
   else: var = "='"+var+"'"
   return var

def filter_list(genre,series_status,network,runtime):
   genre = null_input(genre)
   series_status = null_input(series_status)
   network = null_input(network)
   runtime = null_input(runtime)
   query = "select serial,genre,status,network,runtime,run from (select *,case when runtime<=0 then 'less30' when runtime between 31 and 60 then 'bet31-60' else 'grt60' end as run from t2) as a where a.genre "+genre+" and a.status "+series_status+" and a.network "+network+" and a.run "+runtime+""
   cursor.execute(query)
   data = cursor.fetchall()
   print data
   return data

