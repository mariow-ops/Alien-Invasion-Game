import sys
import os
from time import sleep

import pygame

from settings import Settings
from gamestats import Gamestats
from keepscore import Keepscore
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:

    def __init__(self):

        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode ((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        self.screen = pygame.display.set_mode ((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption ("Marios Alien Invasion")

        self.stats = Gamestats(self)
        self.ks = Keepscore(self)

        self.bg_color = (230, 10, 230)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):

        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()             
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                    
                    
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collsions()



    def _check_bullet_alien_collsions(self):


        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)


        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.stats.aliens_hit += self.settings.aliens_hit * len(aliens)
            self.ks.check_high_score()
            self.ks.prep_aliens_hit()

        if not self.aliens:

            self.bullets.empty()
            self._create_fleet()


    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print ("SHIP HIT!!!")
            self._ship_hit()
        self._check_aliens_bottom()



    def _create_fleet(self):

        aliens = Alien(self)
        aliens_width, aliens_height = aliens.rect.size

        available_space_x = self.settings.screen_width - (2*aliens_width)
        number_aliens_x = available_space_x // (2*aliens_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (4 * aliens_height) - ship_height)
        number_rows = available_space_y // (2 * aliens_height)

        for row_number in range (number_rows):
            for alien_number in range (number_aliens_x):
                self._create_alien(alien_number, row_number)


    def _create_alien(self, alien_number, row_number):
        
        aliens = Alien(self)
        aliens_width, aliens_height = aliens.rect.size
        aliens_width = aliens.rect.width
        aliens.x = aliens_width + 2 * aliens_width * alien_number
        aliens.rect.x = aliens.x
        aliens.rect.y = aliens_height + 2 * aliens.rect.height * row_number
        self.aliens.add(aliens)
    

    def _check_fleet_edges(self):

        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1       


    def _ship_hit(self):

        if self.stats.ships_left >= 0:

            self.stats.ships_left -= 1
            self.ks.prep_ships()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep (0.5)
        if self.stats.ships_left < 0:
            while 1:
             Game_Over = pygame.font.SysFont('Corbel',100).render("GAME OVER", True,(30,30,30))
             self.screen.blit(Game_Over, (1200/2 -200, 800/2-50))
             self._check_events()
             self.aliens.empty()
             pygame.display.flip()
             
            


    def _check_aliens_bottom(self):
        
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:

                self._ship_hit()
                break


    def _update_screen(self):        
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
     
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()

            self.aliens.draw(self.screen)

            self.ks.show_score()

            pygame.display.flip()

if __name__ == '__main__':

    ai = AlienInvasion()
    ai.run_game()

quit()