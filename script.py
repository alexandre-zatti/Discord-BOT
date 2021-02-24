import db as database
import roleml
import json
from riotwatcher import LolWatcher, ApiError


riotApi = LolWatcher('RGAPI-8f7ea0b8-ddd7-4bf4-938a-87240a81361d')

region = 'br1'

def get_accs_data():
    res = database.get_acc_names()
    players_matches = {}

    for r in res:
        acc_info = riotApi.summoner.by_name(region,r[0])
        players_matches[acc_info['name']] = riotApi.match.matchlist_by_account(region,acc_info['accountId'],'','','','',20)['matches']

    return players_matches


def get_accs_matches_info(players_matches):
    
    match_dto = {}
    
    for player in players_matches:
        match_dto[player] = []
        count = 0
        for match in players_matches[player]:
            match_info = riotApi.match.by_id(region,match['gameId'])
            if(filter_matches(match_info)):
                match_timeline = riotApi.match.timeline_by_match(region,match['gameId'])
                match_champ_id = match['champion']
                predict_positions = roleml.predict(match_info,match_timeline)
                participant = match_info_procesing(match_info, match_champ_id)
                participant['position'] = predict_positions[participant['participantId']]
                match_dto[player].append(participant)
                count+=1
            else:
                continue
        match_dto[player].append(count)
        
    return match_dto


def filter_matches(match):
    if match["gameMode"] == "CLASSIC" and match["gameType"] == "MATCHED_GAME":
        return True
    else:
        return False


def match_info_procesing(match_info, match_champ_id):
    for participant in match_info['participants']:
        if participant['championId'] == match_champ_id:
            return participant

def point_processing(match_dto):
    players_points = {}

    for player in match_dto:
        players_points[player] = 0
        for match in match_dto[player]:
            if isinstance(match, int):
                continue
            else:
                points = statistic_calculation(match)
                players_points[player]+= points

        if match_dto[player][-1] != 0:
            players_points[player] = round(players_points[player]/match_dto[player][-1])
    
    return players_points

def statistic_calculation(match):
       
    points = 0
    multipliers = {}
    
    if match['position'] == 'top':
        
        multipliers = {
            'totalDamageDealtToChampions' : 3,
            'damageDealtToTurrets' : 5,
            'damageDealtToObjectives' : 3,
            'totalHeal' : 3,
            'totalDamageTaken' : 2,
            'goldEarned' : 4,
            'visionScore' : 3,
            'visionWardsBoughtInGame' : 5,
            'totalMinionsKilled' : 5,
            'neutralMinionsKilled' : 1,
            'kills' : 3,
            'deaths' : 2,
            'assists' : 3,
        }

    elif match['position'] == 'mid':

         multipliers = {
            'totalDamageDealtToChampions' : 4,
            'damageDealtToTurrets' : 4,
            'damageDealtToObjectives' : 4,
            'totalHeal' : 1,
            'totalDamageTaken' : 5,
            'goldEarned' : 5,
            'visionScore' : 3,
            'visionWardsBoughtInGame' : 5,
            'totalMinionsKilled' : 5,
            'neutralMinionsKilled' : 1,
            'kills' : 5,
            'deaths' : 4,
            'assists' : 2,
        }

    elif match['position'] == 'jungle':

         multipliers = {
            'totalDamageDealtToChampions' : 3,
            'damageDealtToTurrets' : 5,
            'damageDealtToObjectives' : 3,
            'totalHeal' : 3,
            'totalDamageTaken' : 2,
            'goldEarned' : 4,
            'visionScore' : 3,
            'visionWardsBoughtInGame' : 5,
            'totalMinionsKilled' : 5,
            'neutralMinionsKilled' : 4,
            'kills' : 3,
            'deaths' : 2,
            'assists' : 3,
        }

    elif match['position'] == 'bot':

         multipliers = {
            'totalDamageDealtToChampions' : 4,
            'damageDealtToTurrets' : 4,
            'damageDealtToObjectives' : 4,
            'totalHeal' : 1,
            'totalDamageTaken' : 5,
            'goldEarned' : 5,
            'visionScore' : 3,
            'visionWardsBoughtInGame' : 5,
            'totalMinionsKilled' : 5,
            'neutralMinionsKilled' : 1,
            'kills' : 5,
            'deaths' : 4,
            'assists' : 2,
        }

    elif match['position'] == 'supp':
        
         multipliers = {
            'totalDamageDealtToChampions' : 3,
            'damageDealtToTurrets' : 5,
            'damageDealtToObjectives' : 3,
            'totalHeal' : 5,
            'totalDamageTaken' : 2,
            'goldEarned' : 5,
            'visionScore' : 5,
            'visionWardsBoughtInGame' : 5,
            'totalMinionsKilled' : 5,
            'neutralMinionsKilled' : 1,
            'kills' : 4,
            'deaths' : 3,
            'assists' : 4,
        }

    else:
        return round(points)

    points += (match['stats']['totalDamageDealtToChampions'] / 1500)* multipliers['totalDamageDealtToChampions'] 
    points += (match['stats']['damageDealtToTurrets']/ 1000) * multipliers['damageDealtToTurrets'] 
    points += (match['stats']['damageDealtToObjectives']/ 1200) * multipliers['damageDealtToObjectives'] 
    points += (match['stats']['totalHeal']/ 1000) * multipliers['totalHeal']
    points -= (match['stats']['totalDamageTaken']/1600) * multipliers['totalDamageTaken'] 
    points += (match['stats']['goldEarned']/ 700) * multipliers['goldEarned'] 
    points += (match['stats']['visionScore']/ 2) * multipliers['visionScore'] 
    points += match['stats']['visionWardsBoughtInGame'] * multipliers['visionWardsBoughtInGame'] 
    points += (match['stats']['totalMinionsKilled']/ 10) * multipliers['totalMinionsKilled'] 
    points += (match['stats']['neutralMinionsKilled']/ 6) * multipliers['neutralMinionsKilled'] 
    points += match['stats']['kills'] * multipliers['kills'] 
    points -= match['stats']['deaths'] * multipliers['deaths'] 
    points += match['stats']['assists'] * multipliers['assists'] 

    return round(points)


def insert_ranking(players_points):
    database.insert_ranking(players_points)

def runAll():
    players_matches = get_accs_data()
    match_dto = get_accs_matches_info(players_matches)
    players_points = point_processing(match_dto)
    json_ranking = json.dumps(players_points)
    insert_ranking(json_ranking)
    print('fecho o pastel!')

runAll()