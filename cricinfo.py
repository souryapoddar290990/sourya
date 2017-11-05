import sys, os, json, pprint, yaml, bson, math, operator
import pandas as pd
from collections import Counter, OrderedDict

def preprocess(filename):
	file = open(filename,'r')
	temp = file.read()
	data = yaml.load(temp)
	info = data['info']
	city = info['city']
	competition = info['competition']
	venue = info['venue']
	gender = info['gender']
	match_type = info['match_type']
	overs = info['overs']
	winner = info['outcome']['winner']
	by_param = info['outcome']['by'].keys()[0]
	by_val = info['outcome']['by'][by_param]
	player_of_match = info['player_of_match'][0]
	team_1 = info['teams'][0]
	team_2 = info['teams'][1]
	toss_winner = info['toss']['winner']
	toss_decision = info['toss']['decision']
	umpires_1 = info['umpires'][0]
	umpires_2 = info['umpires'][1]
	print team_1,'vs',team_2,',',venue,',',city
	print toss_winner,'won the toss and elected to',toss_decision
	print winner,'won the match by',by_val,by_param
	print 'Man of the Match is',player_of_match
	return data,team_1,team_2,winner

def get_ball_by_ball_details(data,innings_num):
	if innings_num == 1: innings_deliveries = data['innings'][innings_num-1]['1st innings']['deliveries']
	if innings_num == 2: innings_deliveries = data['innings'][innings_num-1]['2nd innings']['deliveries']
	final = []
	for ball in range(len(innings_deliveries)):
		temp = innings_deliveries[ball]
		ball_num = temp.keys()[0]
		batsman = temp[ball_num]['batsman']
		bowler = temp[ball_num]['bowler']
		non_striker = temp[ball_num]['non_striker']
		extras_type = 'NA'
		extras_val = 0
		wicket_kind = 'NA'
		wicket_player = 'NA'
		wicket_fielder_1 = 'NA'
		wicket_fielder_2 = 'NA'
		
		if 'extras' in temp[ball_num].keys():
			extras_type = temp[ball_num]['extras'].keys()[0]
			extras_val = temp[ball_num]['extras'][extras_type]

		runs_batsman = temp[ball_num]['runs']['batsman']
		runs_extra = temp[ball_num]['runs']['extras']
		runs_total = temp[ball_num]['runs']['total']

		if 'wicket' in temp[ball_num].keys():
			wicket_kind = temp[ball_num]['wicket']['kind']
			wicket_player = temp[ball_num]['wicket']['player_out']
			if 'fielders' in temp[ball_num]['wicket'].keys():
				wicket_fielder_1 = temp[ball_num]['wicket']['fielders'][0]
				if len(temp[ball_num]['wicket']['fielders']) == 2: 
					wicket_fielder_2 = temp[ball_num]['wicket']['fielders'][1]

		final.append([innings_num, ball_num, batsman, bowler, non_striker, extras_type, extras_val, wicket_kind, wicket_player, wicket_fielder_1, wicket_fielder_2, runs_batsman, runs_extra, runs_total])

	return final

def generate_scorecard(data,innings_details,innings_num):
	if innings_num == 1: innings_team = data['innings'][innings_num-1]['1st innings']['team']
	if innings_num == 2: innings_team = data['innings'][innings_num-1]['2nd innings']['team']
	print '----------------------------------------------------'
	print innings_team,'\n----------------------------------------------------'
	batsman_details = {}
	batsman_name = []
	batsman_wicket = {}
	bowler_details = {}
	bowler_name = []
	bowler_order = []
	extra_list = {'legbyes':0,'wides':0,'byes':0,'noballs':0,'penalty':0}
	extras = 0
	total_runs = 0
	total_wickets = 0
	total_balls = len(innings_details)
	maiden_overs = [-6]*20
	bowler_overs = ['']*20

	for balls in innings_details:
		# print balls
		if balls[13] == 0: maiden_overs[int(math.floor(balls[1]))] += 1
		if int(math.floor((balls[1]*10)%10)) == 1:
			bowler_overs[int(math.floor(balls[1]))] = balls[3]
		if balls[2] in batsman_details:
			batsman_details[balls[2]].append(balls[11])
		else:
			batsman_details[balls[2]] = [balls[11]]
			batsman_wicket[balls[2]] = ''
			batsman_name.append(balls[2])
		if balls[4] not in batsman_details:
			batsman_details[balls[4]] = []
			batsman_name.append(balls[4])
			batsman_wicket[balls[4]] = ''
		if balls[3] in bowler_details:
			bowler_details[balls[3]].append(balls[13])
		else:
			bowler_details[balls[3]] = [balls[13]]
			bowler_name.append(balls[3])
		if balls[7] != 'NA':
			total_wickets += 1
			if balls[7] not in  ['run out', 'hit wicket', 'retired hurt']:
				bowler_details[balls[3]].append(-1)
			batsman_details[balls[8]].append(-1)
			text = balls[7]
			if balls[7] in ['hit wicket', 'retired hurt']:
				pass
			if balls[7] in ['bowled', 'lbw', 'caught and bowled']:
				if balls[3] != 'NA': text += ' '+balls[3]
			if balls[7] in ['caught', 'stumped']:
				if balls[9] != 'NA': text += ' '+balls[9]
				if balls[10] != 'NA': text += ' '+balls[10]
				if balls[3] != 'NA': text += ' bowled '+balls[3]
			if balls[7] == 'run out':
				if balls[9] != 'NA': text += ' '+balls[9]
				if balls[10] != 'NA': text += '/'+balls[10]
			batsman_wicket[balls[8]] = text

		if balls[5] != 'NA':
			if balls[5] in ['wides','noballs']:
				total_balls -= 1
				maiden_overs[int(math.floor(balls[1]))] += 10
				bowler_details[balls[3]].append(-2)
			extra_list[balls[5]] += balls[6]
		extras += balls[12]
		total_runs += balls[13]

	for name in batsman_name:
		status = 'not out'
		if len(batsman_details[name]) == 0:
			runs = 0
			balls = 0
			fours = 0
			sixes = 0
			strike_rate = 0.0
		else:
			if batsman_details[name] == [-1]:
				runs = 0
				balls = 0
				fours = 0
				sixes = 0
				strike_rate = 0.0				
				status = batsman_wicket[name]
			else:
				if batsman_details[name][-1] == -1:
					runs = sum(batsman_details[name][:-1])
					balls = len(batsman_details[name][:-1])
					status = batsman_wicket[name]
				else:
					runs = sum(batsman_details[name])
					balls = len(batsman_details[name])
				fours = Counter(batsman_details[name])[4]
				sixes = Counter(batsman_details[name])[6]
				strike_rate = round(runs*100.0/balls,2)
		print name, status, str(runs)+'('+str(balls)+')', fours, sixes, strike_rate
	
	print '\nB',extra_list['byes'],'LB',extra_list['legbyes'],'W',extra_list['wides'],'NB',extra_list['noballs'],'PEN',extra_list['penalty'],'EXTRAS',extras,'\n'
	print 'TOTAL',str(total_runs)+'/'+str(total_wickets)+'('+str(total_balls/6)+'.'+str(total_balls%6)+')','\n'
	
	maiden_bowlers = [bowler_overs[ind] for ind,item in enumerate(maiden_overs) if item == 0]
	for name in bowler_name:
		wickets = Counter(bowler_details[name])[-1]
		extra_ball = Counter(bowler_details[name])[-2]
		balls = len(bowler_details[name])-wickets-2*extra_ball
		maidens = Counter(maiden_bowlers)[name]
		overs = str(balls/6)+'.'+str(balls%6)
		ball_runs = [item for item in bowler_details[name] if item >= 0]
		print name, overs, str(maidens), str(sum(ball_runs)), str(wickets), round(sum(ball_runs)*6.0/balls,2)

def match_details(filename):
	data,team_1,team_2,winner = preprocess(filename)
	innings_details = get_ball_by_ball_details(data,1)
	generate_scorecard(data,innings_details,1)
	innings_details = get_ball_by_ball_details(data,2)
	generate_scorecard(data,innings_details,2)

def points_table():
	teams, winners = [], []
	for ii,index in enumerate(range(335982,336038)):
		filename = 'ipl/'+str(index)+'.yaml'
		try:
			data,team_1,team_2,winner = preprocess(filename)
			match_details(filename)
			teams.append(team_1)
			teams.append(team_2)
			winners.append(winner)
		except Exception, e:
			print e, ii+1

	matches = Counter(teams)
	wins = Counter(winners)
	team_points = {}
	for team in matches:
		team_points[team] = wins[team]*2+14-matches[team]

	ranking = sorted(team_points.items(), key=operator.itemgetter(1), reverse=True)

	print 'POINTS TABLE\n'
	for team in ranking:
		match = matches[team[0]]
		won = wins[team[0]]
		nr = 14-match
		lost = match-won
		print team[0],14,won,nr,lost,team[1]
	print '\n'

# filename = 'ipl/335982.yaml'
# match_details(filename)
# points_table()
