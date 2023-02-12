import sys
import os
import json
import time
import datetime

from pypresence import Presence
import pyrez.models
from pyrez.api import PaladinsAPI
from pyrez.enumerations import Format, Endpoint

from CLI import *

#CONST
DISCORD_APP = '678959295374688296'
UPDATE_TIME = 5

#GLOBAL
TIME, TIME_ONLINE = 0, 0

class PaladinsAPI_fixed(PaladinsAPI):
    def __init__(self, devId, authKey, responseFormat=Format.JSON, sessionId=None, storeSession=True):
        self.maindir = os.path.dirname(os.path.abspath(__file__))
        super().__init__(devId, authKey, responseFormat, sessionId, storeSession)
        self.endpoint = Endpoint.PALADINS
        self.debug_mode = False
    def _getSession(cls, idOnly=True, devId=None):
        try:
            with open("{}/{}.json".format(cls.maindir, devId or cls.devId), 'r', encoding="utf-8") as f:
                session = pyrez.models.Session(**json.load(f))
                return session.sessionId if idOnly else session
        except (FileNotFoundError, ValueError):
            return None
    def _API__setSession(self, session, devId=None):
        self.sessionId = session.sessionId
        if self.storeSession and session:
            with open('{}/{}.json'.format(self.maindir, devId or self.devId), 'w', encoding='utf-8') as f:
                f.write(json.dumps(session.json, sort_keys=True, ensure_ascii=True, indent=4))


#Helpful functions
def delete_lines(lines=1):
    while lines > 0:
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')
        lines -= 1


def sleep(text):
    print(text)
    while True:
        time.sleep(60)


def map_rename_ru(name) -> str:
    map_name = ''
    for _ in HD.map_names:
        if _ in name:
            map_name += HD.map_names[_]
    if map_name != '':
        map_mode = ''
        for mode in HD.gamemode_names:
            if mode in name:
                map_mode = HD.gamemode_names[mode]
        if map_mode == '':
            map_mode = 'Казуал'
        return f"{map_name} ({map_mode})"
    else:
        return name.replace("LIVE ", "")


#Prepare functions
def first_prepare():
    global SETTINGS, CLI
    print("[1/4] Trying to read settings.json.")
    try:
        with open('settings.json') as data:
            SETTINGS = json.load(data)
    except FileNotFoundError:
        delete_lines(1)
        print("[1/4] Failed to read settings.json")
        sleep(text="App will not continue work.")
    else:
        delete_lines(1)
        CLI = CL_Interface(lang=SETTINGS['Language'] if SETTINGS['Language'] else 'EN', playername=SETTINGS['Account'])
        CLI.messaging(1, 'read_settings', 'finish')


def api_connect() -> list:
    global API
    try:
        API = PaladinsAPI_fixed(devId=int(SETTINGS['Access']['devid']), authKey=SETTINGS['Access']['authkey'])
        session = API._createSession()
    except ValueError:
        return [False, 1, 'error_value']
    except (pyrez.exceptions.InvalidArgument, pyrez.exceptions.IdOrAuthEmpty, UnboundLocalError):
        return [False, 2, 'error']
    else:
        return [True, 1, 'finish']


def search_player() -> list:
    global PLAYER_ID
    try:
        PLAYER_ID = API.getPlayerId(playerName=SETTINGS["Account"], portalId=None, xboxOrSwitch=False)[0]
    except IndexError:
        return [False, 1, 'error']
    else:
        return [True, 1, 'finish']


def presence_connect() -> list:
    global RICHPRESENCE
    try:
        RICHPRESENCE = Presence(DISCORD_APP)
        RICHPRESENCE.connect()
    except:
        return [False, 1, 'error']
    else:
        return [True, 1, 'finish']


list_to_prepare = {
        2: ['api_connect', api_connect],
        3: ['searching_player', search_player],
        4: ['rich_presence_connect', presence_connect]
    }

#Active phase functions
def get_player_status() -> list:
    Status_Request = API.getPlayerStatus(playerId=PLAYER_ID["player_id"])
    return [Status_Request["status"], Status_Request["Match"]]


def get_player_activity(match_id):
    Match_Info = API.getMatch(matchId=match_id, isLiveMatch=True)
    for player in Match_Info:
        if int(player["playerId"]) == PLAYER_ID["player_id"]:
            if player["mapGame"] == "LIVE Shooting Range Local":
                image = "target"
                champion = "Undefined champion"
            else:
                image = str((player["ChampionName"]).lower()).replace("'", "")
                champion = player["ChampionName"]
            if SETTINGS["Language"].upper == 'RU':
                return [image,
                        map_rename_ru(player["mapGame"]),
                        HD.champion_names[champion] if champion in HD.champion_names else champion,
                        player["Mastery_Level"]]
            else:
                return [image,
                        str(player["mapGame"]).replace("LIVE ", ""),
                        champion,
                        player["Mastery_Level"]]
    return None


def get_player_info() -> list:
    Player_Info = API.getPlayer(player=SETTINGS["Account"])
    return [Player_Info["Title"],
            Player_Info["Level"],
            Player_Info["HoursPlayed"],
            HD.rank_names[max(Player_Info["Tier_RankedKBM"], Player_Info["Tier_RankedController"])]]


if __name__ == '__main__':
    first_prepare()

    if SETTINGS['Language'].upper() == 'RU':
        import helpful_dicts_ru as HD
    else:
        import helpful_dicts as HD

    for step in range(2, 5):
        CLI.messaging(step, list_to_prepare[step][0], 'start')
        process = list_to_prepare[step][1]()

        delete_lines(process[1])
        if process[0]:
            CLI.messaging(step, list_to_prepare[step][0], 'finish')
        else:
            CLI.messaging(step, list_to_prepare[step][0], process[2])
            sleep(text=CLI.text["sleep_text"])

    if UPDATE_TIME < 3:
        UPDATE_TIME = 3

    while True:
        TIME += UPDATE_TIME
        Status = get_player_status()
        Info = get_player_info()
        if Status[0] == 1:
            TIME_ONLINE += UPDATE_TIME
            Text = SETTINGS['Discord']['idle']
            Data = None
        elif Status[0] == 2:
            TIME_ONLINE += UPDATE_TIME
            Text = SETTINGS['Discord']['choose_phase']
            Data = None
        elif Status[0] == 3:
            TIME_ONLINE += UPDATE_TIME
            Text = SETTINGS['Discord']['in_match']
            Data = get_player_activity(Status[1])
        else:
            TIME_ONLINE = 0
            Text = SETTINGS['Discord']['offline']
            Data = None
        namespaces = {'player': SETTINGS['Account'],
                      'time_rich_presence': datetime.timedelta(seconds=round(TIME)),
                      'time': datetime.timedelta(seconds=round(TIME_ONLINE)),
                      'map': Data[1] if Data else "Unknown",
                      'champion': Data[2] if Data else "Unknown",
                      'mastery': Data[3] if Data else "Unknown",
                      'title': Info[0],
                      'account_level': Info[1],
                      'total_hours': Info[2],
                      'rank': Info[3]}
        RICHPRESENCE.update(state=Text['bottom_text'].format(**namespaces),
                            details=Text['upper_text'].format(**namespaces),
                            large_image=Data[0] if Data else "p",
                            small_image="p",
                            large_text=Text['image_text'].format(**namespaces))
        delete_lines(CLI.Lines if CLI.ActivePhase else 0)
        CLI.print_cli(Status[0], namespaces)
        time.sleep(UPDATE_TIME)