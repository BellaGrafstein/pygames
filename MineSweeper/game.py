import pygame
import configparser
import os

# Game imports
from button import Button
from mine_field import Field


class Game:
    def __init__(self):
        self.ROW_COL_COUNT = 18

        pygame.init()
        pygame.font.init()

        self.settings = self.get_config()
        self.screen = pygame.display.set_mode(
            (int(self.settings["Width"]), int(self.settings["Height"]))
        )
        pygame.display.set_caption("Mine Sweeper")

        # Set up tile size
        self.tile_size = (
            int(self.settings["Width"]) // self.ROW_COL_COUNT,
            int(self.settings["Height"]) // self.ROW_COL_COUNT,
        )

        # Set up mine field
        self.mine_field = Field(
            (self.ROW_COL_COUNT, self.ROW_COL_COUNT),
            float(self.settings["BombProbability"]),
        )

        # Load images
        self.tile_images = {}
        self.load_assets()

        # Set up fonts
        self.end_game_font = pygame.font.SysFont(pygame.font.get_default_font(), 40)
        self.end_game_font = pygame.font.SysFont(pygame.font.get_default_font(), 30)

        # Begin game loop
        self.game_started = False
        self.game_over = 0
        self.game_loop()

    def get_config(self):
        config = configparser.ConfigParser()
        config.read("settings.cfg")
        return config["GameSettings"]

    def game_loop(self):
        clock = pygame.time.Clock()

        run = True

        while run:
            clock.tick(int(self.settings["FPS"]))
            # Check each event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONUP and pygame.mouse.get_focused():

                    if self.game_over == -1 or self.game_over == 1:
                        self.game_over = 0
                        # Overwrite the minefeild with a new one for a new game
                        self.mine_field = Field(
                            (self.ROW_COL_COUNT, self.ROW_COL_COUNT),
                            float(self.settings["BombProbability"]),
                        )

                    else:
                        # Get the clicked tile's coordinates from the mouse position
                        pos = pygame.mouse.get_pos()
                        coor = (
                            pos[1] // self.tile_size[1],
                            pos[0] // self.tile_size[0],
                        )

                        if coor[0] < len(self.mine_field.board) and coor[1] < len(
                            self.mine_field.board[coor[0]]
                        ):
                            # Get the click id, 1 for a left click, 3 for a right click
                            click_id = event.button

                            # Left click
                            if click_id == 1:
                                # Set tile explored
                                self.game_over = self.mine_field.set_explored(coor)
                            # Right click
                            elif click_id == 3:
                                # Add a flag
                                self.mine_field.set_flag(coor)

                # Update game screen
                self.draw_game()

        pygame.quit()

    def draw_game(self):
        self.screen.fill((215, 215, 215))

        if not self.game_over:

            for row in range(len(self.mine_field.board)):
                for col in range(len(self.mine_field.board[row])):
                    tile = self.mine_field.board[row][col]
                    if tile.explored:
                        if tile.has_bomb:
                            self.screen.blit(
                                self.tile_images["Bomb"],
                                (col * self.tile_size[0], row * self.tile_size[1]),
                            )
                        elif tile.seen_bombs == 0:
                            self.screen.blit(
                                self.tile_images["Empty"],
                                (col * self.tile_size[0], row * self.tile_size[1]),
                            )
                        else:
                            img_str = "Checked_0" + str(tile.seen_bombs)
                            self.screen.blit(
                                self.tile_images[img_str],
                                (col * self.tile_size[0], row * self.tile_size[1]),
                            )
                    else:
                        if tile.flagged:
                            self.screen.blit(
                                self.tile_images["Flag"],
                                (col * self.tile_size[0], row * self.tile_size[1]),
                            )
                        else:
                            self.screen.blit(
                                self.tile_images["Unchecked"],
                                (col * self.tile_size[0], row * self.tile_size[1]),
                            )

        else:
            end_text = ""
            if self.game_over == 1:
                end_text = "You won!!!"
            else:
                end_text = "You lost :("
            draw_text = self.end_game_font.render(end_text, 1, (0, 0, 0))
            restart_text = self.end_game_font.render(
                "Click to restart...", 1, (0, 0, 0)
            )
            self.screen.blit(
                draw_text,
                (
                    int(self.settings["Width"]) // 2 - draw_text.get_width() // 2,
                    int(self.settings["Height"]) // 2 - draw_text.get_height() // 2,
                ),
            )

            self.screen.blit(
                restart_text,
                (
                    int(self.settings["Width"]) // 2 - restart_text.get_width() // 2,
                    int(self.settings["Height"]) // 2 + draw_text.get_height(),
                ),
            )

        pygame.display.update()

    def load_assets(self):
        tile_dir = str(self.settings["TileDir"])

        for filename in os.listdir(tile_dir):
            image = pygame.image.load(os.path.join(tile_dir, filename))
            pygame.transform.scale(image, (self.tile_size[0], self.tile_size[1]))
            self.tile_images[filename.split(".")[0]] = image
