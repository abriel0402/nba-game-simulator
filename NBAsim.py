from bs4 import BeautifulSoup
import requests
import random
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import time
from cgitb import text
from tempfile import gettempdir
import tkinter as tk
from tkinter import *
from tkinter import ttk
import os 

def main(year, name1, name2):
    POSSESSIONS = 134
    MINUTES = 48


                
    yearStandings = requests.get("https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_standings.html").text
    site = "https://www.basketball-reference.com"

    yearStandingsSoup = BeautifulSoup(yearStandings, "lxml")

    teams = yearStandingsSoup.find_all("th", class_ = "left")
    teamTags = []
    rosterSites = []


    for team in teams:
        if "Conference" in team:
            continue
        else:
            teamTags.append(team)


    for team in teamTags:
        if name1.lower() in (team.text).lower():
            team1Name = team.text
            if "*" in team1Name:
                team1Name = team1Name[:-1]
            for a in team.find_all('a', href=True):
                rosterSites.append(site + a['href'])
        if name2.lower() in (team.text).lower():
            team2Name = team.text
            if "*" in team2Name:
                team2Name = team2Name[:-1]
            for a in team.find_all('a', href=True):
                rosterSites.append(site + a['href'])


    team1Site = requests.get(rosterSites[0]).text
    team2Site = requests.get(rosterSites[1]).text

    team1RosterSoup = BeautifulSoup(team1Site, "lxml")
    team2RosterSoup = BeautifulSoup(team2Site, "lxml")

    team1Players = team1RosterSoup.find_all("td", attrs={"data-stat" : "player"})
    team2Players = team2RosterSoup.find_all("td", attrs={"data-stat" : "player"})

    team1PlayerSites = []
    team2PlayerSites = []

    for player in team1Players:
        for a in player.find_all('a', href=True):
            if (site + a['href']) not in team1PlayerSites:
                team1PlayerSites.append(site + a['href'])
    for player in team2Players:
        for a in player.find_all('a', href=True):
            if (site + a['href']) not in team2PlayerSites:
                team2PlayerSites.append(site + a['href'])
    team1Roster = []
    team2Roster = []

    class Player:
        def __init__(self, name, fg, fg3, ast, orb, drb, stl, blk, tov, usg, mp, ws, ppg, apg, pts=0, asts=0, rebs=0, stls=0, blks=0, tovs=0, hasBall=False):
            self.name = name
            self.fg = fg
            self.fg3 = fg3
            self.ast = ast
            self.orb = orb
            self.drb = drb
            self.stl = stl
            self.blk = blk
            self.tov = tov
            self.usg = usg
            self.mp = mp
            self.ws = ws
            self.ppg = ppg
            self.apg = apg
            self.pts = pts
            self.asts = asts
            self.rebs = rebs
            self.stls = stls
            self.blks = blks
            self.tovs = tovs
            self.hasBall = hasBall
            self.usgScore = (0.2*(float(usg)))+(1*(float(ppg)))
            if self.usgScore > 30.0:
                self.usgScore *= 0.9
            self.fgScore = (float(fg)*0.5)+(float(ppg)*0.9)
            self.fg3Score = (float(fg3)*0.5)+(float(ppg)*0.9)
            self.astScore = (float(apg)*2.3)+(float(ast)*0.15)/2
            if self.astScore > 17.0 and self.astScore < 21.0:
                self.astScore *= 0.8
            if self.astScore >= 21.0:
                self.astScore *= 0.7
    for site in team1PlayerSites:
        playerProfile = requests.get(site).text
        playerProfileSoup = BeautifulSoup(playerProfile, 'lxml')
        playerNameTag = playerProfileSoup.find_all("h1")
        for x in playerNameTag:
            name = x.text
        name = name[1:-1]
        team1YearSoup = playerProfileSoup.find_all("tr", id={"per_game." + str(year)})
        team1AdvYearSoup = playerProfileSoup.find_all("tr", id={"advanced." + str(year)})
        for stat in team1YearSoup:
            for i in stat:
                if i["data-stat"] == "fg_pct":
                    fg = (i.text)
                    if fg == '':
                        fg = 0.100
                if i["data-stat"] == "fg3_pct":
                    fg3 = (i.text)
                    if fg3 == '':
                        fg3 = 0.100
                if i["data-stat"] == "mp_per_g":
                    mp = (i.text)
                if i["data-stat"] == "pts_per_g":
                    ppg = (i.text)
                if i["data-stat"] == "ast_per_g":
                    apg = (i.text)
                
        for stat in team1AdvYearSoup:
            for i in stat:
                if i["data-stat"] == "ast_pct":
                    ast = (i.text)
                if i["data-stat"] == "orb_pct":
                    orb = (i.text)
                if i["data-stat"] == "drb_pct":
                    drb = (i.text)
                if i["data-stat"] == "stl_pct":
                    stl = (i.text)
                if i["data-stat"] == "blk_pct":
                    blk = (i.text)
                if i["data-stat"] == "tov_pct":
                    tov = (i.text)
                if i["data-stat"] == "usg_pct":
                    usg = (i.text)
                if i["data-stat"] == "ws":
                    ws = (i.text)
                
        player = Player(name, fg, fg3, ast, orb, drb, stl, blk, tov, usg, mp, ws, ppg, apg)
        team1Roster.append(player)

    for site in team2PlayerSites:
        playerProfile = requests.get(site).text
        playerProfileSoup = BeautifulSoup(playerProfile, 'lxml')
        playerNameTag = playerProfileSoup.find_all("h1")
        for x in playerNameTag:
            name = x.text
        name = name[1:-1]
        team2YearSoup = playerProfileSoup.find_all("tr", id={"per_game." + str(year)})
        team2AdvYearSoup = playerProfileSoup.find_all("tr", id={"advanced." + str(year)})
        for stat in team2YearSoup:
            for i in stat:
                if i["data-stat"] == "fg_pct":
                    fg = (i.text)
                    if fg == '':
                        fg = 0.100
                if i["data-stat"] == "fg3_pct":
                    fg3 = (i.text)
                    if fg3 == '':
                        fg3 = 0.100
                if i["data-stat"] == "mp_per_g":
                    mp = (i.text)
                if i["data-stat"] == "pts_per_g":
                    ppg = (i.text)
                if i["data-stat"] == "ast_per_g":
                    apg = (i.text)
        for stat in team2AdvYearSoup:
            for i in stat:
                if i["data-stat"] == "ast_pct":
                    ast = (i.text)
                if i["data-stat"] == "orb_pct":
                    orb = (i.text)
                if i["data-stat"] == "drb_pct":
                    drb = (i.text)
                if i["data-stat"] == "stl_pct":
                    stl = (i.text)
                if i["data-stat"] == "blk_pct":
                    blk = (i.text)
                if i["data-stat"] == "tov_pct":
                    tov = (i.text)
                if i["data-stat"] == "usg_pct":
                    usg = (i.text)
                if i["data-stat"] == "ws":
                    ws = (i.text)
                
        player = Player(name, fg, fg3, ast, orb, drb, stl, blk, tov, usg, mp, ws, ppg, apg)
        team2Roster.append(player)

    #Sorts rosters in order of most win shares to slice off the extra bad players
    #----------
    for player in team1Roster:
        def sortByWs(player):
            return float(player.ws)
        team1Roster.sort(reverse=True, key=sortByWs)

    for player in team2Roster:
        def sortByWs(player):
            return float(player.ws)
        team2Roster.sort(reverse=True, key=sortByWs)

    team1Roster = team1Roster[0:11]
    team2Roster = team2Roster[0:11]

    #----------

    class Team:
        def __init__(self, name, roster):
            self.name = name
            self.roster = roster

    team1 = Team(team1Name, team1Roster)
    team2 = Team(team2Name, team2Roster)

    #-----------------------------#
    # Below is the simulating #
    #-----------------------------#

    team1OnTheFloor = []
    team2OnTheFloor = []

    team1Points = 0
    team2Points = 0

    def addPlayersOnFloor(teamRoster, teamOnTheFloor):
        while len(teamOnTheFloor) < 5:
            for player in teamRoster:
                if player not in teamOnTheFloor:
                    min_pct = (float(player.mp) / MINUTES) * 100
                    randomNum = random.uniform(0, 100)
                    if randomNum <= min_pct:
                        teamOnTheFloor.append(player)
        return teamOnTheFloor


    #TEAM 1 OFFENSIVE POSSESIONS
    for i in range(POSSESSIONS):
        PlayerHasBall = False
        MadeShot = False
        Assist = False
        MissedShot = False
        Rebound = False
        Blocked = False
        Stolen = False

        #OFFENSE PLAYERS
        team1OnTheFloor = addPlayersOnFloor(team1.roster, team1OnTheFloor)
        

        #DEFENSE PLAYERS
        team2OnTheFloor = addPlayersOnFloor(team2.roster, team2OnTheFloor)

        #SORTS PLAYERS BY MINUTES PLAYED
        if len(team1OnTheFloor) > 1:
            for player in team1OnTheFloor:
                def sortByMin(player):
                    return float(player.mp)
                team1OnTheFloor.sort(reverse=True, key=sortByMin)
        
        
        if len(team2OnTheFloor) > 1:
            for player in team2OnTheFloor:
                def sortByMin(player):
                    return float(player.mp)
                team2OnTheFloor.sort(reverse=True, key=sortByMin)

        # Decides who can shoot this posession
        for player in team1OnTheFloor:
            def sortByUsgScore(player):
                return player.usgScore
            team1OnTheFloor.sort(reverse=True, key=sortByUsgScore)

        for player in team1OnTheFloor:
            if PlayerHasBall == False:
                randomNum = random.uniform(0, 100)
                if randomNum <= float(player.usg):
                    #print(player.name + " has the ball")
                    PlayerHasBall = True
                    player.hasBall = True
            
            if player.hasBall:
                # Steal/Blk/Tov
                randomNum = random.randint(0, 4)
                defensivePlayer = team2OnTheFloor[randomNum]
                offNum = random.uniform(0, float(player.tov))
                randomNum = random.randint(1, 5)
                if randomNum == 1 or randomNum == 2 or randomNum == 3:
                    defNum = random.uniform(0, float(defensivePlayer.stl))
                else:
                    defNum = random.uniform(0, float(defensivePlayer.blk))
                if offNum >= defNum:
                    pass
                else:
                    if randomNum == 1 or randomNum == 2 or randomNum == 3:
                        Stolen = True
                        player.tovs += 1
                        defensivePlayer.stls += 1
                        #print(defensivePlayer.name + " stole the ball")
                        player.hasBall = False
                    else:
                        Blocked = True
                        player.tovs += 1
                        defensivePlayer.blks += 1
                        #print(defensivePlayer.name + " blocked the shot")
                        player.hasBall = False

                # 3pt or 2pt
                if player.hasBall == True:
                    randomNum = random.uniform(0, 100)
                    if randomNum <= 35.9 and Stolen == False and Blocked == False:
                        randomNum = random.uniform(0, 100)
                        if randomNum <= (float(player.fg3))*100:
                            MadeShot = True
                            #print(player.name + " scored a 3 pointer")
                            player.pts += 3    
                            team1Points += 3
                            player.hasBall = False
                            MadeShot = True
                            Rebound = True
                        else:
                            MadeShot = False
                            MissedShot = True 
                            #print(player.name + " missed a 3 pointer")
                            player.hasBall = False
                            Rebound = False

                    elif Stolen == False and Blocked == False:
                        randomNum = random.uniform(0, 100)
                        if randomNum <= (float(player.fg))*100:
                            MadeShot = True
                            player.pts += 2
                            #print(player.name + " scored a 2 pointer")
                            team1Points += 2
                            player.hasBall = False
                            Rebound = True
                        else:
                            MissedShot = True
                            MadeShot = False
                            #print(player.name + " missed a 2 pointer")
                            player.hasBall = False
                            Rebound == False

                #Rebound
                if MadeShot == False and Rebound == False:
                    MissedShot = True
                    while Rebound == False:
                        randomNum = random.randint(0, 4)
                        defensivePlayer = team2OnTheFloor[randomNum]
                        randomNum = random.uniform(0, 100)
                        if randomNum <= float(defensivePlayer.drb):
                            defensivePlayer.rebs += 1
                            Rebound = True
                        else:
                            randomNum = random.randint(0, 4)
                            currentPlayer = team1OnTheFloor[randomNum]
                            while currentPlayer == player:
                                randomNum = random.randint(0, 4)
                                currentPlayer = team1OnTheFloor[randomNum]
                            randomNum = random.uniform(0, 100)
                            if randomNum <= float(currentPlayer.orb):
                                currentPlayer.rebs += 1
                                Rebound = True
            #Assist
            if MadeShot == True and Assist == False:
                for p in team1OnTheFloor:
                    if p != player and Assist == False:
                        randomNum = random.uniform(0, 100)
                        randomNum *= 10
                        if randomNum <= float(p.astScore):
                            p.asts += 1
                            Assist = True
        
        #removes players from the floor to allow new possession with new players
        player.hasBall = False
        while len(team1OnTheFloor) > 0:
            team1OnTheFloor.pop()
        while len(team2OnTheFloor) > 0:
            team2OnTheFloor.pop()

    #TEAM 2 OFFENSIVE POSSESIONS
    for i in range(POSSESSIONS):
        PlayerHasBall = False
        MadeShot = False
        Assist = False
        MissedShot = False
        Rebound = False
        Blocked = False
        Stolen = False

        #OFFENSE PLAYERS
        team2OnTheFloor = addPlayersOnFloor(team2.roster, team2OnTheFloor)
        

        
        #DEFENSE PLAYERS
        team1OnTheFloor = addPlayersOnFloor(team1.roster, team1OnTheFloor)

        #SORTS PLAYERS BY MINUTES PLAYED
        if len(team2OnTheFloor) > 1:
            for player in team2OnTheFloor:
                def sortByMin(player):
                    return float(player.mp)
                team2OnTheFloor.sort(reverse=True, key=sortByMin)
        
        
        if len(team1OnTheFloor) > 1:
            for player in team1OnTheFloor:
                def sortByMin(player):
                    return float(player.mp)
                team1OnTheFloor.sort(reverse=True, key=sortByMin)

        #Who can shoot this posession
        for player in team2OnTheFloor:
            def sortByUsgScore(player):
                return player.usgScore
            team2OnTheFloor.sort(reverse=True, key=sortByUsgScore)

        for player in team2OnTheFloor:
            if PlayerHasBall == False:
                randomNum = random.uniform(0, 100)
                if randomNum <= float(player.usg):
                    #print(player.name + " has the ball")
                    PlayerHasBall = True
                    player.hasBall = True
            
            if player.hasBall:
                # Steal/Blk/Tov
                randomNum = random.randint(0, 4)
                defensivePlayer = team1OnTheFloor[randomNum]
                offNum = random.uniform(0, float(player.tov))
                randomNum = random.randint(1, 5)
                if randomNum == 1 or randomNum == 2 or randomNum == 3:
                    defNum = random.uniform(0, float(defensivePlayer.stl))
                else:
                    defNum = random.uniform(0, float(defensivePlayer.blk))
                if offNum >= defNum:
                    pass
                else:
                    if randomNum == 1 or randomNum == 2 or randomNum == 3:
                        Stolen = True
                        player.tovs += 1
                        defensivePlayer.stls += 1
                        #print(defensivePlayer.name + " stole the ball")
                        player.hasBall = False
                    else:
                        Blocked = True
                        player.tovs += 1
                        defensivePlayer.blks += 1
                        #print(defensivePlayer.name + " blocked the shot")
                        player.hasBall = False

                # 3pt or 2pt
                if player.hasBall == True:
                    randomNum = random.uniform(0, 100)
                    if randomNum <= 35.9 and Stolen == False and Blocked == False:
                        randomNum = random.uniform(0, 100)
                        if randomNum <= (float(player.fg3))*100:
                            MadeShot = True
                            #print("---")
                            #print(player.name + " scored a 3 pointer")
                            player.pts += 3    
                            team2Points += 3
                            player.hasBall = False
                            MadeShot = True
                            Rebound = True
                        else:
                            MadeShot = False
                            MissedShot = True 
                            #print(player.name + " missed a 3 pointer")
                            player.hasBall = False
                            Rebound = False

                    elif Stolen == False and Blocked == False:
                        randomNum = random.uniform(0, 100)
                        if randomNum <= (float(player.fg))*100:
                            MadeShot = True
                            player.pts += 2
                            #print("---")
                            #print(player.name + " scored a 2 pointer")
                            team2Points += 2
                            player.hasBall = False
                            Rebound = True
                        else:
                            MissedShot = True
                            MadeShot = False
                            #print(player.name + " missed a 2 pointer")
                            player.hasBall = False
                            Rebound == False

                #Rebound
                if MadeShot == False and Rebound == False:
                    MissedShot = True
                    while Rebound == False:
                        randomNum = random.randint(0, 4)
                        defensivePlayer = team1OnTheFloor[randomNum]
                        randomNum = random.uniform(0, 100)
                        if randomNum <= float(defensivePlayer.drb):
                            defensivePlayer.rebs += 1
                            Rebound = True
                        else:
                            randomNum = random.randint(0, 4)
                            currentPlayer = team2OnTheFloor[randomNum]
                            while currentPlayer == player:
                                randomNum = random.randint(0, 4)
                                currentPlayer = team2OnTheFloor[randomNum]
                            randomNum = random.uniform(0, 100)
                            if randomNum <= float(currentPlayer.orb):
                                currentPlayer.rebs += 1
                                Rebound = True
            #assists
            if MadeShot == True and Assist == False:
                for p in team2OnTheFloor:
                    if p != player and Assist == False:
                        randomNum = random.uniform(0, 10)
                        randomNum *= 10
                        if randomNum <= float(p.astScore):
                            p.asts += 1
                            #print("assisted by " + p.name + "(" + str(p.astScore) + ")")
                            #print(str(randomNum) + " out of " + str(p.astScore))
                            Assist = True
        
        #removes players from the floor to allow new possession with new players
        player.hasBall = False
        while len(team2OnTheFloor) > 0:
            team2OnTheFloor.pop()
        while len(team1OnTheFloor) > 0:
            team1OnTheFloor.pop()


    for player in team1.roster:
        def sortByPts(player):
                return player.pts
        team1.roster.sort(reverse=True, key=sortByPts)

    for player in team2.roster:
        def sortByPts(player):
                return player.pts
        team2.roster.sort(reverse=True, key=sortByPts)

    print(team1.name + ": " + str(team1Points))
    for player in team1.roster:
        print(player.name + ": " + str(player.pts) + " / " + str(player.asts) + " / " + str(round(player.rebs*0.65)) + " / " + str(player.stls) + " / " + str(player.blks) + " / " + str(player.tovs))
    print("-------------")
    print(team2.name + ": " + str(team2Points))
    for player in team2.roster:
        print(player.name + ": " + str(player.pts) + " / " + str(player.asts) + " / " + str(round(player.rebs*0.65)) + " / " + str(player.stls) + " / " + str(player.blks) + " / " + str(player.tovs)) 
    
    results.append(team1)
    results.append(team2)
    removeWidget(textField)
    removeWidget(button)
    removeWidget(label)

    e = 0.05

    #for left team
    Label(window, text=team1.name, font=("Times New Roman", 20)).place(relx=0.27, rely=0.1, anchor=CENTER)
    Label(window, text=team1Points, font=("Times New Roman", 15)).place(relx=0.27, rely=0.15, anchor=CENTER)
    Label(window, text="PLAYER", font=("Times New Roman", 11)).place(relx=0.12, rely=0.2, anchor=CENTER)
    Label(window, text="PTS", font=("Times New Roman", 11)).place(relx=0.17, rely=0.2, anchor=CENTER)
    Label(window, text="AST", font=("Times New Roman", 11)).place(relx=0.22, rely=0.2, anchor=CENTER)
    Label(window, text="REB", font=("Times New Roman", 11)).place(relx=0.27, rely=0.2, anchor=CENTER)
    Label(window, text="STL", font=("Times New Roman", 11)).place(relx=0.32, rely=0.2, anchor=CENTER)
    Label(window, text="BLK", font=("Times New Roman", 11)).place(relx=0.37, rely=0.2, anchor=CENTER)
    Label(window, text="TOV", font=("Times New Roman", 11)).place(relx=0.42, rely=0.2, anchor=CENTER)

    #for right team
    Label(window, text=team2.name, font=("Times New Roman", 20)).place(relx=0.73, rely=0.1, anchor=CENTER)
    Label(window, text=team2Points, font=("Times New Roman", 15)).place(relx=0.73, rely=0.15, anchor=CENTER)
    Label(window, text="PLAYER", font=("Times New Roman", 11)).place(relx=0.58, rely=0.2, anchor=CENTER)
    Label(window, text="PTS", font=("Times New Roman", 11)).place(relx=0.63, rely=0.2, anchor=CENTER)
    Label(window, text="AST", font=("Times New Roman", 11)).place(relx=0.68, rely=0.2, anchor=CENTER)
    Label(window, text="REB", font=("Times New Roman", 11)).place(relx=0.73, rely=0.2, anchor=CENTER)
    Label(window, text="STL", font=("Times New Roman", 11)).place(relx=0.78, rely=0.2, anchor=CENTER)
    Label(window, text="BLK", font=("Times New Roman", 11)).place(relx=0.83, rely=0.2, anchor=CENTER)
    Label(window, text="TOV", font=("Times New Roman", 11)).place(relx=0.88, rely=0.2, anchor=CENTER)

    for player in team1.roster:
        Label(window, text=(player.name), font=("Times New Roman", 10)).place(relx=0.12, rely=0.2+e, anchor=CENTER)
        Label(window, text=(str(player.pts)), font=("Times New Roman", 10)).place(relx=0.17, rely=0.2+e, anchor=CENTER)
        Label(window, text=(str(player.asts)), font=("Times New Roman", 10)).place(relx=0.22, rely=0.2+e, anchor=CENTER)
        Label(window, text=(str(player.rebs)), font=("Times New Roman", 10)).place(relx=0.27, rely=0.2+e, anchor=CENTER)
        Label(window, text=(str(player.stls)), font=("Times New Roman", 10)).place(relx=0.32, rely=0.2+e, anchor=CENTER)
        Label(window, text=(str(player.blks)), font=("Times New Roman", 10)).place(relx=0.37, rely=0.2+e, anchor=CENTER)
        Label(window, text=(str(player.tovs)), font=("Times New Roman", 10)).place(relx=0.42, rely=0.2+e, anchor=CENTER)
        e += 0.05
    e = 0.05
    for player in team2.roster:
        Label(window, text=(player.name), font=("Times New Roman", 10)).place(relx=0.58, rely=0.2+e, anchor=CENTER)
        Label(window, text=(str(player.pts)), font=("Times New Roman", 10)).place(relx=0.63, rely=0.2+e, anchor=CENTER)
        Label(window, text=(str(player.asts)), font=("Times New Roman", 10)).place(relx=0.68, rely=0.2+e, anchor=CENTER)
        Label(window, text=(str(player.rebs)), font=("Times New Roman", 10)).place(relx=0.73, rely=0.2+e, anchor=CENTER)
        Label(window, text=(str(player.stls)), font=("Times New Roman", 10)).place(relx=0.78, rely=0.2+e, anchor=CENTER)
        Label(window, text=(str(player.blks)), font=("Times New Roman", 10)).place(relx=0.83, rely=0.2+e, anchor=CENTER)
        Label(window, text=(str(player.tovs)), font=("Times New Roman", 10)).place(relx=0.88, rely=0.2+e, anchor=CENTER)
        e += 0.05
    

    



window = tk.Tk()


def removeWidget(widget):
    widget.destroy()


def getData():
    global textField
    if len(userInput) == 0:
        data = int(textField.get())
        if int(data) < 1980 or int(data) > 2022:
            label.configure(text="Invalid input, enter year between 1980-2022")
        else:
            userInput.append(int(textField.get()))
            label.configure(text="Enter team #1 name")
    elif len(userInput) == 1:
        userInput.append(textField.get())
        label.configure(text="Enter team #2 name")
    elif len(userInput) == 2:
        userInput.append(textField.get())
        main(userInput[0], userInput[1], userInput[2])

    

        
      

def getTeam():
    global textField
    label.configure(text="Enter team #1 name")
    if len(userInput) == 1:
        
        userInput.append(textField.get())
    elif len(userInput) == 2:
        label.configure(text="Enter team #2 name")
        userInput.append(textField.get())
        main(userInput[0], userInput[1], userInput[2])
    else:
        print(str(userInput[0]) + userInput[1] + userInput[2])
            
    


label = Label(window, text="Enter year between 1980-2022", font=("Times New Roman", 15))
label.place(relx=0.5, rely=0.2, anchor=CENTER)


textField = Entry(window)
textField.place(relx=0.5, rely=0.25, anchor=CENTER)

userInput = []
results = []

button = Button(window, text="Enter", fg="black", command=getData)
button.place(relx=0.575, rely=0.25, anchor=CENTER)

window.title("Title")
window.geometry("1358x764")
window.mainloop()

                  
# -------------------------- ui stuff above ---------------------

#----------------main program below----------------------
