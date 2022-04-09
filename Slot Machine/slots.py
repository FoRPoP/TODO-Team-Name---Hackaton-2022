from ast import Str
import itertools
from operator import le
import string
from tokenize import Double, String
from typing import List
from xmlrpc.client import Boolean
from matplotlib.pyplot import yscale
import pygame, os, random, sys, noise
from PIL import Image
import itertools

import button

from pygame.locals import *
import button
from menu import *

import data.engine as e


class Game():
    def __init__(self):

        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 1920, 1080
        self.clock = pygame.time.Clock()
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.font_name = '8-BIT WONDER.TTF'
        self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)

        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

        self.background_img = pygame.image.load('data/images/background.png')
        self.table_img = pygame.image.load('data/images/table.png')
        self.table_borders_img = pygame.image.load('data/images/table_borders.png')
        self.pineapple_img = pygame.image.load('data/images/pineapple.png')
        self.rectangle_img = pygame.image.load('data/images/rectangle.png')

        self.lines1_img = pygame.image.load('data/images/lines1.png')
        self.totalbet_img = pygame.image.load('data/images/totalbet.png')
        self.won_img = pygame.image.load('data/images/won.png')
        self.credits1_img = pygame.image.load('data/images/credits1.png')
        self.spins_img = pygame.image.load('data/images/spins.png')


        self.spin_img = pygame.image.load('./data/images/spinbutton.png')
        self.autostart_img = pygame.image.load('./data/images/autostart.png')
        self.lines_img = pygame.image.load('./data/images/lines.png')
        self.betmax_img = pygame.image.load('./data/images/betmax.png')
        self.soundon_img = pygame.image.load('./data/images/sound.png')
        self.soundoff_img = pygame.image.load('./data/images/sound-off.png')
        self.return_img = pygame.image.load('./data/images/return.png')
        self.sound=True

        self.spin_button = button.Button(1920/2-self.spin_img.get_width()/2, 840, self.spin_img, 1)
        self.autostart_button = button.Button(0,300,self.autostart_img,1)
        self.lines_button = button.Button(1720,300,self.lines_img,1)
        self.betmax_button = button.Button(1705,600,self.betmax_img,1)
        self.soundon_button = button.Button(1805, 30, self.soundon_img, 0.2)
        self.soundoff_button = button.Button(1805, 30, self.soundoff_img, 0.2)
        self.return_button = button.Button(60, 30, self.return_img, 0.1)

        self.banana_img = pygame.image.load('data/images/banana.png')
        self.banana_img = pygame.transform.scale(self.banana_img, (191, 153))
        self.apple_img = pygame.image.load('data/images/apple.png')
        self.apple_img = pygame.transform.scale(self.apple_img, (191, 153))
        self.jungle1_img = pygame.image.load('data/images/jungle1.png')
        self.jungle1_img = pygame.transform.scale(self.jungle1_img, (191, 153))
        self.pyramid_img = pygame.image.load('data/images/pyramid.png')
        self.pyramid_img = pygame.transform.scale(self.pyramid_img, (191, 153))
        self.monkey_img = pygame.image.load('data/images/monkey.png')
        self.monkey_img = pygame.transform.scale(self.monkey_img, (191, 153))
        self.alfa_img = pygame.image.load('data/images/alfa.png')
        self.alfa_img = pygame.transform.scale(self.alfa_img, (191, 153))
        self.beta_img = pygame.image.load('data/images/beta.png')
        self.beta_img = pygame.transform.scale(self.beta_img, (191, 153))
        self.omega_img = pygame.image.load('data/images/omega.png')
        self.omega_img = pygame.transform.scale(self.omega_img, (191, 153))
        self.mi_img = pygame.image.load('data/images/mi.png')
        self.mi_img = pygame.transform.scale(self.mi_img, (191, 153))
        self.pi_img = pygame.image.load('data/images/pi.png')
        self.pi_img = pygame.transform.scale(self.pi_img, (191, 153))

        self.pineapple_img.set_colorkey((255, 255, 255))
        self.rectangle_img.set_colorkey((255, 255, 255))

        self.table_borders_surface = pygame.Surface((1920, 1080))
        self.table_borders_surface.fill((255, 255, 255))
        self.table_borders_surface.blit(self.table_img, (0, 0))
        self.table_surface = pygame.Surface((1920, 1080))
        self.table_surface.blit(self.table_img, (0, 0))
        pygame.transform.threshold(self.table_borders_surface, self.table_surface, (29, 36, 48), (40, 40, 40, 0), (255, 255, 255), 1, None, True)
        self.table_borders_surface.set_colorkey((255, 255, 255))

        pygame.mixer.music.load('data/music/BattleLoop2.ogg')
        pygame.mixer.music.play(-1)

        self.default_reel1 = [Tile(350, 675 - i * 200, self.pineapple_img, 1, self.display, "pineapple") for i in range (50)]
        self.default_reel2 = [Tile(604, 675 - i * 200, self.pineapple_img, 2, self.display, "pineapple") for i in range (50)]
        self.default_reel3 = [Tile(858, 675 - i * 200, self.pineapple_img, 3, self.display, "pineapple") for i in range (50)]
        self.default_reel4 = [Tile(1112, 675 - i * 200, self.pineapple_img, 4, self.display, "pineapple") for i in range (50)]
        self.default_reel5 = [Tile(1366, 675 - i * 200, self.pineapple_img, 5, self.display, "pineapple") for i in range (50)]

        self.reel1 = [Tile(350, 675 - i * 200, self.pi_img, 1, self.display, "pineapple") for i in range(50)]
        self.reel2 = [Tile(604, 675 - i * 200, self.mi_img, 2, self.display, "pineapple") for i in range(50)]
        self.reel3 = [Tile(858, 675 - i * 200, self.omega_img, 3, self.display, "pineapple") for i in range(50)]
        self.reel4 = [Tile(1112, 675 - i * 200, self.alfa_img, 4, self.display, "pineapple") for i in range(50)]
        self.reel5 = [Tile(1366, 675 - i * 200, self.beta_img, 5, self.display, "pineapple") for i in range(50)]

        self.default_reels = [self.default_reel1, self.default_reel2, self.default_reel3, self.default_reel4, self.default_reel5]
        self.reels = [self.reel1, self.reel2, self.reel3, self.reel4, self.reel5]

        self.display_rect = pygame.Rect(345, 270, 1330, 600)

        self.velocity = 0
        self.rebound_velocity = 0
        self.spin = False
        self.spinning = False
        self.payout = False
        self.frame_counter = 0

        self.casino = Payout()

    def game_loop(self):

        while self.playing:

            self.check_events()
            if self.START_KEY:
                self.playing = False
            self.display.fill(self.BLACK)

            self.display.blit(self.background_img, (0, 0))
            self.display.blit(self.table_img, (0, 0))

            if self.spin == True and self.spinning == False:
                self.velocity = 100
                self.spinning = True

            collisions = []

            for reel in self.reels:
                for tile in reel:
                    if self.display_rect.colliderect(tile.get_rect()):
                        collisions.append(tile)
                        tile.draw()

            if self.velocity > 0:
                for reel in self.reels:
                    for tile in reel:
                        tile.move(self.velocity)
                self.velocity -= 1

            if self.velocity == 0:
                if self.spin:
                    _, list_tile_y = collisions[0].get_position()
                    y_difference = 675 - list_tile_y
                    if y_difference != 0:
                        self.rebound_velocity = y_difference
                    self.spin = False

            if self.rebound_velocity != 0:
                if self.frame_counter < 10:
                    for reel in self.reels:
                        for tile in reel:
                            move_amount = self.rebound_velocity
                            tile.move(move_amount / 10)
                    self.frame_counter += 1
                else:
                    self.rebound_velocity = 0
                    self.frame_counter = 0
                    self.spinning = False
                    self.payout = True

            if self.payout == True:
                _, y_pos_last = collisions[0].get_position()
                tiles_passed = 0
                for tile in self.reels[0]:
                    _, y_pos = tile.get_position()
                    if y_pos_last < y_pos:
                        tiles_passed += 1
                
                for i in range(len(self.reels)):
                    new_reel = self.default_reels[i][4:]
                    for j in range(len(new_reel)):
                        new_reel[j].set_position(675 - j * 200)
                        self.reels[i] = new_reel

                collisions_matrix = []
                for i in range(3):
                    row = []
                    for j in range(5):
                        row.append(collisions[j*3 + i].get_type())
                    collisions_matrix.append(row)

                self.casino.setFruitsState(collisions_matrix)
                self.casino.calculateWinnings()
                print(f'igrac ima novca: {self.casino.player_money}')

                self.payout = False

            self.display.blit(self.table_borders_surface, (0, 0))

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_m:
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.fadeout(1000)
                        else:
                            pass
                            # pygame.mixer.music.play()
                    if event.key == K_SPACE:
                        self.spin = self.casino.payToMachine(self.casino.money_invested)
                if event.type == MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    print(f'mouse x je {mx}')
                    print(f'mouse y je {my}')

            self.display.blit(self.table_borders_surface, (0, 0))

            if self.spin_button.draw(self.display):
                self.spin = self.casino.payToMachine(self.casino.money_invested)

            if self.autostart_button.draw(self.display):
                while self.casino.spins>0:
                    self.casino.spins = self.casino.spins-1
                    self.spin = self.casino.payToMachine(self.casino.money_invested)

            if self.lines_button.draw(self.display):
                print("Clicked")

            if self.betmax_button.draw(self.display):
                self.casino.money_invested=self.casino.betmax

            if self.return_button.draw(self.display):
                self.curr_menu = self.main_menu
                self.playing = False

            if self.sound:
                if self.soundon_button.draw(self.display):
                   self.sound= False
                   pygame.mixer.music.stop()

            else:
                if self.soundoff_button.draw(self.display):
                    self.sound = True
                    pygame.mixer.music.play(-1)

            self.display.blit(self.lines1_img,(200,900))
            self.display.blit(self.totalbet_img,(450,900))
            self.draw_text(str(self.casino.money_invested), 45, 580, 970)
            self.display.blit(self.won_img,(1210,900))
            self.display.blit(self.credits1_img,(1445,900))
            self.draw_text(str(self.casino.player_money), 45, 1550, 970)
            self.display.blit(self.spins_img, (1680, 905))
            self.draw_text(str(self.casino.spins), 45, 1800, 970)

            self.window.blit(pygame.transform.scale(self.display, (self.DISPLAY_W, self.DISPLAY_H)), (0, 0))
            pygame.display.update()
            self.clock.tick(120)

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True


class Tile():

    def __init__(self, x, y, img, reel, display, tile_type):
        self.x = x
        self.y = y
        self.img = img
        self.reel = reel
        self.display = display
        self.tile_type = tile_type
        self.rectangle_img = pygame.image.load('data/images/rectangle.png')
        self.rectangle_img.set_colorkey((255, 255, 255))

    def move(self, velocity):
        self.y += velocity

    def draw(self):
        self.display.blit(self.rectangle_img, (self.x, self.y))
        self.display.blit(self.img, (self.x + 5, self.y + 15))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

    def get_reel(self):
        return self.reel

    def get_position(self):
        return self.x, self.y

    def set_position(self, y):
        self.y = y

    def get_type(self):
        return self.tile_type

class Payout(object):

    def __init__(self):
        self.fruits = None
        self.array = None
        # TODO moze i u konstruktoru
        self.player_money = 100.0
        self.start_bank_money = 10000.0
        self.spins=10
        self.betmax=5

        self.bank_money = self.start_bank_money

        self.special_symbol = None
        self.free_bets = 0.0
        self.active_special = False
        self.fixed = False

        self.money_invested = 0.0
    
    def get_random_element(self, number):
        if number == 0:
            return "alfa"
        if number == 1:
            return "beta"
        if number == 2:
            return "mi"
        if number == 3:
            return "omega"
        if number == 4:
            return "pi"
        if number == 5:
            return "apple"
        if number == 6:
            return "pineapple"
        if number == 7:
            return "banana"
        if number == 8:
            return "vine"
        if number == 9:
            return "monkey"
        if number == 10:
            return "pyramid"

    def fix_columns(self, symbol, length):
        for i in range(3):
            for j in range(5):
                if j < length:
                    self.fruits[i][j] = symbol
    

    def calculate_best_from_begginging(self, row):
        current_el = row[0]
        length = len(row)

        max_length = 1
        for j in range(1, length):
            if current_el == 'pyramid':
                max_length += 1
                if row[j] != 'pyramid':
                    current_el = row[j]
            elif current_el == row[j] or row[j] == 'pyramid':
                    max_length += 1

        # check for pyramids
        pyramid_count = 0
        for element in row:
            if element == 'pyramid':
                pyramid_count += 1
        if pyramid_count >= 3:
            self.free_bets += 10
            self.special_symbol = self.get_random_element(random.randint(10))
            return True, self.evaluate(current_el, max_length)

        return False, self.evaluate(current_el, max_length)
    
    def calculate_fix(self, row):
        current_el = row[0]
        length = len(row)

        max_length = 1
        for j in range(1, length):
            if current_el == 'pyramid':
                max_length += 1
                if row[j] != 'pyramid':
                    current_el = row[j]
            elif current_el == row[j] or row[j] == 'pyramid':
                    max_length += 1

        return self.evaluate(self.special_symbol, max_length)
               
    def calculate_special_best_from_begginning(self, row):
        current_el = row[0]
        length = len(row)

        max_length = 1
        for j in range(1, length):
            if current_el == 'pyramid':
                max_length += 1
                if row[j] != 'pyramid':
                    current_el = row[j]
            elif current_el == row[j] or row[j] == 'pyramid':
                    max_length += 1

        pyramid_count = 0
        for element in row:
            if element == 'pyramid':
                pyramid_count += 1
        if pyramid_count >= 3 and self.fixed != True:
            self.free_bets += 10

        if current_el == self.special_symbol and max_length >= 3 and self.fixed != True:
            self.fix_columns(self.special_symbol, max_length)
            self.fixed = True
            return self.fixed,
            
    def setFruitsState(self, fruits):
        self.fruits = fruits
        array = []
        for row in self.fruits:
            for element in row:
                array.append(element)
        self.array = array

    def evaluate(self, element:string, length:string):
        winnings = 0.0
        if element == 'alfa':
            if length == 3:
                winnings = 0.50
            if length == 4:
                winnings = 5.00
            if length == 5:
                winnings = 10.0
        
        if element == 'beta':
            if length == 3:
                winnings = 0.5
            if length == 4:
                winnings = 5.0
            if length == 5:
                winnings = 12.50

        if element == 'mi':
            if length == 3:
                winnings = 0.50
            if length == 4:
                winnings = 5.0
            if length == 5:
                winnings = 15.0

        if element == 'omega':
            if length == 3:
                winnings = 0.8
            if length == 4:
                winnings = 6.0
            if length == 5:
                winnings = 20.0

        if element == 'pi':
            if length == 3:
                winnings = 0.8
            if length == 4:
                winnings = 6.0
            if length == 5:
                winnings = 25.0

        if element == 'apple':
            if length == 2:
                winnings = 0.2
            if length == 3:
                winnings = 1.0
            if length == 4:
                winnings = 7.0
            if length == 5:
                winnings = 50.0

        if element == 'pineapple':
            if length == 2:
                winnings = 0.30
            if length == 3:
                winnings = 1.2
            if length == 4:
                winnings = 7.5
            if length == 5:
                winnings = 75.0

        if element == 'banana':
            if length == 2:
                winnings = 0.4
            if length == 3:
                winnings = 1.4
            if length == 4:
                winnings = 8.0
            if length == 5:
                winnings = 100.0

        if element == 'vine':
            if length == 2:
                winnings = 0.5
            if length == 3:
                winnings = 1.6
            if length == 4:
                winnings = 9.0
            if length == 5:
                winnings = 150.0

        if element == 'monkey':
            if length == 2:
                winnings = 1.0
            if length == 3:
                winnings = 2.0
            if length == 4:
                winnings = 10.0
            if length == 5:
                winnings = 500.0
        
        if element == 'pyramid':
            if length == 2:
                winnings = 1.0
            if length == 3:
                winnings = 2.0
            if length == 4:
                winnings = 10.0
            if length == 5:
                winnings = 500.0   
        
        return winnings * self.money_invested

    def calculate_fixed_winnings(self):
        winnings = 0.0
        for row in self.fruits:
            winnings += self.calculate_fix(row)

        # no 4
        pom_list = [self.array[0], self.array[6], self.array[12], self.array[8], self.array[4]]
        winnings += self.calculate_fix(pom_list)

        # no 5
        pom_list = [self.array[10], self.array[6], self.array[2], self.array[8], self.array[14]]
        winnings += self.calculate_fix(pom_list)
       
        # no 6
        pom_list = [self.array[0], self.array[6], self.array[2], self.array[8], self.array[4]]
        winnings += self.calculate_fix(pom_list)

        # no 7
        pom_list = [self.array[5], self.array[11], self.array[7], self.array[13], self.array[9]]
        winnings += self.calculate_fix(pom_list)

        # no 8
        pom_list = [self.array[5], self.array[1], self.array[7], self.array[3], self.array[9]]
        winnings += self.calculate_fix(pom_list)

        # no 9
        pom_list = [self.array[10], self.array[6], self.array[12], self.array[8], self.array[14]]
        winnings += self.calculate_fix(pom_list)

        # no 10
        pom_list = [self.array[0], self.array[6], self.array[12], self.array[13], self.array[14]]
        winnings += self.calculate_fix(pom_list)

        self.payToPlayer(winnings)

    def calculateWinnings(self):
        if self.active_special == False:
            money_invested = self.money_invested
            # provera reel-ova, obraditi self.fruits i self.array
    
            # horizontalni #no 1, 2, 3
            best_special = None
            winnings = 0.0
            for row in self.fruits:
                special, win = self.calculate_best_from_begginging(row)
                winnings += win
                if special == True:
                    best_special = True
    
            # no 4
            pom_list = [self.array[0], self.array[6], self.array[12], self.array[8], self.array[4]]
            special, win = self.calculate_best_from_begginging(pom_list)
            winnings += win
            if special == True:
                best_special = True
            
            # no 5
            pom_list = [self.array[10], self.array[6], self.array[2], self.array[8], self.array[14]]
            special, win = self.calculate_best_from_begginging(pom_list)
            winnings += win
            if special == True:
                best_special = True
    
            # no 6
            pom_list = [self.array[0], self.array[6], self.array[2], self.array[8], self.array[4]]
            special, win = self.calculate_best_from_begginging(pom_list)
            winnings += win
            if special == True:
                best_special = True
    
            # no 7
            pom_list = [self.array[5], self.array[11], self.array[7], self.array[13], self.array[9]]
            special ,win = self.calculate_best_from_begginging(pom_list)
            winnings += win
            if special == True:
                best_special = True
    
            # no 8
            pom_list = [self.array[5], self.array[1], self.array[7], self.array[3], self.array[9]]
            special, win = self.calculate_best_from_begginging(pom_list)
            winnings += win
            if special == True:
                best_special = True
    
            # no 9
            pom_list = [self.array[10], self.array[6], self.array[12], self.array[8], self.array[14]]
            special, win = self.calculate_best_from_begginging(pom_list)
            winnings += win
            if special == True:
                best_special = True
    
            # no 10
            pom_list = [self.array[0], self.array[6], self.array[12], self.array[13], self.array[14]]
            special , winnings = self.calculate_best_from_begginging(pom_list)
            winnings += win
            if special == True:
                best_special = True
    
            self.payToPlayer(winnings)
    
            if best_special != None:
                self.active_special = True

        if self.active_special == True:
            self.free_bets -=  1
            # provera reel-ova, obraditi self.fruits i self.array
    
            # horizontalni #no 1, 2, 3
            winnings = 0.0
            for row in self.fruits:
                special, win = self.calculate_best_from_begginging(row)
                winnings += win
                if special == True:
                    best_special = True
    
            # no 4
            pom_list = [self.array[0], self.array[6], self.array[12], self.array[8], self.array[4]]
            special, win = self.calculate_best_from_begginging(pom_list)
            winnings += win
            if special == True:
                best_special = True
            
            # no 5
            pom_list = [self.array[10], self.array[6], self.array[2], self.array[8], self.array[14]]
            special, win = self.calculate_best_from_begginging(pom_list)
            winnings += win
            if special == True:
                best_special = True
    
            # no 6
            pom_list = [self.array[0], self.array[6], self.array[2], self.array[8], self.array[4]]
            special, win = self.calculate_best_from_begginging(pom_list)
            winnings += win
            if special == True:
                best_special = True
    
            # no 7
            pom_list = [self.array[5], self.array[11], self.array[7], self.array[13], self.array[9]]
            special ,win = self.calculate_best_from_begginging(pom_list)
            winnings += win
            if special == True:
                best_special = True
    
            # no 8
            pom_list = [self.array[5], self.array[1], self.array[7], self.array[3], self.array[9]]
            special, win = self.calculate_best_from_begginging(pom_list)
            winnings += win
            if special == True:
                best_special = True
    
            # no 9
            pom_list = [self.array[10], self.array[6], self.array[12], self.array[8], self.array[14]]
            special, win = self.calculate_best_from_begginging(pom_list)
            winnings += win
            if special == True:
                best_special = True
    
            # no 10
            pom_list = [self.array[0], self.array[6], self.array[12], self.array[13], self.array[14]]
            special , winnings = self.calculate_best_from_begginging(pom_list)
            winnings += win
            if special == True:
                best_special = True
    
            self.payToPlayer(winnings)
            # TODO calculate winnings

            if self.free_bets == 0:
                self.active_special = False

    def payToMachine(self, money) -> Boolean:
        if self.free_bets > 0:
            self.free_bets -= 1
            # TODO mozda ce biti bag, ako ima free betove, mora da se uzima previously, odnosno da mu se onesposobi da menja
            return True 
        if self.player_money >= 0.0:
            self.player_money -= money
            self.bank_money += money
            self.money_invested = money
            return True
        else:
            return False

    def payToPlayer(self, money):
        self.player_money += money
    
    def calculateRTP(self):
        pass

