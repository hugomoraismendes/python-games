import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange, choice
import constants

pygame.init()
pygame.mixer.init()

main_directory = os.path.dirname(__file__)
images_directory = os.path.join(main_directory, "../images")
sound_directory = os.path.join(main_directory, "../audios")


screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))

pygame.display.set_caption("Dino Game")

sprite_sheet = pygame.image.load(
    os.path.join(images_directory, "dino-sprite-sheet1.png")
).convert_alpha()

coliision_sound = pygame.mixer.Sound(os.path.join(sound_directory, "death_sound.wav"))
coliision_sound.set_volume(1)

som_pontuacao = pygame.mixer.Sound(os.path.join(sound_directory, "score_sound.wav"))
som_pontuacao.set_volume(1)

collision = False

choose_obstacle = choice([0, 1])

score = 0

speed_game = 10


def prepare_message(msg, size, color):
    font = pygame.font.SysFont("times", size, True, False)
    message = f"{msg}"
    formated_text = font.render(message, True, color)
    return formated_text


def restart_game():
    global score, speed_game, collision, choose_obstacle
    score = 0
    speed_game = 10
    collision = False
    dino.rect.y = constants.HEIGHT - 64 - 96 // 2
    dino.pulo = False
    pterodactyl.rect.x = constants.WIDTH
    cactus.rect.x = constants.WIDTH
    choose_obstacle = choice([0, 1])


class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.som_pulo = pygame.mixer.Sound(
            os.path.join(sound_directory, "jump_sound.wav")
        )
        self.som_pulo.set_volume(1)
        self.imagens_dinossauro = []
        for i in range(3):
            img = sprite_sheet.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (32 * 3, 32 * 3))
            self.imagens_dinossauro.append(img)

        self.index_lista = 0
        self.image = self.imagens_dinossauro[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_y_inicial = constants.HEIGHT - 64 - 96 // 2
        self.rect.topleft = (100, self.pos_y_inicial)  # 368   416(centro y)
        self.pulo = False

    def pular(self):
        self.pulo = True
        self.som_pulo.play()

    def update(self):
        if self.pulo == True:
            if self.rect.y <= self.pos_y_inicial - 150:
                self.pulo = False
            self.rect.y -= 15

        else:
            if self.rect.y >= self.pos_y_inicial:
                self.rect.y = self.pos_y_inicial
            else:
                self.rect.y += 15

        if self.index_lista > 2:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.imagens_dinossauro[int(self.index_lista)]


class Clouds(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((7 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 3, 32 * 3))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 200, 50)
        self.rect.x = constants.WIDTH - randrange(30, 300, 90)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = constants.WIDTH
            self.rect.y = randrange(50, 200, 50)
        self.rect.x -= speed_game


class Floor(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((6 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))
        self.rect = self.image.get_rect()
        self.rect.y = constants.HEIGHT - 64
        self.rect.x = pos_x * 64

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = constants.WIDTH
        self.rect.x -= 10


class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((5 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = choose_obstacle
        self.rect.center = (constants.WIDTH, constants.HEIGHT - 64)
        self.rect.x = constants.WIDTH

    def update(self):
        if self.escolha == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = constants.WIDTH
            self.rect.x -= speed_game


class Pterodactyl(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_dinossauro = []
        for i in range(3, 5):
            img = sprite_sheet.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (32 * 3, 32 * 3))
            self.imagens_dinossauro.append(img)

        self.index_lista = 0
        self.image = self.imagens_dinossauro[self.index_lista]
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = choose_obstacle
        self.rect = self.image.get_rect()
        self.rect.center = (constants.WIDTH, 300)
        self.rect.x = constants.WIDTH

    def update(self):
        if self.escolha == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = constants.WIDTH
            self.rect.x -= speed_game

            if self.index_lista > 1:
                self.index_lista = 0
            self.index_lista += 0.25
            self.image = self.imagens_dinossauro[int(self.index_lista)]


all_sprites = pygame.sprite.Group()
dino = Dino()
all_sprites.add(dino)

for i in range(4):
    nuvem = Clouds()
    all_sprites.add(nuvem)

for i in range(constants.WIDTH * 2 // 64):
    floor = Floor(i)
    all_sprites.add(floor)

cactus = Cactus()
all_sprites.add(cactus)

pterodactyl = Pterodactyl()
all_sprites.add(pterodactyl)

obstacle_group = pygame.sprite.Group()
obstacle_group.add(cactus)
obstacle_group.add(pterodactyl)

clock = pygame.time.Clock()
while True:
    clock.tick(30)
    screen.fill(constants.WHITE)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE and collision == False:
                if dino.rect.y != dino.pos_y_inicial:
                    pass
                else:
                    dino.pular()

            if event.key == K_r and collision == True:
                restart_game()

    colisoes = pygame.sprite.spritecollide(
        dino, obstacle_group, False, pygame.sprite.collide_mask
    )

    all_sprites.draw(screen)

    if cactus.rect.topright[0] <= 0 or pterodactyl.rect.topright[0] <= 0:
        choose_obstacle = choice([0, 1])
        cactus.rect.x = constants.WIDTH
        pterodactyl.rect.x = constants.WIDTH
        cactus.escolha = choose_obstacle
        pterodactyl.escolha = choose_obstacle

    if colisoes and collision == False:
        coliision_sound.play()
        collision = True

    if collision == True:
        if score % 100 == 0:
            score += 1

        game_over = prepare_message("GAME OVER", 40, (0, 0, 0))

        width = (constants.WIDTH // 2) - 80
        height = constants.HEIGHT // 2

        screen.blit(game_over, (width, height - 60))
        restart = prepare_message("Pressione r para reiniciar", 20, (0, 0, 0))
        screen.blit(restart, (width, height + 20))

    else:
        score += 1
        all_sprites.update()
        text_score = prepare_message(score, 40, (0, 0, 0))

    if score % 100 == 0:
        som_pontuacao.play()
        if speed_game >= 23:
            speed_game += 0
        else:
            speed_game += 1

    screen.blit(text_score, (520, 30))

    pygame.display.flip()
