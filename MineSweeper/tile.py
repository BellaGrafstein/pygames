class Tile:
    def __init__(self, has_bomb):
        self.has_bomb = has_bomb
        self.seen_bombs = 0
        self.explored = False
        self.flagged = False

    def increment_seen_bombs(self):
        self.seen_bombs += 1
