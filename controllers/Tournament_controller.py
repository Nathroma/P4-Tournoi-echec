import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


from models.tournament_model import Tournament
from views.home_view import HomeView
from views.tournament_view import TournamentView

class TournamentController(object):
    def __init__(self, parent_view):
        # A la création du controleur, on peut le lier à son modèle et sa vue
        self.model = Tournament()
        self.view = TournamentView(self)
        self.parent_view = parent_view

    def save_tournament(self, tournament):
        new_tournament = self.model(tournament.reference, tournament.date_début, tournament.date_fin, tournament.description)
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
            return self.view.display_create_tournament()
        elif menu_option == "3":
            message = "Désolé, ce menu n'est pas encore implémenté !\nVeuillez réessayer : "
            return self.view.navigate_to_menu(message)
        elif menu_option == "4":
            message = "Désolé, ce menu n'est pas encore implémenté !\nVeuillez réessayer : "
            return self.view.navigate_to_menu(message)
        elif menu_option == "X":
            return self.view.display_home()
        elif menu_option == "Z":
            return self.parent_view.display_home()