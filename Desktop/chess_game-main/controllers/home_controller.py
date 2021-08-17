from models.tournament_model import Tournament
from views.home_view import HomeView
from controllers.player_controller import PlayerController
from controllers.Tournament_controller import TournamentController
from views.tournament_view import TournamentView
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


class HomeController(object):
    def __init__(self):
        # A la création du controleur, on peut le lier à son modèle et sa vue
        self.view = HomeView(self)
        self.player_controller = PlayerController(self.view)
        self.tournament_model = Tournament
        self.Tournament_controller = TournamentController(self.view)
        self.tournament_view = TournamentView(self)

    def display_home(self):
        """
        Permet l'affichage de la page de gestion des joueurs
        """
        return self.view.display_home()

    def go_to_menu(self, menu_option):
        """
        Fonction permettant de gérer la navigation entre les pages d'une vue

        [1]: Gérer les tournois\n
        [2]: Gérer les joueurs\n
        [3]: N/a\n
        [4]: N/a\n
        [X]: Sortir de l'application (pas encore implémenté)\n
        """
        if menu_option == "1":
            # Menu de gestion des tournois
            return self.Tournament_controller.display_home()
        elif menu_option == "2":
            # Menu de gestion des joueurs
            return self.player_controller.display_home()
        elif menu_option == "3":
            # Menu de gestion des tournées
            message = "Désolé, ce menu n'est pas encore implémenté !\
                       \nVeuillez réessayer : "
            return self.view.navigate_to_menu(message)
        elif menu_option == "4":
            message = "Désolé, ce menu n'est pas encore implémenté !\
                       \nVeuillez réessayer : "
            return self.view.navigate_to_menu(message)
        elif menu_option == "5":
            return self.tournament_view.generate_pairs("test")
        elif menu_option == "X":
            message = "Aurevoir !\n"
            sys.exit()
