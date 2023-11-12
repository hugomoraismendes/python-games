import pygame
import constants
import sprites


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        pygame.display.set_caption(constants.GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.is_running = True

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
        self.all_sprints.draw(self.tela)
        pygame.display.flip()
