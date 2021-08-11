from tinydb import TinyDB, Query

from models.match_model import Match
from models.player_model import Player
from models.round_model import Round

class Tournament:
    tournaments_list = []


    def __init__(self, reference="", date_début="", date_fin="",
                    nombre_tour=4, description=""):
        self.reference = reference
        self.date_début = date_début
        self.date_fin = date_fin
        self.nombre_tour = nombre_tour
        self.description = str(description)
        self.rounds = []
        self.players_in = []
        self.players = []
        self.list_of_matches = []
        self.results_matches = []
        self.db = TinyDB('db.json')
        self.type = "tournoi"
    
    def create_tournament(self, tournament):
        new_tournament = (tournament['reference'], tournament['date_début'],
                tournament['date_fin'], tournament['description'])
        return new_tournament

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
        
        round = self.create_round()
        players_in_short = self.players_trunc()
        if len(self.rounds) == 1:
            for i in range(self.nombre_tour):
                match = Match(players_in_short[i], players_in_short[i + self.nombre_tour])
                print(match)
                self.list_of_matches.append(match)
        else:
            while len(players_in_short) > 1:
                y = 1
                while self.played_against(players_in_short[0], players_in_short[y]):
                    y += 1
                match = Match(players_in_short[0], players_in_short[y])
                self.list_of_matches.append(match)
                del players_in_short[y]
                del players_in_short[0]
        round.add_matches(self.list_of_matches)
    

    def players_trunc(self):
        players_in_short = []
        for i in range(len(self.players_in)) :
            player_raw = self.players_in[i]
            player_tr = player_raw["nom"],player_raw["prenom"]
            players_in_short.append(player_tr)
        return players_in_short

    
    def create_round(self):
        round_name = 'Round' + str(len(self.rounds) + 1)
        round = Round(round_name)
        self.rounds.append(round)
        return round

    
    def add_matches(self, list_of_matches: list):
        for match in list_of_matches:
            self.list_of_matches.append(match)


    def get_tournament(self):
        self.tournaments_list = Tournament().db.search(Query().type == "tournoi")
        return self.tournaments_list[0]
   
