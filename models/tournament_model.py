from tinydb import TinyDB, Query

from models.match_model import Match
from models.player_model import Player
from models.round_model import Round

class Tournament:
    class Decorators(object):
        @classmethod
        def to_db(cls, func):
            def save_into_db(*args, **kwargs):
                func(*args, **kwargs)
                serialized_tournament = [
                    tournament.serialize()
                    for tournament in Tournament.tournaments_list
                ]
                db = TinyDB('db.json')
                tournaments_table = db.table('tournaments')
                tournaments_table.truncate()
                tournaments_table.insert_multiple(serialized_tournament)

            return save_into_db

    tournaments_list = []

    def __init__(self, reference="", date_début="", date_fin="",
                    nombre_tour=4, description=""):
        self.reference = reference
        self.date_début = date_début
        self.date_fin = date_fin
        self.nombre_tour = nombre_tour
        self.description = description
        self.rounds = []
        self.players = []
        self.db = TinyDB('db.json')
        self.type = "tournoi"
    
    def __str__(self):
        return self.reference + ' - ' + self.date_début + ' - ' + self.date_fin + \
            ' - ' + self.description

    def save(self):
        """
        Todo: Se connecter à la BD et enregistrer le joueur
        """
        # 1. on crée un objet Joueur
        tournament = {
            "reference": self.reference,
            "date_début": self.date_début,
            "date_fin": self.date_fin,
            "nombre_tour": self.nombre_tour,
            "description": self.description,
            "type": self.type
        }

        # 2. On enregistre l'objet joueur
        return self.db.insert(tournament)
    
    def get_suisse_sorted_players(self):
        """ Affiche la liste des joueurs du tournoi
        par le le score et le rang puis renvoie la liste
        """
        s = sorted(
            self.players,
            key=lambda player: int(Player.get_player(player[0]).classement),
            reverse=True
        )  # sort by rank
        return sorted(
            s,
            key=lambda player: float(player[1]),
            reverse=True
        )  # then sort by score

    def create_round(self):
        round_name = 'Round' + str(len(self.rounds) + 1)
        round = Round(round_name)
        self.rounds.append(round)
        return round

    def get_all_tournament(self):
        """
        Todo: Se connecter à la base de données et récupérer tous les joueurs 
        """
        return self.db.search(Query().type == "tournoi")

    def generate_matches(self):
        """ Choisis les joueurs
        créer des matches en fonction du nombre de round :
        Si il y a 8 joueurs:
            Dans le premier round:
                Le joueur 1 affronte le joueur 5,
                Le joueur 2 affronte le joueur 6,
                etc
            Dans le cas d'un autre round:
                Le joueurs 1 affronte le joueur 2
                (sauf si ils ont déja joué, 
                    alors : joueur 1 VS joueur 3)
                Joueur 3 VS Joueur 4
                etc
        """
        list_of_matches = []
        round = self.create_round()
        players = self.get_suisse_sorted_players()
        if len(self.rounds) == 1:
            for i in range(self.nombre_tour):
                match = Match(players[i][0], players[i + self.nombre_tour][0])
                list_of_matches.append(match)
        else:
            while len(players) > 1:
                y = 1
                while self.played_against(players[0][0], players[y][0]):
                    y += 1
                match = Match(players[0][0], players[y][0])
                list_of_matches.append(match)
                del players[y]
                del players[0]
        round.add_matches(list_of_matches)
    
    def played_against(self, player_one, player_two):
        opposition = []
        for round in self.rounds:
            for match in round.matches:
                opposition.append([match.result[0][0], match.result[1][0]])
    
    def create_round(self):
        round_name = 'Round' + str(len(self.rounds) + 1)
        round = Round(round_name)
        self.rounds.append(round)
        return round
    
    def add_matches(self, list_of_matches: list):
        for match in list_of_matches:
            self.list_of_matches.append(match)