import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


from models.tournament_model import Tournament
from views.home_view import HomeView
from views.tournament_view import TournamentView
from models.player_model import Player
from models.round_model import Round   
from models.match_model import Match

class TournamentController(object):
    
    def __init__(self, parent_view):
        # A la création du controleur, on peut le lier à son modèle et sa vue
        self.model = Tournament
        self.view = TournamentView(self)
        self.parent_view = parent_view

    def save_tournament(self, tournament):
        new_tournament = self.model(tournament['reference'], tournament['date_début'],
                tournament['date_fin'], tournament['description'])
        print('saving...')
        return new_tournament.save()

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
            all_tournaments = self.model().get_all_tournament()
            return self.view.display_tournaments_list(all_tournaments)
        elif menu_option == "2":
            return self.view.display_create_tournament()
        elif menu_option == "3":
            message = "Désolé, ce menu n'est pas encore implémenté !\nVeuillez réessayer : "
            return self.view.navigate_to_menu(message)
        elif menu_option == "4":
            return Tournament().generate_matches() 
        elif menu_option == "5":
            all_lists = self.model.get_lists()
            return self.view.generate_pairs(all_lists)
        elif menu_option == "X":
            return self.view.display_home()
        elif menu_option == "Z":
            return self.parent_view.display_home()

    def score(self, tournament: Tournament, round: Round, match: Match):
        TournamentView.result_menu(match)
        choice = input()
        if choice == '0':  # back last Menu
            return self.match_index(tournament, round)
        if choice == '1':
            match.set_result(1, 0)
        elif choice == '2':
            match.set_result(0, 1)
        elif choice == '3':
            match.set_result(0.5, 0.5)
        elif choice == '4':
            match.set_result(0, 0)
        else:
            return self.score(tournament, round, match)

        tournament.update_players_score()
        return self.match_index(tournament, round)

    def update_players_score(self):
        for player in self.players:
            score = 0
            for round in self.rounds:
                for match in round.matches:
                    if player[0] == match.result[0][0]:
                        score += match.result[0][1]
                    if player[0] == match.result[1][0]:
                        score += match.result[1][1]
            player[1] = score

    def leaderboard(self, tournament):
        for player in tournament.get_suisse_sorted_players():
            print('[{}]'.format(player[1]), Player.get_player(player[0]))
        