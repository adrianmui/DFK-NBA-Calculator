# FantasyCalculator.
#
# Created by adrian mui on 4/4/16.
#---------------------------------------------------------------------

from __future__ import division
from nba_py import _api_scrape, _get_json, HAS_PANDAS
from nba_py import game
from nba_py.player import get_player
from nba_py import player
from nba_py.constants import *
import nbastats.nbastats as nbastats
import numpy
import json
#---------------------------------------------------------------------

def main(argv=None):
    #acquiring player's information using get_player(NAME)
    #I want LBJ's points, reb, ast, stl, blk, to, 3pm
    #I want LBJ's last 10 games information
    #I want to calculate LBJ's DK points
    #I want to determine if LBJ's DK points exceeds/dissapoints salary * (multiplier)
    
    #input first name last name salary
    firstName = raw_input('input firstname: ')
    lastName = raw_input('input lastname: ')
    salary = raw_input('input salary: $')
    
    dfkPlayerList = player.PlayerList()
    
    #print dfkPlayerList.info()
    
    plyr = player.PlayerGameLogs(get_player(firstName,lastName)).info()
    
    #getting the player's name name
    plyrName = player.PlayerSummary(plyr.get('Player_ID')[0]).info().get('DISPLAY_FIRST_LAST')[0]

    plyrGameLog = playerGetGameLog(plyr)
    DFPKList = []

    # calculating DFK from GameLog
    for i in range(0,len(plyrGameLog)):
        DFPKList.append(calculate_DKFP(plyrGameLog[i][0],plyrGameLog[i][1],plyrGameLog[i][2],plyrGameLog[i][3],plyrGameLog[i][4],plyrGameLog[i][5],plyrGameLog[i][6]))

    #outputs
    
    print '\n__[%s]__ DFKpoints for the 2015-2016 season \n' % (plyrName)
    print DFPKList
    print exceeds_expectation(DFPKList, numpy.float(salary), 5.6)


    s = 'abcdefghijklmnop'
    temp = ''
    for letter in s:
        print letter
        temp = letter + temp
    print temp




#---------------------------------------------------------------------

#returns a list of player's statline/gamelogs
def playerGetGameLog(player):
    
    playerPoints = pandasConvertToList(player.get('PTS'))
    playerRebound = pandasConvertToList(player.get('REB'))
    playerAssist = pandasConvertToList(player.get('AST'))
    playerTurnover = pandasConvertToList(player.get('TOV'))
    playerThree = pandasConvertToList(player.get('FG3M'))
    playerSteal = pandasConvertToList(player.get('STL'))
    playerBlock = pandasConvertToList(player.get('BLK'))
    categories = [playerPoints,playerThree,playerRebound,playerAssist,playerSteal,playerBlock,playerTurnover]

    gameLog = []

    for i in range(0,len(playerPoints), 1):
        list = []
        for x in range(0,len(categories),1):
            list.append(categories[x][i])
        gameLog.append(list)
    return gameLog

# converts pandas.series object to list object
def pandasConvertToList(aPandaSeries):
    list = []
    for line in aPandaSeries:
        list.append(line)
    return list

#returns a player's Daily Fantasy Points as a float value
def calculate_DKFP(pts, tpm, reb, ast, stl, blk, tov):
    num = pts+0.5*tpm+1.25*reb+1.5*ast+2*(stl+blk)-0.5*tov
    if pts >= 10:
        if reb >= 10:
            num += 1.5
            if ast >= 10:
                num += 3
        elif ast >= 10:
            num += 1.5
    return num

#takes a player's playerDFPlog and prints amount of times a player has exceeded his value
def exceeds_expectation(playerDFPlog, salary, multiplier):
    recent = 0
    count = 0
    games = 0
    if salary >= 9.0:
        multiplierM = 5.3
    else:
        multiplierM = multiplier
    
    for i in range(0, len(playerDFPlog), 1):
        if playerDFPlog[i] >= (salary * multiplierM):
            if i <= 10:
                recent += 1
            count += 1
        games += 1
    
    print '\nexceeded expected value of [%s] in [%s] out of [%s] games.' % (salary * multiplierM, count, games)
    print 'exceeded expected value [%s] percent of the time.' % (int(count / games * 100))
    print 'last 10 games: exceeded expected value [%s] times.' % (recent)

#---------------------------------------------------------------------

if __name__ == '__main__':
    main()