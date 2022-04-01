from tile import Tile
import random


class Field:
    def __init__(self, size, bomb_probabilty):
        # (Row, Column) counts
        self.size = size
        self.tile_count = size[0] * size[1]
        # Appx probability of any tile being a bomb
        self.bomb_probability = bomb_probabilty
        # Array representing a board
        self.board = []
        # Count of all the bombs
        self.bomb_count = 0
        # Number of tiles explored
        self.explored = 0

        self.set_mine_field()

    def set_mine_field(self):
        for row in range(self.size[0]):
            field_row = []
            for col in range(self.size[1]):
                # Check if there is a bomb
                has_bomb = self.has_bomb()
                # Create tile and append it to the mine field
                tile = Tile(has_bomb)
                field_row.append(tile)
                # If there is a bomb, increment the bomb count and increment
                # seen bombs for the existing, surounding tiles
                if has_bomb:
                    self.bomb_count += 1
                    # Add 1 to the bombs to the left and above
                    if row:
                        self.board[row - 1][col].increment_seen_bombs()
                        if col:
                            self.board[row - 1][col - 1].increment_seen_bombs()
                        if col < self.size[1] - 1:
                            self.board[row - 1][col + 1].increment_seen_bombs()
                    if col:
                        field_row[col - 1].increment_seen_bombs()

                # Check the existing tiles to the left and above
                else:
                    if row:
                        if self.board[row - 1][col].has_bomb:
                            tile.increment_seen_bombs()
                        if col and self.board[row - 1][col - 1].has_bomb:
                            tile.increment_seen_bombs()
                        if (
                            col + 1 < self.size[1]
                            and self.board[row - 1][col + 1].has_bomb
                        ):
                            tile.increment_seen_bombs()

                    if col and field_row[col - 1].has_bomb:
                        tile.increment_seen_bombs()

            self.board.append(field_row)

    def has_bomb(self):
        return random.random() < self.bomb_probability

    def set_explored(self, coordinates: tuple):
        # print(coordinates)
        game_over = 0
        self.explored += 1
        col, row = coordinates[0], coordinates[1]
        tile = self.board[col][row]
        if not tile.flagged:
            tile.explored = True
            if tile.has_bomb:
                game_over = -1
            elif tile.seen_bombs == 0:
                # Expand region to encompass all 0 elements
                if row:
                    # Look directly up
                    if not self.board[col][row - 1].explored:
                        self.set_explored((col, row - 1))
                    # Look up and to the left, if it is not explored
                    if col and not self.board[col - 1][row - 1].explored:
                        self.set_explored((col - 1, row - 1))
                    # Look up and to the right, if it is not explored
                    if (
                        col + 1 < self.size[0]
                        and not self.board[col + 1][row - 1].explored
                    ):
                        self.set_explored((col + 1, row - 1))
                # Check the row below
                if row + 1 < self.size[1]:
                    # Look directly down
                    if not self.board[col][row + 1].explored:
                        self.set_explored((col, row + 1))
                    # Look down to the left
                    if col and not self.board[col - 1][row + 1].explored:
                        self.set_explored((col - 1, row + 1))
                    # Look down to the right
                    if (
                        col + 1 < self.size[0]
                        and not self.board[col + 1][row + 1].explored
                    ):
                        self.set_explored((col + 1, row + 1))
                # Look directly left
                if col and not self.board[col - 1][row].explored:
                    self.set_explored((col - 1, row))
                # Look directly right
                if col + 1 < self.size[0] and not self.board[col + 1][row].explored:
                    self.set_explored((col + 1, row))

            # Check if all tiles have been explored
            if self.explored + self.bomb_count == self.tile_count:
                game_over = 1
        return game_over

    def set_flag(self, coordinates):
        tile = self.board[coordinates[0]][coordinates[1]]
        tile.flagged = not tile.flagged
