
from dataclasses import dataclass
from datetime import date


@dataclass
class Attori:
    id:str
    name:str
    height: int
    date_of_birth: date
    known_for_movies:str

    def __eq__(self, other):
        return self.id == other.id
    def __hash__(self):
        return hash(self.id)
    def __str__(self):
        return f"{self.name} - ({self.id})"