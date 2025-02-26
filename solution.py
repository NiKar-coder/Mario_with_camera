import pygame
import os
import sys

pygame.init()


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    return image


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (W, H))
    screen.blit(fon, (0, 0))

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                terminate()
            elif e.type == pygame.KEYDOWN or \
                    e.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(fps)


tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mar.png')


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Grass(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(grasses_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(walls_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)


class Camera:
    def __init__(self):
        pass

    @staticmethod
    def update(group):
        for i in group:
            if not isinstance(i, Player):
                i.rect.x -= dx
                i.rect.y -= dy

    @staticmethod
    def return_update(group):
        for i in group:
            if not isinstance(i, Player):
                i.rect.x += dx
                i.rect.y += dy


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Grass('empty', x, y)
            elif level[y][x] == '#':
                Wall('wall', x, y)
            elif level[y][x] == '@':
                Grass('empty', x, y)
                new_player = Player(x, y)

    return new_player, x, y


fps = 50
W, H = 500, 500

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Перемещение героя')
clock = pygame.time.Clock()
screen.fill('black')

tile_width = tile_height = 50

all_sprites = pygame.sprite.Group()
grasses_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
start_screen()

player, level_x, level_y = generate_level(load_level('new_map.txt'))

camera = Camera()
all_sprites.draw(screen)
while True:
    screen.fill('black')
    dx, dy = 0, 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                dy = -tile_height
            elif event.key == pygame.K_DOWN:
                dy = tile_height
            elif event.key == pygame.K_LEFT:
                dx = -tile_width
            elif event.key == pygame.K_RIGHT:
                dx = tile_width
    camera.update(walls_group)
    camera.update(grasses_group)
    if pygame.sprite.spritecollideany(player, walls_group):
        camera.return_update(walls_group)
        camera.return_update(grasses_group)
    grasses_group.draw(screen)
    walls_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
