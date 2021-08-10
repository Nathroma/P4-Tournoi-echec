from datetime import datetime

from models.match_model import Match

class Round:
    def __init__(self, name):
        self.name = name
        self.start_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.matches = []
        self.end_time = False


    def add_match(self, match: Match):
        self.matches.append(match)

    def add_matches(self, matches: list):
        for match in matches:
            self.matches.append(match)

    def total_scores(self):
        return sum(match.total_score() for match in self.matches)
