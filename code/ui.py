import pygame 
from settings import *

class UI:
    def __init__(self):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # convert weapon dict keys to a list for easy access
        self.weapon_graphic = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphic.append(weapon)
        
        # convert magic dict keys to a list for easy access
        self.magic_graphic = []
        for magic in magic_data.values():
            path = magic['graphic']
            magic = pygame.image.load(path).convert_alpha()
            self.magic_graphic.append(magic)
    
    def show_bar(self, current, max_amount, bg_rect, color):
        # draw background
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # calculate width based on current value
        ratio = current / max_amount
        bar_width = int(bg_rect.width * ratio)
        
        # draw the filled part of the bar
        filled_rect = bg_rect.copy()
        filled_rect.width = bar_width

        # draw the rect 
        pygame.draw.rect(self.display_surface, color, filled_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def selection_box(self, left, top, has_switched) -> pygame.Rect:
        bg_react = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_react)
        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_react, 3)
        else:
            # draw the normal border
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_react, 3)
        return bg_react

    def weapon_overlay(self, weapon_index, has_switched):
        bg_rect = self.selection_box(10, 630, has_switched) # weapon selection box
        weapon_surf = self.weapon_graphic[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)
    
    def magic_overlay(self, magic_index, has_switched):
        bg_rect = self.selection_box(80, 635, has_switched)
        magic_surf = self.magic_graphic[magic_index]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(magic_surf, magic_rect)
    
        
    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)

        self.show_exp(player.exp)
        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        self.magic_overlay(player.magic_index, not player.can_switch_magic) # magic selection box