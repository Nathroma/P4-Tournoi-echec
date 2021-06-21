class Tournament:

    tournaments_list = []

    def __init__(self, reference="", date_début="", date_fin="", description=""):
        self.reference = reference
        self.date_début = date_début
        self.date_fin = date_fin
        self.description = description

    def save(self):
        """
        Todo: Se connecter à la BD et enregistrer le joueur
        """
        # 1. on crée un objet Joueur
        tournament = {
            "reference": self.reference,
            "date_début": self.date_début,
            "date_fin": self.date_fin,
            "description": self.description,
        }

        # 2. On enregistre l'objet joueur
        self.tournaments_list.append(tournament)
        return tournament
        