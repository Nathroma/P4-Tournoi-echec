from models.player_model import Player


class Match:
    def __init__(self, player_one_id, player_two_id, score_one=0, score_two=0):
        self.player_one = player_one_id
        self.player_two = player_two_id
        self.score_one = score_one
        self.score_two = score_two

    def __str__(self):
        return 'J1 :  ' + str(self.player_one) + ', J2 : ' + str(self.player_two)

    def set_result(self, score_one, score_two):
        self.score_one = score_one
        self.score_two = score_two
    
    def get_player_one(self):
        return self.player_one
    
    def get_player_two(self):
        return self.player_two
        
    def resultat(self):
        return [self.player_one, self.score_one], \
               [self.player_two, self.score_two]

    def total_score(self):
        return self.score_one + self.score_two
