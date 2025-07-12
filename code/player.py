import pygame
from settings import * 
from support import *
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacles_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(groups)
        self.image = pygame.image.load('./graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET['player'])

        # import player assets
        self.import_player_assets()
        self.status = 'down'  # default status

        # movement 
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacles_sprites = obstacles_sprites

        # weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200  # time to switch weapons & magic

        # magic
        self.create_magic = create_magic
        self.magic_index = 0  # index for magic spells, if you have multiple
        self.magic = list(magic_data.keys())[self.magic_index]  # current magic spell
        self.can_switch_magic = True
        self.magic_switch_time = None

        # stats
        self.stats = {
            'health': 100,
            'energy': 60,
            'attack': 10,
            'magic': 4,
            'speed': 5,
        }
        self.max_stats = {
            'health': 300,
            'energy': 140,
            'attack': 20,
            'magic': 10,
            'speed': 10,
        }
        self.upgrade_cost = {
            'health': 100,
            'energy': 100,
            'attack': 100,
            'magic': 100,
            'speed': 100,
        }
        self.health = self.stats['health'] * 0.5
        self.energy = self.stats['energy'] * 0.8
        self.exp = 5000
        self.speed = self.stats['speed']

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500  # milliseconds

        # import sound
        self.weapon_attack_sound = pygame.mixer.Sound('./audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.4)

    def import_player_assets(self):
        character_path = './graphics/player/'
        self.animations = {
            'up': [],
            'down': [],
            'left': [],
            'right': [],
            'right_idle': [],
            'left_idle': [],
            'up_idle': [],
            'down_idle': [],
            'right_attack': [],
            'left_attack': [],
            'up_attack': [],
            'down_attack': [],
        }
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
    
    def input(self):
        if not self.attacking:  # only process input if not attacking
            keys = pygame.key.get_pressed()

            #MOVEMENT input
            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
            
            # attack input
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()  # reset attack time 
                self.create_attack()
                self.weapon_attack_sound.play()

            # magic input
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()  # reset attack time 
                style = list(magic_data.keys())[self.magic_index]  # get the current magic style
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']  # get the magic strength
                cost = list(magic_data.values())[self.magic_index]['cost'] 

                self.create_magic(style, strength, cost)  # example magic call
            
            if keys[pygame.K_q] and self.can_switch_weapon:  # change weapon
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                if self.weapon_index < len(weapon_data.keys()) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                self.weapon = list(weapon_data.keys())[self.weapon_index]
            
            if keys[pygame.K_e] and self.can_switch_magic:  # change weapon
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                if self.magic_index < len(magic_data.keys()) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0
                self.magic = list(magic_data.keys())[self.magic_index]
    
    def get_status(self):
        if self.direction.magnitude() == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status += '_idle'
        
        if self.attacking:
            self.direction = pygame.math.Vector2(0, 0)  # stop movement during attack
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status += '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')  # remove attack status if not attacking

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()
        
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True
        
        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True
        
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        animation = self.animations[self.status]
    
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # flicker 
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    
    def get_full_weapon_damage(self) -> int:
        # calculate the full weapon damage considering player's stats and resistance
        return weapon_data[self.weapon]['damage'] + self.stats['attack']

    def get_full_magic_damage(self) -> int:
        # calculate the full magic damage considering player's stats and resistance
        return magic_data[self.magic]['strength'] + self.stats['magic']
    
    def get_value_by_index(self, index) -> int:
        return list(self.stats.values())[index]
    
    def get_cost_by_index(self, index) -> int:
        return list(self.upgrade_cost.values())[index]

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']  # recover energy over time
            if self.energy > self.stats['energy']:
                self.energy = self.stats['energy']

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.stats['speed'])
        self.energy_recovery()
