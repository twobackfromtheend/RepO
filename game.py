from datetime import datetime
from typing import List, Tuple

MAPS = {
    "Stadium_P": "DFHStadium",
    "EuroStadium_P": "Mannfield",
    "cs_p": "ChampionsField",
    "TrainStation_P": "UrbanCentral",
    "Park_P": "BeckwithPark",
    "UtopiaStadium_P": "UtopiaColiseum",
    "wasteland_s_p": "Wasteland",
    "NeoTokyo_Standard_P": "NeoTokyo",
    "Underwater_P": "AquaDome",
    "arc_standard_p": "StarbaseArc",
    "farm_p": "Farmstead",
    "beach_P": "SaltyShores",
    "Stadium_Foggy_P": "DFHStadium_Stormy",
    "stadium_day_p": "DFHStadium_Day",
    "EuroStadium_Rainy_P": "Mannfield_Stormy",
    "EuroStadium_Night_P": "Mannfield_Night",
    "cs_day_p": "ChampionsField_Day",
    "Park_Rainy_P": "BeckwithPark_Stormy",
    "Park_Night_P": "BeckwithPark_Midnight",
    "TrainStation_Night_P": "UrbanCentral_Night",
    "TrainStation_Dawn_P": "UrbanCentral_Dawn",
    "UtopiaStadium_Dusk_P": "UtopiaColiseum_Dusk",
    "Stadium_Winter_P": "DFHStadium_Snowy",
    "eurostadium_snownight_p": "Mannfield_Snowy",
    "UtopiaStadium_Snow_P": "UtopiaColiseum_Snowy",
    "Wasteland_P": "Badlands",
    "Wasteland_Night_P": "Badlands_Night",
    "NeoTokyo_P": "TokyoUnderpass",
    "ARC_P": "Arctagon",
    "Labs_CirclePillars_P": "Pillars",
    "Labs_Cosmic_V4_P": "Cosmic",
    "Labs_DoubleGoal_V2_P": "DoubleGoal",
    "Labs_Octagon_02_P": "Octagon",
    "Labs_Underpass_P": "Underpass",
    "Labs_Utopia_P": "UtopiaRetro",
    "HoopsStadium_P": "Hoops_DunkHouse",
    "ShatterShot_P": "DropShot_Core707",
    "ThrowbackStadium_P": "ThrowbackStadium"
}


class Goal:
    def __init__(self, goal_dict: dict):
        self.player = goal_dict['PlayerName']
        self.team = goal_dict['PlayerTeam']
        self.frame = goal_dict['frame']

    def __str__(self):
        team = "B" if self.team == 0 else "O"
        return f"{team}: {self.player}"


class Player:
    def __init__(self, player_dict: dict):
        self.name = player_dict['Name']
        self.team = player_dict['Team']
        self.goals = player_dict['Goals']
        self.assists = player_dict['Assists']
        self.shots = player_dict['Shots']
        self.saves = player_dict['Saves']
        self.score = player_dict['Score']
        self.online_id = player_dict['OnlineID']


class Game:
    DATE_FORMATS = ['%Y-%m-%d %H-%M-%S', '%Y-%m-%d:%H-%M']

    def __init__(self, properties: dict):
        self.name = properties.get('ReplayName', "UNNAMED")
        self.score = properties.get('Team0Score', 0), properties.get('Team1Score', 0)
        self.map = properties['MapName']
        self.id = properties['Id']

        self.goals = [Goal(goal_dict) for goal_dict in properties.get('Goals', [])]

        self.players: Tuple[List[Player], List[Player]] = ([], [])
        for player_dict in properties.get('PlayerStats', []):
            player = Player(player_dict)
            self.players[player.team].append(player)

        self.date = None
        date_string = properties['Date']
        for date_format in self.DATE_FORMATS:
            try:
                self.date = datetime.strptime(date_string, date_format)
                break
            except ValueError:
                pass

        self.match_type = properties['MatchType']
        self.map = MAPS.get(properties['MapName'], f"UNKNOWN_{properties['MapName']}")

    def __str__(self):
        return f"Game ({self.name}) with {len(self.players)} players: {[player.name for player in self.players]}"
