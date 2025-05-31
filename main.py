import requests
import json
from typing import (
    List,
    Dict,
    Set,
    Tuple
)

class Sportik:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.headers = {'Authorization': token}
    
    def get_matches(self) -> List[Dict]:
        response = requests.get(f"{self.base_url}/matches", headers=self.headers)
        return response.json()
    
    def get_teams(self) -> List[Dict]:
        response = requests.get(f"{self.base_url}/teams", headers=self.headers)
        return response.json()
    
    def get_team(self, team_id: int) -> Dict:
        response = requests.get(f"{self.base_url}/teams/{team_id}", headers=self.headers)
        return response.json()
    
    def get_player(self, player_id: int) -> Dict:
        response = requests.get(f"{self.base_url}/players/{player_id}", headers=self.headers)
        return response.json()


def process_requests() -> None:
    BASE_URL = "https://lksh-enter.ru"
    TOKEN = input("Введите ваш plain-token: ")
    
    api = Sportik(BASE_URL, TOKEN)
    
    try:
        matches = api.get_matches()
        teams = api.get_teams()

        team_info = {team['id']: team for team in teams}
        print(team_info)
        team_name_to_id = {team['name']: team['id'] for team in teams}

        all_players = set()
        for team in teams:
            for player_id in team['players']:
                all_players.add(player_id)

        players_info = {}
        for player_id in all_players:
            print(player_id)
            player = api.get_player(player_id)
            full_name = f"{player.get('name', '')} {player.get('surname', '')}".strip()
            players_info[player_id] = full_name

        sorted_players = sorted(players_info.values(), key=lambda x: x.lower())
        for player in sorted_players:
            print(player)

        while True:
            try:
                request = input().strip()
                if not request:
                    continue
                
                if request.startswith("stats? "):
                    parts = request.split('"')
                    if len(parts) < 2:
                        print("0 0 0")
                        continue
                    
                    team_name = parts[1]
                    if team_name not in team_name_to_id:
                        print("0 0 0")
                        continue
                    
                    team_id = team_name_to_id[team_name]
                    wins = 0
                    losses = 0
                    goal_diff = 0
                    
                    for match in matches:
                        if match['team1'] == team_id:
                            goal_diff += match['team1_score'] - match['team2_score']
                            if match['team1_score'] > match['team2_score']:
                                wins += 1
                            elif match['team1_score'] < match['team2_score']:
                                losses += 1
                        elif match['team2'] == team_id:
                            goal_diff += match['team2_score'] - match['team1_score']
                            if match['team2_score'] > match['team1_score']:
                                wins += 1
                            elif match['team2_score'] < match['team1_score']:
                                losses += 1
                    
                    print(f"{wins} {losses} {goal_diff:+d}".replace("+", "+").replace("-", "-"))
                elif request.startswith("versus? "):
                    parts = request.split()
                    if len(parts) != 3:
                        print("0")
                        continue
                    
                    try:
                        player1_id = int(parts[1])
                        player2_id = int(parts[2])
                    except ValueError:
                        print("0")
                        continue

                    if player1_id not in players_info or player2_id not in players_info:
                        print("0")
                        continue

                    player1_teams = set()
                    player2_teams = set()
                    
                    for team in teams:
                        if player1_id in team['players']:
                            player1_teams.add(team['id'])
                        if player2_id in team['players']:
                            player2_teams.add(team['id'])

                    count = 0
                    for match in matches:
                        if (match['team1'] in player1_teams and match['team2'] in player2_teams) or \
                           (match['team1'] in player2_teams and match['team2'] in player1_teams):
                            count += 1
                    
                    print(count)
                else:
                    continue
                    
            except EOFError:
                break
            except Exception as e:
                print(f"Ошибка при обработке запроса: {e}")
                continue
    
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    process_requests()
