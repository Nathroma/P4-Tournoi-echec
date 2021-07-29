import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


from models.player_model import Player
from views.home_view import HomeView
from views.player_view import PlayerView


class PlayerController(object):
    def index(self):
        self.view.launch()
        choice = input()
        if choice == '0':
            return self.parent_view.display_home()
        elif choice == '1':
            self.add_player()
        elif choice == '2':
            player_id = self.select_player()
            if player_id is not None:
                player = Player.get_player(player_id)
                self.edit_rank(player)
        return self.index()

    def __init__(self, parent_view):
        # A la création du controleur, on peut le lier à son modèle et sa vue
        self.model = Player
        self.view = PlayerView(self)
        self.parent_view = parent_view


    def save_player(self, player):
        new_player = self.model(player['nom'], player['prenom'], player['date_naissance'], player['sexe'])
        return new_player.save()


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
            all_players = self.model().get_all()
            return self.view.display_players_list(all_players)
        elif menu_option == "2":
            return self.view.display_create_player()
        elif menu_option == "3":
            message = "Désolé, ce menu n'est pas encore implémenté !\nVeuillez réessayer : "
            return self.view.navigate_to_menu(message)
        elif menu_option == "4":
            all_players = self.model().get_all()
            return self.view.display_erase_player(all_players)
        elif menu_option == "X":
            return self.view.display_home()
        elif menu_option == "Z":
            return self.parent_view.display_home()
    
    def get_all(self):
        return Player().get_all()
        


