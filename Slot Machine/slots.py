from ast import Str
import itertools
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
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

        self.background_img = pygame.image.load('data/images/background.png')
        self.table_img = pygame.image.load('data/images/table.png')
        self.table_borders_img = pygame.image.load('data/images/table_borders.png')
        self.pineapple_img = pygame.image.load('data/images/pineapple.png')
        self.rectangle_img = pygame.image.load('data/images/rectangle.png')

        self.spin_img = pygame.image.load('./data/images/spinbutton.png')
        # self.options_img = pygame.image.load('./data/images/options.png').convert_alpha()
        # self.credits_img = pygame.image.load('./data/images/credits.png').convert_alpha()

        self.spin_button = button.Button(1920/2-self.spin_img.get_width()/2, 840, self.spin_img, 1)
        # self.options_button = button.Button(self.optionsx, self.optionsy, self.options_img, 2)
        # self.credits_button = button.Button(self.creditsx, self.creditsy, self.credits_img, 2)

        self.pineapple_img.set_colorkey((255, 255, 255))
        self.rectangle_img.set_colorkey((255, 255, 255))

        self.table_borders_surface = pygame.Surface((1920, 1080))
        self.table_borders_surface.fill((255, 255, 255))
        self.table_borders_surface.blit(self.table_img, (0, 0))
        self.table_surface = pygame.Surface((1920, 1080))
        self.table_surface.blit(self.table_img, (0, 0))
        pygame.transform.threshold(self.table_borders_surface, self.table_surface, (29, 36, 48), (40, 40, 40, 0), (255, 255, 255), 1, None, True)
        self.table_borders_surface.set_colorkey((255, 255, 255))

        #pygame.mixer.music.load('data/audio/music.wav')

        self.default_reel1 = [Tile(350, 675 - i * 200, self.pineapple_img, 1, self.display, "pineapple") for i in range (50)]
        self.default_reel2 = [Tile(604, 675 - i * 200, self.pineapple_img, 2, self.display, "pineapple") for i in range (50)]
        self.default_reel3 = [Tile(858, 675 - i * 200, self.pineapple_img, 3, self.display, "pineapple") for i in range (50)]
        self.default_reel4 = [Tile(1112, 675 - i * 200, self.pineapple_img, 4, self.display, "pineapple") for i in range (50)]
        self.default_reel5 = [Tile(1366, 675 - i * 200, self.pineapple_img, 5, self.display, "pineapple") for i in range (50)]

        self.reel1 = [Tile(350, 675 - i * 200, self.pineapple_img, 1, self.display, "pineapple") for i in range(50)]
        self.reel2 = [Tile(604, 675 - i * 200, self.pineapple_img, 2, self.display, "pineapple") for i in range(50)]
        self.reel3 = [Tile(858, 675 - i * 200, self.pineapple_img, 3, self.display, "pineapple") for i in range(50)]
        self.reel4 = [Tile(1112, 675 - i * 200, self.pineapple_img, 4, self.display, "pineapple") for i in range(50)]
        self.reel5 = [Tile(1366, 675 - i * 200, self.pineapple_img, 5, self.display, "pineapple") for i in range(50)]

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
                        self.spin = self.casino.payToMachine(1)
                if event.type == MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    print(mx)
                    print(my)

            self.display.blit(self.table_borders_surface, (0, 0))

            if self.spin_button.draw(self.display):
                self.spin = self.casino.payToMachine(1)

            self.window.blit(pygame.transform.scale(self.display, (self.DISPLAY_W, self.DISPLAY_H)), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

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

    def move(self, velocity):
        self.y += velocity

    def draw(self):
        self.display.blit(self.img, (self.x, self.y))
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

        self.bank_money = self.start_bank_money
        self.money_invested = 0.0

    def calculate_best(row):
        length = len(row)
        max_winnings, winnings = 0.0 , 0.0

        for i in range(length):
            current_length = 0
            for j in range(i, length):
                if row[i] == row[j]:
                    current_length += 1
                winnings = Payout.evaluate(row[i] , current_length)
                if winnings > max_winnings:
                    max_winnings = winnings            
        return max_winnings

    def calculate_best_book(row):
        length = len(row)
        max_winnings, winnings = 0.0, 0.0
        current_element = None
        for i in range(length):
            current_element = row[i]
            current_length = 0
            for j in range(i, length):
                if current_element == row[j] or row[j] == 'book':
                    current_length += 1
                    winnings = Payout.evaluate(current_element, current_length)
                    if winnings > max_winnings:
                        max_winnings = winnings
                if current_element == "book":
                    current_length += 1
                    if row[j] != 'book':
                        current_element = row[j]
                    winnings = Payout.evaluate(current_element, current_length)
                    if winnings > max_winnings:
                        max_winnings = winnings
        return max_winnings

    def setFruitsState(self, fruits):
        self.fruits = fruits
        array = []
        for row in self.fruits:
            for element in row:
                array.append(element)
        self.array = array

    def evaluate(element, length):
        # TODO
        return 100


    def calculateWinnings(self):
        money_invested = self.money_invested
        # provera reel-ova, obraditi self.fruits i self.array

        # horizontalni #no 1, 2, 3
        winnings = 0.0
        for row in self.fruits:
            winnings += Payout.calculate_best(row)

        # no 4
        pom_list = [self.array[0], self.array[6], self.array[12], self.array[8], self.array[4]]
        winnings += Payout.calculate_best(pom_list)
        
        # no 5
        pom_list = [self.array[10], self.array[6], self.array[2], self.array[8], self.array[14]]
        winnings += Payout.calculate_best(pom_list)

        # no 6
        pom_list = [self.array[0], self.array[6], self.array[2], self.array[8], self.array[4]]
        winnings += Payout.calculate_best(pom_list)

        # no 7
        pom_list = [self.array[5], self.array[11], self.array[7], self.array[13], self.array[9]]
        winnings += Payout.calculate_best(pom_list)

        # no 8
        pom_list = [self.array[5], self.array[1], self.array[7], self.array[3], self.array[9]]
        winnings += Payout.calculate_best(pom_list)

        # no 9
        pom_list = [self.array[10], self.array[6], self.array[12], self.array[8], self.array[14]]
        winnings += Payout.calculate_best(pom_list)

        # no 10
        pom_list = [self.array[0], self.array[6], self.array[12], self.array[13], self.array[14]]
        winnings += Payout.calculate_best(pom_list)

        self.payToPlayer(winnings)        

    def payToMachine(self, money) -> Boolean:
        if self.player_money >= 0.0:
            self.player_money -= money
            self.bank_money += money
            self.money_invested = money
            # pozvati spin ukoliko ovo ima novca ili ovde ili u main-u
            return True
        else:
            return False

    def payToPlayer(self, money):
        self.player_money += money
    
    def calculateRTP(self):
        pass

