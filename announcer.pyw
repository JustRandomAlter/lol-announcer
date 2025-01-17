import requests
import time
import urllib3
import audioplayer
from os import path, _exit
import random
from tkinter import *
import threading

SOUNDS_FOLDER = "sounds/"
EVENT_SOUNDS = {
    "Welcome": ["welcometosummonersrift1.mp3", "welcometosummonersrift2.mp3", "welcometosummonersrift3.mp3", "welcometosummonersrift4.mp3"],
    "MinionsSpawningSoon": ["30secondsuntilminionsspawn1.mp3", "30secondsuntilminionsspawn2.mp3", "30secondsuntilminionsspawn3.mp3", "30secondsuntilminionsspawn4.mp3", "30secondsuntilminionsspawn5.mp3", "30secondsuntilminionsspawn6.mp3", "30secondsuntilminionsspawn7.mp3", "30secondsuntilminionsspawn8.mp3", "30secondsuntilminionsspawn9.mp3", "30secondsuntilminionsspawn10.mp3"],
    "MinionsSpawning": ["minionshavespawned1.mp3", "minionshavespawned2.mp3", "minionshavespawned3.mp3"],
    "FirstBlood": ["firstblood1.mp3", "firstblood2.mp3", "firstblood3.mp3", "firstblood4.mp3"],
    "PlayerKill": ["youhaveslainanenemy1.mp3", "youhaveslainanenemy2.mp3", "youhaveslainanenemy3.mp3", "youhaveslainanenemy4.mp3", "youhaveslainanenemy5.mp3", "youhaveslainanenemy6.mp3", "youhaveslainanenemy7.mp3", "youhaveslainanenemy8.mp3", "youhaveslainanenemy9.mp3"],
    "PlayerDeath": ["youhavebeenslain1.mp3", "youhavebeenslain2.mp3", "youhavebeenslain3.mp3", "youhavebeenslain4.mp3", "youhavebeenslain5.mp3", "youhavebeenslain6.mp3", "youhavebeenslain7.mp3", "youhavebeenslain8.mp3", "youhavebeenslain9.mp3" ],
    "AllyDeath": ["anallyhasbeenslain1.mp3", "anallyhasbeenslain2.mp3", "anallyhasbeenslain3.mp3"],
    "AllyKill": ["anenemyhasbeenslain1.mp3", "anenemyhasbeenslain2.mp3", "anenemyhasbeenslain3.mp3", "anenemyhasbeenslain4.mp3", "anenemyhasbeenslain5.mp3", "anenemyhasbeenslain6.mp3", "anenemyhasbeenslain7.mp3"],
    "AllyDoubleKill": ["doublekill1.mp3", "doublekill2.mp3", "doublekill3.mp3", "doublekill4.mp3", "doublekill5.mp3", "doublekill6.mp3", "doublekill7.mp3", "doublekill8.mp3"],
    "AllyTripleKill": ["triplekill.mp3", "triplekill1.mp3", "triplekill2.mp3", "triplekill3.mp3", "triplekill4.mp3", "triplekill5.mp3", "triplekill6.mp3"],
    "AllyQuadraKill": ["quadrakill.mp3", "quadrakill1.mp3", "quadrakill2.mp3", "quadrakill3.mp3", "quadrakill4.mp3", "quadrakill5.mp3", "quadrakill6.mp3"],
    "AllyPentaKill": ["pentakill1.mp3", "pentakill2.mp3", "pentakill4.mp3", "pentakill5.mp3", "pentakill6.mp3", "pentakill7.mp3"],
    "PlayerKillingSpree" : ["killingspree.mp3","killingspree1.mp3","killingspree2.mp3","killingspree3.mp3"],
    "PlayerRampage" : ["playerrampage.mp3","playerrampage1.mp3","playerrampage2.mp3","playerrampage3.mp3"],
    "PlayerUnstoppable" : ["playerunstoppable1.mp3","playerunstoppable2.mp3","playerunstoppable3.mp3","playerunstoppable4.mp3"],
    "PlayerDominating" : ["playerdominating1.mp3","playerdominating2.mp3","playerdominating3.mp3","playerdominating4.mp3"],
    "PlayerGodlike" : ["playergodlike1.mp3","playergodlike2.mp3","playergodlike3.mp3","playergodlike4.mp3"],
    "PlayerLegendary" : ["playerlegendary1.mp3","playerlegendary2.mp3","playerlegendary3.mp3","playerlegendary4.mp3"],
    "EnemyDoubleKill": ["enemydoublekill.mp3"],
    "EnemyTripleKill": ["enemytriplekill.mp3"],
    "EnemyQuadraKill": ["enemyquadrakill.mp3"],
    "EnemyPentaKill": ["enemypentakill.mp3", "enemypentakill1.mp3", "enemypentakill2.mp3", "enemypentakill3.mp3", "enemypentakill4.mp3"],
    "AllyAce": ["allyace1.mp3", "allyace2.mp3", "allyace3.mp3", "allyace4.mp3", "allyace5.mp3", "allyace6.mp3", "allyace7.mp3", "allyace8.mp3", "allyace9.mp3"],
    "EnemyAce": ["enemyace.mp3"],
    "Executed": ["executed1.mp3", "executed2.mp3", "executed3.mp3", "executed4.mp3", "executed5.mp3", "executed6.mp3"],
    "AllyTurretKill": ["yourteamhasdestroyedaturret.mp3"],
    "EnemyTurretKill": ["yourturrethasbeendestroyed1.mp3", "yourturrethasbeendestroyed2.mp3"],
    "AllyInhibitorKill": ["yourteamhasdestroyedaninhibitor1.mp3", "yourteamhasdestroyedaninhibitor2.mp3"],
    "EnemyInhibitorKill": ["yourinhibitorhasbeendestroyed1.mp3", "yourinhibitorhasbeendestroyed2.mp3"],
    "AllyInhibitorRespawningSoon": ["yourinhibitorisrespawningsoon.mp3"],
    "EnemyInhibitorRespawningSoon": ["enemyinhibitorisrespawningsoon.mp3"],
    "AllyInhibitorRespawned": ["yourinhibitorhasrespawned.mp3"],
    "EnemyInhibitorRespawned": ["enemyinhibitorhasrespawned.mp3"],
    "Victory": ["victory.mp3"],
    "Defeat": ["defeat.mp3"],
}
volume = 100

def play_event_sound(event):
    ap = audioplayer.AudioPlayer(SOUNDS_FOLDER + random.choice(EVENT_SOUNDS[event]))
    ap.volume = volume
    ap.play(block=True)

def update_volume(v):
    global volume
    volume = int(v)
    
def play_random_sound():
    play_event_sound(random.choice(list(EVENT_SOUNDS.keys())))
    
def close_script():
    gui.quit()
    gui.destroy()
    _exit(1)
    
# Ignore the Unverified HTTPS request warning.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

previous_game_time = 0
game_time = 0
previous_event_count = 0
event_count = 0
player_killStreak = 0


# Get event count so if the program is started in the middle of the match it doesn't play every announcement
# sound which happened until that point.
try:
    # Get all data from the game in JSON format.
    all_game_data = requests.get('https://127.0.0.1:2999/liveclientdata/allgamedata', verify=False).json()
    
    events = all_game_data["events"]["Events"]
    event_count = len(events)
    previous_event_count = event_count
except:
    pass

def announcer_loop():
    # File for logging exceptions.
    log_file = open("log.txt", "w")
    
    global previous_game_time
    global game_time
    global previous_event_count
    global event_count
    global player_killStreak 
    
    while True:
        try:
            # Get all data from the game in JSON format.
            all_game_data = requests.get('https://127.0.0.1:2999/liveclientdata/allgamedata', verify=False).json()

            game_time = all_game_data["gameData"]["gameTime"]
            events = all_game_data["events"]["Events"]
            # TODO: move some things to only update once per game.
            player_name = all_game_data["activePlayer"]["summonerName"]
            player_team = ""
            team_order_players = []
            team_chaos_players = []
            ally_team_players = []
            enemy_team_players = []

            # Populate team chaos and team order players lists and figure out which team the player is on.
            for player in all_game_data["allPlayers"]:
                if player["team"] == "ORDER":
                    team_order_players.append(player["summonerName"])
                    if player["summonerName"] == player_name:
                        player_team = "ORDER"
                elif player["team"] == "CHAOS":
                    team_chaos_players.append(player["summonerName"])
                    if player["summonerName"] == player_name:
                        player_team = "CHAOS"

            # Populate ally and enemy team player lists.
            if player_team == "ORDER":
                ally_team_players = team_order_players
                enemy_team_players = team_chaos_players
            elif player_team == "CHAOS":
                ally_team_players = team_chaos_players
                enemy_team_players = team_order_players

            # Welcome announcement.
            if game_time >= 26 and previous_game_time < 26 and game_time < 28:
                play_event_sound("Welcome")
            # Minions spawning soon.
            if game_time >= 36 and previous_game_time < 36 and game_time < 38:
                play_event_sound("MinionsSpawningSoon")

            event_count = len(events)

            # Loop over all new events.
            for event_index in range(previous_event_count, event_count):
                event = events[event_index]
                event_name = event["EventName"]

                # Someone got first blood.
                if event_name == "ChampionKill" and event_index < event_count - 1 and events[event_index + 1]["EventName"] == "FirstBlood":
                    print("Got First Blood Event")
                    play_event_sound("FirstBlood")
                    event_index += 1
                # Someone got a multikill.
                elif event_name == "ChampionKill" and event_index < event_count - 1 and events[event_index + 1]["EventName"] == "Multikill":
                    multikill = events[event_index + 1]["KillStreak"]
                    # Ally got a multikill.
                    if event["KillerName"] in ally_team_players:
                        if multikill == 2:
                            play_event_sound("AllyDoubleKill")
                        elif multikill == 3:
                            play_event_sound("AllyTripleKill")
                        elif multikill == 4:
                            play_event_sound("AllyQuadraKill")
                        elif multikill == 5:
                            play_event_sound("AllyPentaKill")
                    # Enemy got a multikill.
                    elif event["KillerName"] in enemy_team_players:
                        if multikill == 2:
                            play_event_sound("EnemyDoubleKill")
                        elif multikill == 3:
                            play_event_sound("EnemyTripleKill")
                        elif multikill == 4:
                            play_event_sound("EnemyQuadraKill")
                        elif multikill == 5:
                            play_event_sound("EnemyPentaKill")
                    event_index += 1
                # Someone got a kill.
                elif event_name == "ChampionKill":
                    # Player got a kill.
                    print ("Got a Player_Kill Event")
                    if event["KillerName"] == player_name:
                        if player_killStreak < 3:
                            play_event_sound("PlayerKill")
                        if player_killStreak == 3:
                            play_event_sound("PlayerKillingSpree")
                        if player_killStreak == 4:
                            play_event_sound("PlayerRampage")
                        if player_killStreak == 5:
                            play_event_sound("PlayerUnstoppable")
                        if player_killStreak == 6:
                            play_event_sound("PlayerDominating")
                        if player_killStreak == 7:
                            play_event_sound("PlayerGodlike")
                        if player_killStreak > 7:
                            play_event_sound("PlayerLegendary")
                        player_killStreak += 1
                        #print(player_killStreak)
                        
                    # Ally got a kill.
                    elif event["KillerName"] in ally_team_players:
                        print ("Got an Enemy_Kill Event")
                        play_event_sound("AllyKill")
                    # Enemy got a kill.
                    elif event["KillerName"] in enemy_team_players:
                        # Player was killed.
                        if event["VictimName"] == player_name:
                            print ("Got an Player_Death Event")
                            play_event_sound("PlayerDeath")
                            player_killStreak = 0
                        # Ally was killed.
                        else:
                            play_event_sound("AllyDeath")
                    # Someone got executed.
                    else:
                        play_event_sound("Executed")
                # A team scored an ace.
                elif event_name == "Ace":
                    # Ally team scored an ace.
                    if event["AcingTeam"] == player_team:
                        play_event_sound("AllyAce")
                    # Enemy team scored an ace.
                    else:
                        play_event_sound("EnemyAce")
                # A turret was killed.
                elif event_name == "TurretKilled":
                    turret_name = event["TurretKilled"]
                    # Ally team got a turret kill.
                    if turret_name[7:9] == "T2" and player_team == "ORDER" or turret_name[7:9] == "T1" and player_team == "CHAOS":
                        play_event_sound("AllyTurretKill")
                    # Enemy team got a turret kill.
                    elif turret_name[7:9] == "T1" and player_team == "ORDER" or turret_name[7:9] == "T2" and player_team == "CHAOS":
                        play_event_sound("EnemyTurretKill")
                # A turret was killed.
                elif event_name == "InhibKilled":
                    inhib_name = event["InhibKilled"]
                    # Ally team got a turret kill.
                    if inhib_name[9:11] == "T2" and player_team == "ORDER" or inhib_name[9:11] == "T1" and player_team == "CHAOS":
                        play_event_sound("AllyInhibitorKill")
                    # Enemy team got a turret kill.
                    elif inhib_name[9:11] == "T1" and player_team == "ORDER" or inhib_name[9:11] == "T2" and player_team == "CHAOS":
                        play_event_sound("EnemyInhibitorKill")
                # An inhibitor is respawning soon.
                elif event_name == "InhibRespawningSoon":
                    inhib_name = event["InhibRespawningSoon"]
                    # Ally team's inhibitor is respawning soon.
                    if inhib_name[9:11] == "T1" and player_team == "ORDER" or inhib_name[9:11] == "T2" and player_team == "CHAOS":
                        play_event_sound("AllyInhibitorRespawningSoon")
                    # Enemy team's inhibitor is respawning soon.
                    elif inhib_name[9:11] == "T2" and player_team == "ORDER" or inhib_name[9:11] == "T1" and player_team == "CHAOS":
                        play_event_sound("EnemyInhibitorRespawningSoon")
                # An inhibitor has respawned.
                elif event_name == "InhibRespawned":
                    inhib_name = event["InhibRespawned"]
                    # Ally team's inhibitor has respawned.
                    if inhib_name[9:11] == "T1" and player_team == "ORDER" or inhib_name[9:11] == "T2" and player_team == "CHAOS":
                        play_event_sound("AllyInhibitorRespawned")
                    # Enemy team's inhibitor has respawned.
                    elif inhib_name[9:11] == "T2" and player_team == "ORDER" or inhib_name[9:11] == "T1" and player_team == "CHAOS":
                        play_event_sound("EnemyInhibitorRespawned")
                # Minions have spawned.
                elif event_name == "MinionsSpawning":
                    play_event_sound("MinionsSpawning")
                # Game has ended.
                elif event_name == "GameEnd":
                    # Victory
                    if event["Result"] == "Win":
                        play_event_sound("Victory")
                    # Defeat
                    elif event["Result"] == "Lose":
                        play_event_sound("Defeat")    
                # TODO: killing streaks

            previous_game_time = game_time
            previous_event_count = event_count
        except Exception as e:
            # Probably not in game or some other catastrophic error.
            print(e)
            log_file.write(repr(e) + "\n")
            log_file.flush()
            time.sleep(5)
            

if __name__ == '__main__':
    # GUI that shows a slider for sound volume control and a button for testing volume.
    gui = Tk()
    gui.geometry("250x100")
    gui.title("LoL Announcer")
    gui.protocol("WM_DELETE_WINDOW", close_script)
    volume_slider = Scale(gui, from_=0, to=100, orient=HORIZONTAL, command=update_volume)
    volume_slider.set(100)
    volume_slider.pack()
    Button(gui, text='Test volume', command=play_random_sound).pack()
    announcer_thread = threading.Thread(target=announcer_loop)
    announcer_thread.start()
    mainloop()

