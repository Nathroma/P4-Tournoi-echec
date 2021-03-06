from tinydb import TinyDB, Query


class Player(object):
    players_list = []

    def __init__(self, nom="", prenom="", date_naissance="", sexe=""):
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.sexe = sexe
        self.classement = 0
        self.db = TinyDB('db.json')
        self.type = "player"

    def __str__(self):
        return self.nom + ' - ' + self.prenom + ' - ' + self.date_naissance + \
            ' - ' + self.sexe + ' - ' + self.classement

    def save(self):
        """
        Todo: Se connecter à la BD et enregistrer le joueur
        """
        # 1. on crée un objet Joueur
        player = {
            "nom": self.nom,
            "prenom": self.prenom,
            "date_naissance": self.date_naissance,
            "sexe": self.sexe,
            "classement": self.classement,
            "type": self.type
        }

        # 2. On enregistre l'objet joueur
        return self.db.insert(player)

    def get_all(self):
        """
        Todo: Se connecter à la base de données et récupérer tous les joueurs
        """
        return self.db.search(Query().type == "player")

    @classmethod
    def get_player(cls, ref):
        cls.players_list = Player().db.search(Query().type == "player")
        return cls.players_list[ref]

    @classmethod
    def save_all_to_db(cls):
        serialized_players = \
            [player.serialize() for player in cls.players_list]
        db = TinyDB('db.json')
        players_table = db.table('players')
        players_table.truncate()
        players_table.insert_multiple(serialized_players)
