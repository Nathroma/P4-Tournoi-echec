from models.tournament_model import Tournament
from views.tournament_view import TournamentView
from models.player_model import Player
from controllers.player_controller import PlayerController
from models.match_model import Match
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


class TournamentController(object):

    def __init__(self, parent_view):
        # A la création du controleur, on peut le lier à son modèle et sa vue
        self.model = Tournament()
        self.view = TournamentView(self)
        self.parent_view = parent_view
        self.players_list = []

    def save_tournament(self, tournament):
        tournament = self.model.create_tournament(tournament['reference'],
                                                  tournament['date_debut'],
                                                  tournament['date_fin'],
                                                  tournament['nombre_tour'],
                                                  tournament['description'])
        return tournament.save()

    def display_home(self):
        """
        Permet l'affichage de la page de gestion des joueurs
        """
        return self.view.display_home()

    def go_to_menu(self, menu_option):
        """
        Fonction permettant de gérer la navigation entre les pages d'une vue
        """
        if menu_option == "0":
            return self.parent_view.display_home()
        elif menu_option == "1":
            all_tournaments = self.model.get_all_tournament()
            return self.view.display_tournaments_list(all_tournaments)
        elif menu_option == "2":
            return self.view.display_create_tournament()
        elif menu_option == "3":
            return self.menu_manage_tournament()
        elif menu_option == "4":
            return self.display_results()
        elif menu_option == "X":
            return self.view.display_home()
        elif menu_option == "Z":
            return self.parent_view.display_home()
        else:
            print('Choix invalide')

    def menu_manage_tournament(self):
        self.view.manage_tournament()
        option = int(input())
        if option == 0:
            return self.parent_view.display_home()
        elif option == 1:
            self.add_player_to_tournament()
            return self.menu_manage_tournament()
        elif option == 2:
            self.model.generate_matches()
            return self.menu_manage_tournament()
        elif option == 3:
            return self.match_index()
        else:
            print('Valeur incorrect !')
            return self.menu_manage_tournament()

    def score(self, match: Match, player_one, player_two):
        """
        Todo: ajoute les scores au joueur gagnant
        """
        option = int(input())
        if option == 0:  # retour menu précédent
            return self.match_index()
        if option == 1:
            match.set_result(1, 0)
        elif option == 2:
            match.set_result(0, 1)
        elif option == 3:
            match.set_result(0.5, 0.5)
        elif option == 4:
            match.set_result(0, 0)
        else:
            return self.score()

        self.model.results_matches.append(match.resultat())
        # self.update_score(match, player_one, player_two)
        return self.match_index()

    def display_results(self):
        tournaments_list = self.model.get_all_tournament()
        self.view.choose_tournament_list(tournaments_list)
        option = int(input())
        option -= 1
        list_results = self.get_results()
        nb = 0
        print('Liste des resultats :\n')
        for score in list_results:
            print('Match n°' + str(nb) + ' : ' + str(list_results[nb]))
            nb += 1

        self.view.ask_continue()
        choice = int(input())
        if choice == 0:
            return self.display_home()
        else:
            return self.display_home()

    def match_index(self):
        # 1) récuperer la liste des matches
        list_joueurs = self.model.list_of_matches

        # 2) pour chaque match afficher les 2 joueurs
        self.view.scoring_menu()

        # 3) Slectionner le match à scorer
        option = int(input())
        option -= 1
        if option == -1:
            return self.display_home()
        else:
            player_one = list_joueurs[option].player_one
            player_two = list_joueurs[option].player_two

        # 4) entrer le resultat du match (Gagnant, perdant, égalité)
        self.view.scoring_match(player_one, player_two)

        # 4) Ajouter les scores aux joueurs
        return self.score(list_joueurs[option], player_one, player_two)

    def get_list_players_in_match(self):
        return self.model.list_of_matches

    def get_players_in(self):
        return self.model.players_in

    def get_tournament(self):
        return self.model.tournaments_list[0]

    def get_player_list(self):
        self.players_list = Player.get_player()
        return self.players_list

    def get_matches(self):
        return self.model.list_of_matches

    def get_results(self):
        return self.model.results_matches

    def add_player_to_tournament(self):
        tournament = self.model.get_tournament()
        while len(self.model.players_in) < 2 * int(tournament["nombre_tour"]):
            self.view.add_player_to_tournament()

            choosen_player = int(input())
            choosen_player -= 1
            list_players = PlayerController.get_all(self)

            if choosen_player in range(0, len(list_players)):
                self.model.players_in.append(list_players[choosen_player])

            elif choosen_player not in range(0, len(list_players)):
                print("Valeur incorrect !")

    def ask_continue(self):
        self.view.ask_continue()
        option = int(input())

        if option == 0:
            return self.view.display_create_tournament()
        elif option == 1:
            return self.match_index()
        else:
            print('Valeur incorrect !')
            return self.ask_continue()
