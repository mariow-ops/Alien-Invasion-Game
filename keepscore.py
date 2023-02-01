import pygame.font
from pygame.sprite import Group

from ship import Ship


class Keepscore:

    def __init__(self, ai_game):

        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_high_score()
        self.prep_aliens_hit()
        self.prep_ships()
        

    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)
                                                 
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20

    def prep_aliens_hit(self):
        aliens_hit = round(self.stats.aliens_hit, None)
        aliens_hit_str = "{:,}".format(aliens_hit)
        self.aliens_hit_image = self.font.render(aliens_hit_str, True, self.text_color, self.settings.bg_color)

        self.aliens_hit_rect = self.aliens_hit_image.get_rect()
        self.aliens_hit_rect.right = self.screen_rect.right - 20
        self.aliens_hit_rect.top = 20
    
    def prep_ships(self):
        
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score() 
            
             
    def show_score(self):
        
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.aliens_hit_image, self.aliens_hit_rect)
        self.ships.draw(self.screen)