import pygame
import pyBaba
import config
import sys
import sprites
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

icon_images = {pyBaba.ObjectType.ICON_BABA: 'BABA',
               pyBaba.ObjectType.ICON_FLAG: 'FLAG',
               pyBaba.ObjectType.ICON_WALL: 'WALL',
               pyBaba.ObjectType.ICON_ROCK: 'ROCK',
               pyBaba.ObjectType.ICON_TILE: 'TILE',
               pyBaba.ObjectType.ICON_WATER: 'WATER',
               pyBaba.ObjectType.ICON_GRASS: 'GRASS',
               pyBaba.ObjectType.ICON_LAVA: 'LAVA',
               pyBaba.ObjectType.ICON_SKULL: 'SKULL',
               pyBaba.ObjectType.ICON_FLOWER: 'FLOWER'}

text_images = {pyBaba.ObjectType.BABA: 'BABA',
               pyBaba.ObjectType.IS: 'IS',
               pyBaba.ObjectType.YOU: 'YOU',
               pyBaba.ObjectType.FLAG: 'FLAG',
               pyBaba.ObjectType.WIN: 'WIN',
               pyBaba.ObjectType.WALL: 'WALL',
               pyBaba.ObjectType.STOP: 'STOP',
               pyBaba.ObjectType.ROCK: 'ROCK',
               pyBaba.ObjectType.PUSH: 'PUSH',
               pyBaba.ObjectType.WATER: 'WATER',
               pyBaba.ObjectType.SINK: 'SINK',
               pyBaba.ObjectType.LAVA: 'LAVA',
               pyBaba.ObjectType.MELT: 'MELT',
               pyBaba.ObjectType.HOT: 'HOT',
               pyBaba.ObjectType.SKULL: 'SKULL',
               pyBaba.ObjectType.DEFEAT: 'DEFEAT'}

game = pyBaba.Game("../../Resources/Maps/simple_map.txt")
screen_size = (game.GetMap().GetWidth() * config.BLOCK_SIZE,
               game.GetMap().GetHeight() * config.BLOCK_SIZE)
screen = pygame.display.set_mode( #screen size settings
    (screen_size[0], screen_size[1]), pygame.DOUBLEBUF)

map_sprite_group = pygame.sprite.Group()

result_image = sprites.ResultImage()
result_image_group = pygame.sprite.Group()
result_image_group.add(result_image)


def draw_obj(x_pos, y_pos):
    objects = game.GetMap().At(x_pos, y_pos)
    is_icon = False

    for obj_type in objects.GetTypes():
        if pyBaba.IsTextType(obj_type):
            obj_image = text_images[obj_type]
        else:
            if obj_type == pyBaba.ObjectType.ICON_EMPTY:
                continue
            obj_image = icon_images[obj_type]
            is_icon = True
        map_sprite = sprites.MapSprite(obj_image, x_pos * config.BLOCK_SIZE, y_pos * config.BLOCK_SIZE, is_icon)
        map_sprite_group.add(map_sprite)


def draw():
    map_sprite_group.empty()

    for y_pos in range(game.GetMap().GetHeight()):
        for x_pos in range(game.GetMap().GetWidth()):
            draw_obj(x_pos, y_pos)

    map_sprite_group.draw(screen)


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    """size_modifier=2
    (width, height) = (600*size_modifier, 400*size_modifier)
    screen = pygame.display.set_mode((width, height))"""

    #rescale game
    #screen.blit(sprite, [5, 5])
    resolution = (screen_size[0], screen_size[1])
    surf = pygame.transform.scale2x(screen)
    _screen = pygame.display.set_mode(resolution)
    _screen.blit(surf, [0,0])
    pygame.display.flip()

    action_dic = {"Direction.UP": pyBaba.Direction.UP, "Direction.DOWN": pyBaba.Direction.DOWN,
                  "Direction.LEFT": pyBaba.Direction.LEFT, "Direction.RIGHT": pyBaba.Direction.RIGHT, "Direction.NONE": pyBaba.Direction.NONE}

    clock = pygame.time.Clock()

    pygame.time.set_timer(pygame.USEREVENT, 200)

    game_over = False
    time_step = 0

    while True:
        if game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            if game.GetPlayState() == pyBaba.PlayState.WON:
                result_image_group.update(pyBaba.PlayState.WON, screen_size)
                result_image_group.draw(screen)
            else:
                result_image_group.update(pyBaba.PlayState.LOST, screen_size)
                result_image_group.draw(screen)
            pygame.display.flip()
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP]: game.MovePlayer(action_dic['Direction.UP'])
            if pressed[pygame.K_DOWN]: game.MovePlayer(action_dic['Direction.DOWN'])
            if pressed[pygame.K_LEFT]: game.MovePlayer(action_dic['Direction.LEFT'])
            if pressed[pygame.K_RIGHT]: game.MovePlayer(action_dic['Direction.RIGHT'])

  
        if game.GetPlayState() == pyBaba.PlayState.WON or game.GetPlayState() == pyBaba.PlayState.LOST:
            game_over = True

        screen.fill(config.COLOR_BACKGROUND)
        draw()
        pygame.display.flip()

        clock.tick(config.FPS)
