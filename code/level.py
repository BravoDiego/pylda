import pygame 
from settings import *
from tile import Tile
from player import Player
from weapon import Weapon
from ui import UI
from debug import debug
from support import *
from random import choice

class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groupe setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        # atatck sprite group
        self.current_attack = None

        #sprite setup
        self.create_map()

        # user interface
        self.ui = UI()

    def create_map(self):
        # create the map, load tiles and player
        # this is where you would load your level data
        layouts = {
            'boundary': import_csv_layout('./map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('./map/map_Grass.csv'),
            'object': import_csv_layout('./map/map_Objects.csv'),
        }
        graphics = {
            'grass': import_folder('./graphics/grass'),
            'objects': import_folder('./graphics/objects'),
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacles_sprites], 'invisible')
                        if style == 'grass':
                            # create a grass tile
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y), [self.visible_sprites, self.obstacles_sprites], 'grass', random_grass_image)
                            
                        if style == 'object':
                            # create an object tile
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacles_sprites], 'object', surf)

        self.player = Player(
            (2000, 1400), 
            [self.visible_sprites], 
            self.obstacles_sprites, 
            self.create_attack, 
            self.destroy_attack,
            self.create_magic,
        )
        
    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])
    
    def create_magic(self, style, strength, cost):
        print(f'Creating magic of style: {style}, strength: {strength}, cost: {cost}')
        if style == 'flame':
            print('Flame magic created')
            # Here you would create the flame magic sprite
            # For example:
            # FlameMagic(self.player, [self.visible_sprites], strength, cost)
        elif style == 'heal':
            print('Heal magic created')
            # Here you would create the heal magic sprite
            # For example:
            # HealMagic(self.player, [self.visible_sprites], strength, cost)
        else:
            print('Unknown magic style')

    
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
            self.current_attack = None
    
    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surface = pygame.image.load('./graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):

        #getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)