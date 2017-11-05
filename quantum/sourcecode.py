import sys, os, json, pprint, yaml, bson, math, operator, MySQLdb
import pandas as pd
from collections import Counter, OrderedDict

def create_db_connection():
	db=MySQLdb.connect(host="localhost",port=3306,user="root",passwd="290990",db="sourya_practice")
	cursor = db.cursor()
	return db, cursor

db, cursor = create_db_connection()

def create_table(db, cursor):
	query = "CREATE TABLE `post_box` (`post_id` INT(11) NOT NULL,`name` VARCHAR(100) NULL DEFAULT NULL,`loc_x` FLOAT NULL DEFAULT NULL,`loc_y` FLOAT NULL DEFAULT NULL, PRIMARY KEY (`post_id`))"
	cursor.execute(query)
	db.commit()

create_table(db, cursor)

def insert_rows(db, cursor):
	f = open('POBoxes.txt')
	data = []
	for line in f:
	    data.append(json.loads(line))
	items = data[0]['items']
	for index in range(len(items)):
		pid = items[index]['id']
		name = items[index]['name']
		loc_x = items[index]['loc_x']
		loc_y = items[index]['loc_y']
		# print pid, name, loc_x, loc_y, '\n'
		query = 'insert into post_box values("'+pid+'","'+name+'","'+str(loc_x)+'","'+str(loc_y)+'")'
		# print query
		cursor.execute(query)
	db.commit()

insert_rows(db, cursor)

def solve_1(cursor):
	query = "select post_id, name from post_box where post_id not in (select aid from (SELECT a.post_id as aid, b.post_id as bid,111.1111 * DEGREES(ACOS(COS(RADIANS(a.loc_x)) * COS(RADIANS(b.loc_x)) * COS(RADIANS(a.loc_y - b.loc_y)) + SIN(RADIANS(a.loc_x))   * SIN(RADIANS(b.loc_x)))) AS distance_in_km FROM post_box AS a JOIN post_box AS b ON a.post_id <> b.post_id) as temp_table where distance_in_km <= 0.5 group by aid)"
	cursor.execute(query)
	solution_1 = cursor.fetchall()
	# print solution_1
	solution_1_id = [int(item[0]) for item in solution_1]
	solution_1_name = [item[1].rstrip() for item in solution_1]
	print "PROBLEM 1: POSTBOXES HAVING NO OTHER POSTBOX WITHIN 500m DISTANCE\n",solution_1,"\n"

solve_1(cursor)

def solve_2(cursor):
	query = "select * from (SELECT aid,lat1,lat2,lon1,lon2,count(*) as counts from (SELECT a.post_id AS aid, b.post_id AS bid,a.loc_x as alat,a.loc_y as alon,b.loc_x as blat,b.loc_y as blon,a.loc_y-1/ ABS(COS(RADIANS(a.loc_x))*111.1111) AS lon1,a.loc_y+1/ ABS(COS(RADIANS(a.loc_x))*111.1111) AS lon2,a.loc_x-(1/111.1111) AS lat1, a.loc_x+(1/111.1111) AS lat2 FROM post_box AS a JOIN post_box AS b ON a.post_id <> b.post_id) AS temp_table where blon between lon1 and lon2 and blat between lat1 and lat2 group by aid) as temp1 where counts = (select MAX(counts) from (SELECT aid,lat1,lat2,lon1,lon2,count(*) as counts from (SELECT a.post_id AS aid, b.post_id AS bid,a.loc_x as alat,a.loc_y as alon,b.loc_x as blat,b.loc_y as blon,a.loc_y-1/ ABS(COS(RADIANS(a.loc_x))*111.1111) AS lon1,a.loc_y+1/ ABS(COS(RADIANS(a.loc_x))*111.1111) AS lon2,a.loc_x-(1/111.1111) AS lat1, a.loc_x+(1/111.1111) AS lat2 FROM post_box AS a JOIN post_box AS b ON a.post_id <> b.post_id) AS temp_table where blon between lon1 and lon2 and blat between lat1 and lat2 group by aid) as max_table_2)"
	cursor.execute(query)
	solution_2 = cursor.fetchall()
	print "PROBLEM 2: REGION HAVING MOST NUMBER OF POSTBOXES"
	for areas in solution_2:
		print "LAT : ",areas[1]," and ",areas[2]
		print "LON : ",areas[3]," and ",areas[4]
		print "COUNT : ",areas[5]

solve_2(cursor)

def solve_3(cursor):
	query = "SELECT maxname,counts FROM ( SELECT SUBSTRING_INDEX(name,' ',1) AS maxname, COUNT(*) AS counts FROM post_box GROUP BY 1) AS selCount WHERE counts = ( SELECT MAX(COUNT) FROM ( SELECT SUBSTRING_INDEX(name,' ',1) AS maxname, COUNT(*) AS COUNT FROM post_box GROUP BY 1) AS selectMax)"
	# query = "SELECT MAX(COUNT) FROM (SELECT SUBSTRING_INDEX(name,' ',1) AS maxname, COUNT(*) AS COUNT FROM post_box GROUP BY 1) AS selectMax"
	cursor.execute(query)
	solution_3 = cursor.fetchall()
	print "\nPROBLEM 3: FIRST LETTER OF POSTBOX NAME HAVING MOST OCCURENCE"
	for names in solution_3:
		print "NAME START WITH '"+names[0]+"' AND COUNT IS "+str(names[1])+"\n"

solve_3(cursor)
