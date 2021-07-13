from datetime import datetime

from models.match_model import Match

class Round:
    def __init__(self, name):
        self.name = name
        self.start_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.matches = []
        self.end_time = False

    def close(self):
        self.end_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    def add_match(self, match: Match):
        self.matches.append(match)

    def add_matches(self, matches: list):
        for match in matches:
            self.matches.append(match)

    def is_closed(self):
        return self.end_time

    def total_scores(self):
        return sum(match.total_score() for match in self.matches)

    def serialize(self):
        return {
            'name': self.name,
            'start_time': self.start_time,
            'matches': [match.serialize() for match in self.matches],
            'end_time': self.end_time,
        }

    @classmethod
    def deserialize(cls, serialized_round):
        name = serialized_round['name']
        round = Round(name)
        round.start_time = serialized_round['start_time']
        round.matches = [
            Match.deserialize(serialized_match)
            for serialized_match in serialized_round['matches']
        ]
        round.end_time = serialized_round['end_time']
        return round

    def to_report(self):
        return {
            'name': self.name,
            'start_time': self.start_time,
            'end_time': self.end_time,
        }