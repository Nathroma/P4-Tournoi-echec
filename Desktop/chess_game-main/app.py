from models.player_model import Player
from models.tournament_model import Tournament
from controllers.player_controller import PlayerController
from controllers.home_controller import HomeController
from controllers.Tournament_controller import TournamentController
from views.player_view import PlayerView
from views.home_view import HomeView
from views.tournament_view import TournamentView



def main():
    """
    Main function of the program
    """

    home_controller = HomeController()
    home_controller.display_home()







    # 1. Display the list of possible actions to the user




main()


