import pygame, sys
from settings import *
from math import sin

class Menu:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(UI_FONT, 20)
        self.screen_width, self.screen_height = self.screen.get_size()
        self.logo = pygame.image.load('./graphics/menu/logo.png').convert_alpha()
        self.logo = pygame.transform.smoothscale(self.logo, (550, 550))

        self.background = pygame.image.load('./graphics/menu/background_menu.png').convert_alpha()
        self.background = pygame.transform.smoothscale(self.background, (self.screen_width, self.screen_height))
        self.background_rect = self.background.get_rect(topleft=(0,0))
    
    def wave_value(self) -> int:
        value = sin(0.005 * pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
        
    def offset(self):
        return 50 * sin(0.002 * pygame.time.get_ticks()) - 50
    
    def draw(self):
        self.screen.blit(self.background, self.background_rect)

        # Logo
        logo_rect = self.logo.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + self.offset()))
        self.screen.blit(self.logo, logo_rect)

        # Instructions
        info_text = self.font.render("- Press SPACE to play -", False, TEXT_COLOR)
        info_rect = info_text.get_rect(center=(self.screen_width // 2, self.screen_height - 100))
        info_text.set_alpha(self.wave_value())
        self.screen.blit(info_text, info_rect)
    
    def fade_out(self, speed=5):
        fade_surface = pygame.Surface((self.screen_width, self.screen_width)).convert()
        fade_surface.fill((0, 0, 0))

        for alpha in range(0, 255 + speed, speed):
            self.draw()  # redessine le menu derrière
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.update()
            self.clock.tick(60)

    def run(self):
        while self.running:
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.fade_out()
                        self.running = False  # quitte le menu
