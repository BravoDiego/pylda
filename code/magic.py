import pygame
from settings import *
from random import randint

class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player
    
    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
            player.energy -= cost
            player.health += strength
            if player.health > player.stats['health']:
                player.health = player.stats['health']
            self.animation_player.create_particles('aura', player.rect.center, groups)
            self.animation_player.create_particles('heal', player.rect.center + pygame.math.Vector2(0, -60), groups)

    def flame(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost
            if player.status.split('_')[0] == 'right': direction = pygame.math.Vector2(1, 0)
            elif player.status.split('_')[0] == 'left': direction = pygame.math.Vector2(-1, 0)
            elif player.status.split('_')[0] == 'up': direction = pygame.math.Vector2(0, -1)
            else: direction = pygame.math.Vector2(0, 1)
            for i in range(1, 6):
                if direction.x: # horizontal direction
                    offset_x = i * TILESIZE * direction.x
                    x = player.rect.centerx + offset_x + randint(-TILESIZE//3, TILESIZE//3)
                    y = player.rect.centery+ randint(-TILESIZE//3, TILESIZE//3)
                    self.animation_player.create_particles('flame', (x, y), groups) 
                else: #vertical
                    offset_y = i * TILESIZE * direction.y
                    x = player.rect.centerx + randint(-TILESIZE//3, TILESIZE//3)
                    y = player.rect.centery + offset_y + randint(-TILESIZE//3, TILESIZE//3)
                    self.animation_player.create_particles('flame', (x, y), groups)

            
            # Here you would create the flame magic sprite
            # For example:
            # FlameMagic(player, groupq, strength, cost)