from controllers.player_controller import PlayerController
from tinydb import TinyDB


class TournamentView:

    def __init__(self, controller):
        self.controller = controller
        self.db = TinyDB('db.json')

    def navigate_to_menu(self, message):
        """
        Cette fonction permet de récupérer l'option saisie
        par un utilisateur et ensuited'utiliser de naviger
        vers le menu correspondant à cette
        """
        # On récupère l'option saisie par le client
        # La récupération de l'option doit être améliorée pour gérer les cas
        # d'erreur de saisie
        option = input(message)
        # Une fois qu'on a récupéré l'option, on navigue vers la page suggérée
        self.controller.go_to_menu(option)

    def display_home(self):
        """
        Affiche les options pour gérer les joueurs
        """
        message = """
        Ce menu permet de gérer les tournois de l'application\n
        Voici les actions possibles depuis ce menu : \n
        [1]: Liste des tournois\n
        [2]: Ajouter un nouveau tournoi\n
        [3]: Générer un match\n
        [4]: Afficher les scores d'un tournoi terminé\n
        [0]: Retourner au menu parent\n
        [Z]: Sortir de l'application\n
        """
        self.navigate_to_menu(message)

    def display_tournaments_list(self, tournaments_list):
        """
        Todo: Affiche la liste de tournoi avec des numeros
        """
        number_tournament = 1
        message = "tournoi n°"

        if len(tournaments_list) == 0:
            message = "La liste de tournoi est vide !\n"

        for tournament in tournaments_list:
            message += str(number_tournament) + " " + tournament.__str__()\
                + '\n'
            number_tournament += 1

        message += """
        Vous pouvez retourner au menu de gestion des tournoi en saisissant
        l'option 0\nOu bien vous pouvez sortir du programme en saisissant
        l'option X\n
        """

        self.navigate_to_menu(message)

    def choose_tournament_list(self, tournaments_list):
        """
        Todo: Affiche la liste de tournoi pour selection
        """
        print('Choisissez le tournoi à afficher\n')
        nb = 0
        for i in tournaments_list:
            print('Tournoi n°' + str(nb + 1) + " : " +
                  str(tournaments_list[nb]) + '\n')
            nb += 1

    def display_create_tournament(self):
        """
        Todo: Affiche le menu de création d'un tournoi
        """
        message = "Vueillez entrer les informations du nouveau tournoi : \n"
        print(message)
        reference = input("\nVeuillez entrer une référence : ")
        date_début = input("\nVeuillez entrer la date de début : ")
        date_fin = input("\nVeuillez entrer la date de fin : ")
        nombre_tour = input("\nVeuillez entrer le nombre de tours\
                            (4 par défaut) : ")
        description = input("\nVeuillez entrer une description : ")

        tournament = {
            "reference": reference,
            "date_debut": date_début,
            "date_fin": date_fin,
            "nombre_tour": nombre_tour,
            "description": description
        }

        result = self.controller.save_tournament(tournament)

        if result == {}:
            print("Une erreur s'est produite lors de l'enregistrement\
                    du tournoi !")
        message = """Le tournoi a bien été créé et sauvegardé en base
                    de données\n
                    Vous pouvez retourner au menu de gestion des tournoi
                    en saisissant l'option 0\n
                    Ou bien vous pouvez sortir du programme en saisissant
                    l'option X\n"""
        self.navigate_to_menu(message)

    def add_player_to_tournament(self):
        # 1. Afficher le message de la vue : Veuillez choisir le joueur à
        # ajouter au tournois
        print('Choisisser les joueurs à ajouter :\n')

        # 2. Récupérer la liste des joueurs au niveau du contrôler
        list_players = PlayerController.get_all(self)

        # 3. Afficher la liste des joueurs récupérée
        if len(self.controller.get_players_in()) > 0:
            print("Il y a déja ",
                  str(len(self.controller.get_players_in())),
                  " joueur(s)",
                  "Ajoutez-en encore ",
                  str((2 * int(self.controller.get_tournament()
                      ["nombre_tour"])) -
                      len(self.controller.get_players_in())))
        elif len(self.controller.get_players_in()) == 0:
            print("Il n'y a aucun joueur, ajoutez-en au moins 2\n")
        player_number = 1
        for player in list_players:
            print(str(player_number) + ') ' + player['nom'], player['prenom'] +
                  '  [', str(player['classement']) + ' ]')
            player_number += 1

        # 4. Demander à l’utilisateur le joueur à afficher
        print("\nSelectionnez le joueur à ajouter")

    def scoring_menu(self):
        """
        Todo: Affiche tous les matches pour ajouter les scores
        """
        list_joueurs = self.controller.get_list_players_in_match()
        nb = 0
        print('Selectionnez le match pour y entrer les scores : \n')
        print('    [0] revenir au menu précedent')
        for match in list_joueurs:
            print('Match n°' + str(nb + 1) + ' : ' + str(list_joueurs[nb]))
            nb += 1

    def scoring_match(self, player_one, player_two):
        """
        Todo: Affiche les possibilités de choix du gagnant
        """
        print(str(player_one) + "  :  " + str(player_two))
        print(
            'Choisissez le resultat du match :',
            '    [0] Retour',
            '    [1] Gagnant : ' + str(player_one),
            '    [2] Gagnant : ' + str(player_two),
            '    [3] Egalité',
            '    [4] Annulé',
            sep='\n'
        )

    @staticmethod
    def ask_continue():
        print('\nSelectionnez [0] pour continuer')

    def manage_tournament(self):
        """
        Todo: Affiche les menus du Round en cours
        """
        matches = self.controller.get_matches()
        players = self.controller.get_players_in()
        print('\n     Menu du tournoi :\n\n')
        print('   [0] Retour')
        print('   [1] Ajouter les joueurs')
        if (len(matches) < 1) and (len(players) > 1):
            print('   [2] Générer les matches')
        elif len(matches) > 0:
            print('   [3] Entrer les scores')
