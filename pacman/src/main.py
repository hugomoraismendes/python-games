import pygame
import constants
import sprites
import os


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        pygame.display.set_caption(constants.GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.font = pygame.font.match_font(constants.FONT_FAMILY)
        self.load_files()

    def new_game(self):
        self.all_sprints = pygame.sprite.Group()
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(constants.FPS)
            self.events()
            self.update_sprites()
            self.draw_sprites()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.is_running = False

    def update_sprites(self):
        self.all_sprints.update()

    def draw_sprites(self):
        self.screen.fill(constants.BLACK)
        self.all_sprints.draw(self.screen)
        pygame.display.flip()

    def load_files(self):
        image_directory = os.path.join(os.getcwd(), "../images")
        self.audio_directory = os.path.join(os.getcwd(), "../audios")
        self.sprite_sheet = os.path.join(image_directory, constants.SPRITE_SHEET)
        self.pacman_start_logo = os.path.join(
            image_directory, constants.PACMAN_START_LOGO
        )
        self.pacman_start_logo = pygame.image.load(self.pacman_start_logo).convert()

    def display_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font, size)
        text = font.render(text, True, color)
        text_rect = text.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text, text_rect)

    def display_start_logo(self, x, y):
        start_logo_rect = self.pacman_start_logo.get_rect()
        start_logo_rect.midtop = (x, y)
        self.screen.blit(self.pacman_start_logo, start_logo_rect)

    def display_start_screen(self):
        pygame.mixer.music.load(
            os.path.join(self.audio_directory, constants.START_MUSIC)
        )
        pygame.mixer.music.play()

        self.display_start_logo(constants.WIDTH / 2, 20)

        self.display_text(
            "-Pressione uma tecla para jogar",
            32,
            constants.YELLOW,
            constants.WIDTH / 2,
            320,
        )
        self.display_text(
            "Desenvolvido por Hugo Mendes",
            19,
            constants.WHITE,
            constants.WIDTH / 2,
            570,
        )

        pygame.display.flip()
        self.wait_for_the_player()

    def wait_for_the_player(self):
        wait = True
        while wait:
            self.clock.tick(constants.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    wait = False
                    self.is_running = False
                if event.type == pygame.KEYUP:
                    wait = False
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound(
                        os.path.join(self.audio_directory, constants.START_KEY)
                    ).play()

    def display_gameover_screen(self):
        pass


g = Game()
g.display_start_screen()

while g.is_running:
    g.new_game()
    g.display_gameover_screen()
