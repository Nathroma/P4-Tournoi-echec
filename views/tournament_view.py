from random import randint
from tinydb import Query, TinyDB

class TournamentView:

    def __init__(self, controller):
        self.controller = controller
        self.db = TinyDB('db.json')

    def navigate_to_menu(self, message):
        """
        Cette fonction permet de récupérer l'option saisie par un utilisateur et ensuite
        d'utiliser de naviger vers le menu correspondant à cette
        """
        # On récupère l'option saisie par le client
        # La récupération de l'option doit être améliorée pour gérer les cas d'erreur de saisie
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
        [4]: Générer un match\n
        [0]: Retourner au menu parent (pas encore implémenté)\n
        [X]: Aller au menu précédent (pas encore implémenté)\n
        [Z]: Sortir de l'application (pas encore implémenté)\n
        """
        self.navigate_to_menu(message)

    def display_tournaments_list(self, tournaments_list):
        """
        Affiche la liste de tournoi
        """
        number_tournament = 1
        message = "tournoi n°"

        if len(tournaments_list) == 0:
            message = "La liste de tournoi est vide !\n"    

        for tournament in tournaments_list:
            message += str(number_tournament) + " " + tournament.__str__() + '\n'
            number_tournament += 1

        message += """
        Vous pouvez retourner au menu de gestion des tournoi en saisissant l'option 0\n
        Ou bien vous pouvez sortir du programme en saisissant l'option X\n
        """
        
        self.navigate_to_menu(message)
    
    def display_create_tournament(self):
        """
        Affiche le menu de création d'un tournoi
        """
        message = "Vueillez entrer les informations du nouveau tournoi : \n"
        print(message)
        reference = input("\nVeuillez entrer une référence : ")
        date_début = input("\nVeuillez entrer la date de début : ")
        date_fin = input("\nVeuillez entrer la date de fin : ")
        nombre_tour = input("\nVeuillez entrer le nombre de tours (4 par défaut) : ")
        description = input("\nVeuillez entrer une description : ")

        tournament = {
            "reference": reference,
            "date_début": date_début,
            "date_fin": date_fin,
            "nombre_tour": nombre_tour,
            "description": description
        }

        result = self.controller.save_tournament(tournament)

        if result == {}:
            print("Une erreur s'est produite lors de l'enregistrement du tournoi !")
        
        message = """Le tournoi a bien été créé et sauvegardé en base de données\n
                Vous pouvez retourner au menu de gestion des tournoi en saisissant l'option 0\n
                Ou bien vous pouvez sortir du programme en saisissant l'option X\n""" 
        
        self.navigate_to_menu(message)
    
    @staticmethod
    def result_menu(match):
        print(
            'Choisissez le resultat du match :',
            '    [0] Retour',
            '    [1] Gagnant : ' + match.get_player_name(match.player_one),
            '    [2] Gagnant : ' + match.get_player_name(match.player_two),
            '    [3] Egalité',
            '    [4] Annulé',
            sep='\n'
        )

    @staticmethod
    def scoring_menu(round):
        print(
            '----------------------------------------------------',
            'Score du match : ' + round.name,
            '----------------------------------------------------',
            'Choisissez le match :',
            '    [0] Retour',
            sep='\n'
        )
        for i, match in enumerate(round.list_of_matches, start=1):
            print('    [' + str(i) + '] ' + match.result_to_string())
