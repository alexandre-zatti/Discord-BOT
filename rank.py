import db as database
from riotwatcher import LolWatcher, ApiError


riotApi = LolWatcher('RGAPI-c1d2b59b-63a1-4588-966a-c014444ea72e')

region = 'br1'

async def get_accs_data():
    res = database.get_acc_names()
    players_matches = {}

    for r in res:
        acc_info = riotApi.summoner.by_name(region,r[0])
        players_matches[acc_info['name']] = riotApi.match.matchlist_by_account(region,acc_info['accountId'],'','','','',10)['matches']

    return players_matches


async def get_accs_matches_info(players_matches):
    
    match_dto = {}
    
    for player in players_matches:
        match_dto[player] = []
        for match in players_matches[player]:
            match_info = riotApi.match.by_id(region,match['gameId'])
            match_champ_id = match['champion']
            match_dto[player].append(await match_info_procesing(match_info, match_champ_id))

    return match_dto


async def match_info_procesing(match_info, match_champ_id):
    for participant in match_info['participants']:
        if participant['championId'] == match_champ_id:
            return participant


async def point_processing(match_dto):
    players_points = {}

    for player in match_dto:
        players_points[player] = 0
        for match in match_dto[player]:
            points = await statistic_calculation(match['timeline']['role'],match['timeline']['lane'],match)
            players_points[player]+= points

    return players_points

async def statistic_calculation(role, lane, match):
    
    #lane = MIDDLE,NONE,TOP,JUNGLE,BOTTOM
    #role = DUO_SUPPORT,SOLO,NONE,DUO_CARRY
    #lane 0:adc/1:sup/2:mid/3:jng/4:top
    
    points = 0
    teste = 5
    tabela = []

    tabela = [[5, 1, 5, 2, 3], [4, 2, 4, 2, 5], [4, 2, 4, 3, 3], [5, 2, 3, 5, 3], [-1, 3, -1, 3, 4], [5, 2, 5, 4, 4], [3, 5, 3, 4, 3], [5, 5, 5, 5, 5], [5, 1, 5, 1, 5], [1, 1, 1, 5, 1], [5, 1, 5, 3, 3], [-1, -4, -1, -3, -3], [2, 4, 2, 3, 3]]
    
    if lane == 'TOP' and role == 'SOLO':
        teste = 4

    if lane == 'MIDDLE' and role == 'SOLO':

        teste = 2

    if lane == 'JUNGLE' and role == 'NONE':

        teste = 3

    if lane == 'BOTTOM' and role == 'DUO_CARRY':

        teste = 0

    if lane == 'BOTTOM' and role == 'DUO_SUPPORT':
        
        teste = 1
    
    if lane == 5 :
        return points


    print('teste1 '+ tabela[0][teste])
    print('teste2 '+ teste)

    points += (match['stats']['totalDamageDealtToChampions'] / 1500)/ tabela[0][teste]
    points += (match['stats']['damageDealtToTurrets']/ 1000) / tabela[1][teste]
    points += (match['stats']['damageDealtToObjectives']/ 1200) / tabela[2][teste]
    points += (match['stats']['totalHeal']/ 1000) /tabela[3][teste]
    points += (match['stats']['totalDamageTaken']/1600)  / tabela[4][teste]
    points += (match['stats']['goldEarned']/ 700) / tabela[5][teste]
    points += (match['stats']['visionScore']/ 2) /  tabela[6][teste]
    points += match['stats']['visionWardsBoughtInGame'] / tabela[7][teste]
    points += (match['stats']['totalMinionsKilled']/ 10) / tabela[8][teste]
    points += (match['stats']['neutralMinionsKilled']/ 6) / tabela[9][teste]
    points += match['stats']['kills'] / tabela[10][teste]
    points += match['stats']['deaths'] / tabela[11][teste]
    points += (match['stats']['assists']/2) / tabela[12][teste]

    return points
    
    # if match['stats']['win']:

    #     points = 50000
    #     return points
    
    # if match['stats']['win'] == False:

    #     points = 10000
    #     return points



