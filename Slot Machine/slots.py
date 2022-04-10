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
        self.win_lines = [False for i in range(10)]

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
        self.soundoff_img = pygame.image.load('./data/images/mute.png')
        self.return_img = pygame.image.load('./data/images/return.png')
        self.title_img = pygame.image.load('./data/images/title.png')
        self.sound=True
        self.lines=False

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
        self.jungle_img = pygame.image.load('data/images/jungle.png')
        self.jungle_img = pygame.transform.scale(self.jungle_img, (191, 153))
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

        self.default_reel1 = []
        self.default_reel2 = []
        self.default_reel3 = []
        self.default_reel4 = []
        self.default_reel5 = []

        self.default_reels = [self.default_reel1, self.default_reel2, self.default_reel3, self.default_reel4, self.default_reel5]


        self.reel1_numbers = [3, 4, 5, 8, 6, 3, 4, 8, 1, 2, 4, 4, 9, 5, 2, 7, 5, 3, 5, 1, 10, 1, 3, 6, 2, 10, 7, 9, 0,
                              10]
        self.reel2_numbers = [10, 0, 3, 3, 2, 5, 9, 6, 6, 10, 5, 9, 4, 0, 2, 7, 1, 7, 2, 5, 1, 8, 4, 9, 8, 2, 10, 3, 4,
                              4]
        self.reel3_numbers = [4, 8, 10, 5, 3, 4, 3, 5, 6, 3, 0, 10, 8, 5, 8, 9, 3, 4, 9, 5, 7, 1, 1, 7, 2, 2, 4, 1, 6,
                              2]
        self.reel4_numbers = [3, 4, 9, 1, 5, 7, 2, 5, 0, 9, 2, 3, 4, 10, 0, 5, 4, 2, 1, 10, 8, 8, 7, 3, 6, 10, 2, 9, 5,
                              6]
        self.reel5_numbers = [3, 4, 5, 8, 6, 3, 4, 8, 1, 2, 4, 4, 9, 5, 2, 7, 5, 3, 5, 1, 10, 1, 3, 6, 2, 10, 7, 9, 0,
                              10]

        self.reel_numbers = [self.reel1_numbers, self.reel2_numbers, self.reel3_numbers, self.reel4_numbers,
                             self.reel5_numbers]

        for i in range(len(self.reel_numbers)):
            reel_tmp = []
            for j in range(4):
                reel_tmp += self.reel_numbers[i]
            self.reel_numbers[i] = reel_tmp

        # for i in range(len(self.reel_numbers)):
        #     for j in range(len((self.reel_numbers[i]))):
        #         if self.reel_numbers[i][j] == 0:
        #             self.default_reels[i].append(
        #                 Tile(350 + i * 254, 675 - j * 200, self.pyramid_img, i, self.display, "pyramid"))
        #         if self.reel_numbers[i][j] == 1:
        #             self.default_reels[i].append(
        #                 Tile(350 + i * 254, 675 - j * 200, self.pyramid_img, i, self.display, "pyramid"))
        #         if self.reel_numbers[i][j] == 2:
        #             self.default_reels[i].append(
        #                 Tile(350 + i * 254, 675 - j * 200, self.jungle_img, i, self.display, "jungle"))
        #         if self.reel_numbers[i][j] == 3:
        #             self.default_reels[i].append(
        #                 Tile(350 + i * 254, 675 - j * 200, self.pyramid_img, i, self.display, "pyramid"))
        #         if self.reel_numbers[i][j] == 4:
        #             self.default_reels[i].append(Tile(350 + i * 254, 675 - j * 200, self.pyramid_img, i, self.display, "pyramid"))
        #         if self.reel_numbers[i][j] == 5:
        #             self.default_reels[i].append(
        #                 Tile(350 + i * 254, 675 - j * 200, self.pyramid_img, i, self.display, "pyramid"))
        #         if self.reel_numbers[i][j] == 6:
        #             self.default_reels[i].append(
        #                 Tile(350 + i * 254, 675 - j * 200, self.jungle_img, i, self.display, "jungle"))
        #         if self.reel_numbers[i][j] == 7:
        #             self.default_reels[i].append(
        #                 Tile(350 + i * 254, 675 - j * 200, self.jungle_img, i, self.display, "jungle"))
        #         if self.reel_numbers[i][j] == 8:
        #             self.default_reels[i].append(Tile(350 + i * 254, 675 - j * 200, self.jungle_img, i, self.display, "jungle"))
        #         if self.reel_numbers[i][j] == 9:
        #             self.default_reels[i].append(
        #                 Tile(350 + i * 254, 675 - j * 200, self.jungle_img, i, self.display, "jungle"))
        #         if self.reel_numbers[i][j] == 10:
        #             self.default_reels[i].append(
        #                 Tile(350 + i * 254, 675 - j * 200, self.pyramid_img, i, self.display, "pyramid"))

        for i in range(len(self.reel_numbers)):
            for j in range(len((self.reel_numbers[i]))):
                if self.reel_numbers[i][j] == 0:
                    self.default_reels[i].append(
                        Tile(350 + i * 254, 675 - j * 200, self.pyramid_img, i, self.display, "pyramid"))
                if self.reel_numbers[i][j] == 1:
                    self.default_reels[i].append(
                        Tile(350 + i * 254, 675 - j * 200, self.monkey_img, i, self.display, "monkey"))
                if self.reel_numbers[i][j] == 2:
                    self.default_reels[i].append(
                        Tile(350 + i * 254, 675 - j * 200, self.jungle_img, i, self.display, "jungle"))
                if self.reel_numbers[i][j] == 3:
                    self.default_reels[i].append(
                        Tile(350 + i * 254, 675 - j * 200, self.banana_img, i, self.display, "banana"))
                if self.reel_numbers[i][j] == 4:
                    self.default_reels[i].append(Tile(350 + i * 254, 675 - j * 200, self.pi_img, i, self.display, "pi"))
                if self.reel_numbers[i][j] == 5:
                    self.default_reels[i].append(
                        Tile(350 + i * 254, 675 - j * 200, self.omega_img, i, self.display, "omega"))
                if self.reel_numbers[i][j] == 6:
                    self.default_reels[i].append(
                        Tile(350 + i * 254, 675 - j * 200, self.pineapple_img, i, self.display, "pineapple"))
                if self.reel_numbers[i][j] == 7:
                    self.default_reels[i].append(
                        Tile(350 + i * 254, 675 - j * 200, self.apple_img, i, self.display, "apple"))
                if self.reel_numbers[i][j] == 8:
                    self.default_reels[i].append(Tile(350 + i * 254, 675 - j * 200, self.mi_img, i, self.display, "mi"))
                if self.reel_numbers[i][j] == 9:
                    self.default_reels[i].append(
                        Tile(350 + i * 254, 675 - j * 200, self.beta_img, i, self.display, "beta"))
                if self.reel_numbers[i][j] == 10:
                    self.default_reels[i].append(
                        Tile(350 + i * 254, 675 - j * 200, self.alfa_img, i, self.display, "alfa"))

        self.reel1 = []
        self.reel2 = []
        self.reel3 = []
        self.reel4 = []
        self.reel5 = []
        self.reels = [self.reel1, self.reel2, self.reel3, self.reel4, self.reel5]

        for i in range(len(self.reels)):
            for k in range(len(self.default_reels[0])):
                self.reels[i].append(self.default_reels[i][k])

        self.display_rect = pygame.Rect(345, 270, 1330, 550)

        self.index = [0, 0, 0, 0, 0]
        self.velocity = [0, 0, 0, 0, 0]
        self.rebound_velocity = [0, 0, 0, 0, 0]
        self.spin = False
        self.spinning = False
        self.payout = False
        self.frame_counter = [0, 0, 0, 0, 0]
        self.frame_counter_counter = 0
        self.velocities_0_counter = 0
        self.coins = [1,5,10,20,50]
        self.coinsi=0
        self.casino = Payout(self)


    def show_special_element(self, symbol, indexes):
        column0 = [(350, 675) ,  (350, 475) , (350, 275)]
        column1 = [(604, 675) , (604, 475) , (604, 275)]
        column2 = [(858, 675) , (858, 475) , (858, 275)]
        column3 = [(1112, 675), (1112, 475), (1112, 275)]
        column4 = [(1366, 675), (1366, 475), (1366, 275)]

        path = f'./data/images/{symbol}.png'
        surface = pygame.image.load(path)

        for i in indexes:
            if i == 0:
                for position in column0:
                    self.display.blit(surface, position)
            if i == 1:
                for position in column1:
                    self.display.blit(surface, position)
            if i == 2:
                for position in column2:
                    self.display.blit(surface, position)
            if i == 3:
                for position in column3:
                    self.display.blit(surface, position)
            if i == 4:
                for position in column4:
                    self.display.blit(surface, position)

    def game_loop(self):

        while self.playing:

            self.check_events()
            if self.START_KEY:
                self.playing = False
            self.display.fill(self.BLACK)

            self.display.blit(self.background_img, (0, 0))
            self.display.blit(self.table_img, (0, 0))
            self.display.blit(self.title_img, (0, 0))

            if self.spin == False and self.spinning == False and self.casino.free_bets > 0:
                self.spin = self.casino.payToMachine(self.casino.money_invested)

            if self.spin == True and self.spinning == False:
                velocities = [100, 110, 120, 130, 140, 150]
                for i in range(5):
                    self.velocity[i] = random.choice(velocities)
                self.spinning = True
                self.frame_counter_counter = 0
                self.velocities_0_counter = 0

            collisions = []

            for reel in self.reels:
                for tile in reel:
                    if self.display_rect.colliderect(tile.get_rect()):
                        collisions.append(tile)
                        tile.draw()

            for (i, velocity) in enumerate(self.velocity):
                if velocity > 0:
                    for tile in self.reels[i]:
                        tile.move(velocity)
                self.velocity[i] -= 2.5

                if velocity == 0:
                    self.velocities_0_counter += 1
                    if self.spin:
                        list_tiles_y = []
                        last_list_tile_x = None
                        for j in range(len(collisions)):
                            list_tile_x, list_tile_y = collisions[j].get_position()
                            if list_tile_x != last_list_tile_x:
                                last_list_tile_x = list_tile_x
                                list_tiles_y.append(list_tile_y)
                        y_differences = []
                        for k in range(len(list_tiles_y)):
                            y_differences.append(675 - list_tiles_y[k])
                        if y_differences[i] != 0:
                            self.rebound_velocity[i] = y_differences[i]
                        if self.velocities_0_counter == 5:
                            self.spin = False

            for (i, rebound_velocity) in enumerate(self.rebound_velocity):
                if rebound_velocity != 0:
                    if self.frame_counter[i] < 10:
                        reel = self.reels[i]
                        for tile in reel:
                            move_amount = rebound_velocity
                            tile.move(move_amount / 10)
                        self.frame_counter[i] += 1
                    else:
                        self.frame_counter_counter += 1
                        self.rebound_velocity[i] = 0
                        self.frame_counter[i] = 0
                        if self.frame_counter_counter == 5:
                            self.spinning = False
                            self.payout = True

            if self.payout == True:
                y_pos_lasts = []
                last_x_pos = []
                for i in range(len(collisions)):
                    x_pos_last, y_pos_last = collisions[i].get_position()
                    if x_pos_last != last_x_pos:
                        last_x_pos = x_pos_last
                        y_pos_lasts.append(y_pos_last)
                tiles_passed = [0, 0, 0, 0, 0]
                for (i, reel) in enumerate(self.reels):
                    for tile in reel:
                        _, y_pos = tile.get_position()
                        if y_pos_lasts[i] < y_pos:
                            tiles_passed[i] += 1

                    self.index[i] += tiles_passed[i]
                    self.index[i] = self.index[i] % 30

                for i in range(len(self.reels)):
                    new_reel = self.default_reels[i][self.index[i]:]
                    for j in range(len(new_reel)):
                        new_reel[j].set_position(675 - j * 200)
                        self.reels[i] = new_reel
                
                row1 = [collisions[2].get_type() , collisions[5].get_type() , collisions[8].get_type() , collisions[11].get_type() , collisions[14].get_type()]
                row2 = [collisions[1].get_type() , collisions[4].get_type() , collisions[7].get_type() , collisions[10].get_type() , collisions[13].get_type()]
                row3 = [collisions[0].get_type() , collisions[3].get_type() , collisions[6].get_type() , collisions[9].get_type() , collisions[12].get_type()]

                collisions_matrix = [row1, row2, row3]

                self.casino.setFruitsState(collisions_matrix)
                self.casino.calculateWinnings()
                print(f'igrac ima novca: {self.casino.player_money}')

                self.payout = False

            self.casino.set_reels(self.reels)

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
                    if event.key == K_SPACE and self.spin==False:
                        self.spin = self.casino.payToMachine(self.casino.money_invested)
                        for i in range(10):
                            self.win_lines[i] = False
                if event.type == MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    print(f'mouse  je ({mx},{my})')


            self.display.blit(self.table_borders_surface, (0, 0))

            if self.spin_button.draw(self.display) and self.spin==False:
                for i in range(10):
                    self.win_lines[i]=False
                self.spin = self.casino.payToMachine(self.casino.money_invested)

            if self.autostart_button.draw(self.display) and self.spin==False:
                if self.casino.free_bets>0:
                    self.spincounter = self.casino.free_bets

            if self.lines_button.draw(self.display) and self.spin==False:
                self.lines=~self.lines

            if self.lines:
                pygame.draw.line(self.display, (255, 0, 0), (453, 367), (1461, 367), 8)
                pygame.draw.line(self.display, (255, 0, 0), (453, 572), (1461, 572), 8)
                pygame.draw.line(self.display, (255, 0, 0), (453, 767), (1461, 767), 8)

                pygame.draw.line(self.display, (0, 255, 0), (453, 767), (958, 367), 8)
                pygame.draw.line(self.display, (0, 255, 0), (958, 367), (1461, 767), 8)

                pygame.draw.line(self.display, (0, 0, 255), (453, 367), (958, 767), 8)
                pygame.draw.line(self.display, (0, 0, 255), (958, 767), (1461, 367), 8)

                pygame.draw.line(self.display, (100, 0, 255), (456, 574), (704, 371), 8)
                pygame.draw.line(self.display, (100, 0, 255), (704, 371), (959, 573), 8)
                pygame.draw.line(self.display, (100, 0, 255), (959, 573), (1210, 370), 8)
                pygame.draw.line(self.display, (100, 0, 255), (1210, 370), (1461, 571), 8)

                pygame.draw.line(self.display, (10, 100, 155), (457, 574), (705, 770), 8)
                pygame.draw.line(self.display, (10, 100, 155), (705, 770), (962, 578), 8)
                pygame.draw.line(self.display, (10, 100, 155), (962, 578), (1220, 770), 8)
                pygame.draw.line(self.display, (10, 100, 155), (1220, 770), (1457, 573), 8)

                pygame.draw.line(self.display, (255, 255, 50), (461, 361), (703, 555), 8)
                pygame.draw.line(self.display, (255, 255, 50), (703, 555), (960, 356), 8)
                pygame.draw.line(self.display, (255, 255, 50), (960, 356), (1208, 553), 8)
                pygame.draw.line(self.display, (255, 255, 50), (1208, 553), (1453, 361), 8)

                pygame.draw.line(self.display, (204, 0, 102), (463, 770), (707, 582), 8)
                pygame.draw.line(self.display, (204, 0, 102), (707, 582), (958, 780), 8)
                pygame.draw.line(self.display, (204, 0, 102), (958, 780), (1207, 581), 8)
                pygame.draw.line(self.display, (204, 0, 102), (1207, 581), (1455, 765), 8)

                pygame.draw.line(self.display, (255, 128, 0), (476, 358), (978, 770), 8)
                pygame.draw.line(self.display, (255, 128, 0), (978, 770), (1455, 775), 8)



            for i in range(10):
                if i == 0 and self.win_lines[i]:
                    pygame.draw.line(self.display, (255, 0, 0), (453, 367), (1461, 367), 8)

                elif i == 1 and self.win_lines[i]:
                    pygame.draw.line(self.display, (255, 0, 0), (453, 572), (1461, 572), 8)

                elif i == 2 and self.win_lines[i]:
                    pygame.draw.line(self.display, (255, 0, 0), (453, 767), (1461, 767), 8)

                elif i == 3 and self.win_lines[i]:
                    pygame.draw.line(self.display, (0, 0, 255), (453, 367), (958, 767), 8)
                    pygame.draw.line(self.display, (0, 0, 255), (958, 767), (1461, 367), 8)

                elif i == 4 and self.win_lines[i]:
                    pygame.draw.line(self.display, (0, 255, 0), (453, 767), (958, 367), 8)
                    pygame.draw.line(self.display, (0, 255, 0), (958, 367), (1461, 767), 8)

                elif i == 5 and self.win_lines[i]:
                    pygame.draw.line(self.display, (255, 255, 50), (461, 361), (703, 555), 8)
                    pygame.draw.line(self.display, (255, 255, 50), (703, 555), (960, 356), 8)
                    pygame.draw.line(self.display, (255, 255, 50), (960, 356), (1208, 553), 8)
                    pygame.draw.line(self.display, (255, 255, 50), (1208, 553), (1453, 361), 8)

                elif i == 6 and self.win_lines[i]:
                    pygame.draw.line(self.display, (10, 100, 155), (457, 574), (705, 770), 8)
                    pygame.draw.line(self.display, (10, 100, 155), (705, 770), (962, 578), 8)
                    pygame.draw.line(self.display, (10, 100, 155), (962, 578), (1220, 770), 8)
                    pygame.draw.line(self.display, (10, 100, 155), (1220, 770), (1457, 573), 8)

                elif i == 7 and self.win_lines[i]:
                    pygame.draw.line(self.display, (100, 0, 255), (456, 574), (704, 371), 8)
                    pygame.draw.line(self.display, (100, 0, 255), (704, 371), (959, 573), 8)
                    pygame.draw.line(self.display, (100, 0, 255), (959, 573), (1210, 370), 8)
                    pygame.draw.line(self.display, (100, 0, 255), (1210, 370), (1461, 571), 8)

                elif i == 8 and self.win_lines[i]:
                    pygame.draw.line(self.display, (204, 0, 102), (463, 770), (707, 582), 8)
                    pygame.draw.line(self.display, (204, 0, 102), (707, 582), (958, 780), 8)
                    pygame.draw.line(self.display, (204, 0, 102), (958, 780), (1207, 581), 8)
                    pygame.draw.line(self.display, (204, 0, 102), (1207, 581), (1455, 765), 8)

                elif i == 9 and self.win_lines[i]:
                    pygame.draw.line(self.display, (255, 128, 0), (476, 358), (978, 770), 8)
                    pygame.draw.line(self.display, (255, 128, 0), (978, 770), (1455, 775), 8)




            if self.betmax_button.draw(self.display)and self.spin==False:
                if self.coinsi == 4:
                    self.coinsi=0
                else:
                    self.coinsi+=1
                self.casino.money_invested=self.coins[self.coinsi]

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


            self.display.blit(self.totalbet_img,(450,900))
            self.draw_text(str(self.casino.money_invested), 45, 560, 970)
            self.display.blit(self.won_img,(1210,900))
            self.draw_text(str(round(self.casino.get_current_winnings(), 2)), 45, 1320, 970)
            self.display.blit(self.credits1_img,(1445,900))
            self.draw_text(str(round(self.casino.player_money, 2)), 45, 1550, 970)
            self.display.blit(self.spins_img, (200,900))
            self.draw_text(str(self.casino.free_bets), 45, 310,970)

            self.display.blit(self.title_img, (0, 0))



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

    def set_img(self, img_name):
        path = 'data/images/' + img_name + '.png'
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, (191, 153))
        img.set_colorkey((255, 255, 255))
        self.img = img

class Payout(object):

    def __init__(self,game:Game):
        self.fruits = None
        self.array = None
        # TODO moze i u konstruktoru
        self.player_money = 500.0
        self.start_bank_money = 10000.0
        self.current_winnings = 0.0
        self.spins=10
        self.betmax=5
        self.game=game

        self.bank_money = self.start_bank_money

        self.special_symbol = None
        self.free_bets = 0
        self.active_special = False

        self.money_invested = 1

        self.reels = []

    def set_reels(self, reels):
        self.reels = reels

    def set_current_winnings(self, value):
        self.current_winnings = value
    def get_current_winnings(self):
        return self.current_winnings

    def get_random_element(self, number):
        rand = random.randint(1, 100)
        if rand <= 2:
            return "monkey"
        if rand <= 7:
            return "jungle"
        if rand <= 15:
            return "banana"
        if rand <= 35:
            return "pi"
        if rand <= 55:
            return "omega"
        if rand <= 60:
            return "pineapple"
        if rand <= 65:
            return "apple"
        if rand <= 70:
            return "mi"
        if rand <= 80:
            return "beta"
        if rand <= 100:
            return "alfa"

    def fix_columns(self, symbol, list):
        for  (i,reel) in enumerate(self.reels):
            if list[i]:
                reel[0].set_img(symbol)
                reel[1].set_img(symbol)
                reel[2].set_img(symbol)

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
            else: 
                break
        return self.evaluate(current_el, max_length)

    def check_special_symbol(self, symbol):
        counter = 0
        columns = [False for i in range(5)]
        for i in range(5):
           for j in range(3):
               if self.fruits[j][i] == symbol:
                   columns[i] = True
                   counter += 1
                   break
        return columns, counter
            
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
                winnings = 3.00
            if length == 5:
                winnings = 7.5
        
        if element == 'beta':
            if length == 3:
                winnings = 0.8
            if length == 4:
                winnings = 4.0
            if length == 5:
                winnings = 15.0

        if element == 'mi':
            if length == 3:
                winnings = 0.9
            if length == 4:
                winnings = 4.5
            if length == 5:
                winnings = 20.0

        if element == 'omega':
            if length == 3:
                winnings = 0.1
            if length == 4:
                winnings = 1.0
            if length == 5:
                winnings = 3.0

        if element == 'pi':
            if length == 3:
                winnings = 0.2
            if length == 4:
                winnings = 2.0
            if length == 5:
                winnings = 4.0

        if element == 'apple':
            if length == 3:
                winnings = 3.5
            if length == 4:
                winnings = 20.0
            if length == 5:
                winnings = 400.0

        if element == 'pineapple':
            if length == 3:
                winnings = 4.0
            if length == 4:
                winnings = 25.0
            if length == 5:
                winnings = 500.0

        if element == 'banana':
            if length == 3:
                winnings = 1.5
            if length == 4:
                winnings = 3.0
            if length == 5:
                winnings = 20.0

        if element == 'jungle':
            if length == 3:
                winnings = 3.0
            if length == 4:
                winnings = 10.0
            if length == 5:
                winnings = 100.0

        if element == 'monkey':
            if length == 3:
                winnings = 5.0
            if length == 4:
                winnings = 100.0
            if length == 5:
                winnings = 1800.0
        
        if element == 'pyramid':
            if length == 3:
                winnings = 2.0
            if length == 4:
                winnings = 8.0
            if length == 5:
                winnings = 50.0
        
        return winnings * self.money_invested

    def calculateWinnings(self):
        if self.active_special == False:
            money_invested = self.money_invested
            # provera reel-ova, obraditi self.fruits i self.array

            # horizontalni #no 1, 2, 3
            columns, pyramide_counter = self.check_special_symbol('pyramid')
            if pyramide_counter >= 3:
                self.active_special = True
                self.free_bets = 10
                self.special_symbol = self.get_random_element(random.randint(0, 10))
                print(f'prelazim u special mode sa elementom : {self.special_symbol}')

            winnings = 0.0
            for i,row in enumerate(self.fruits):
                win = self.calculate_best_from_begginging(row)
                if win:
                    self.game.win_lines[i] = True
                winnings += win
    
            # no 4
            pom_list = [self.array[0], self.array[6], self.array[12], self.array[8], self.array[4]]
            win = self.calculate_best_from_begginging(pom_list)
            if win:
                self.game.win_lines[3]=True
            winnings += win
            
            # no 5
            pom_list = [self.array[10], self.array[6], self.array[2], self.array[8], self.array[14]]
            win = self.calculate_best_from_begginging(pom_list)
            if win:
                self.game.win_lines[4]=True

            winnings += win

            # no 6
            pom_list = [self.array[0], self.array[6], self.array[2], self.array[8], self.array[4]]
            win = self.calculate_best_from_begginging(pom_list)
            if win:
                self.game.win_lines[5]=True
            winnings += win
    
            # no 7
            pom_list = [self.array[5], self.array[11], self.array[7], self.array[13], self.array[9]]
            win = self.calculate_best_from_begginging(pom_list)
            if win:
                self.game.win_lines[6]=True
            winnings += win
    
            # no 8
            pom_list = [self.array[5], self.array[1], self.array[7], self.array[3], self.array[9]]
            win = self.calculate_best_from_begginging(pom_list)
            if win:
                self.game.win_lines[7]=True
            winnings += win


            # no 9
            pom_list = [self.array[10], self.array[6], self.array[12], self.array[8], self.array[14]]
            win = self.calculate_best_from_begginging(pom_list)
            if win:
                self.game.win_lines[8]=True
            winnings += win


            # no 10
            pom_list = [self.array[0], self.array[6], self.array[12], self.array[13], self.array[14]]
            win = self.calculate_best_from_begginging(pom_list)
            if win:
                self.game.win_lines[9]=True
            winnings += win
    
            self.payToPlayer(winnings)
    
        elif self.active_special == True:
            # provera reel-ova, obraditi self.fruits i self.array
    
            # horizontalni #no 1, 2, 3
            winnings = 0.0

            fixed_columns_special, special_counter = self.check_special_symbol(self.special_symbol)

            fixed_columns_pyramide, pyramid_counter = self.check_special_symbol("pyramid")

            if pyramid_counter >= 3:
                self.free_bets += 10

            if special_counter >= 3:
                special_winning = 10 * self.evaluate(self.special_symbol, special_counter)
                print(f'{self.special_symbol} se pojavio {special_counter} i dobitak je {special_winning}')
                self.fix_columns(self.special_symbol, fixed_columns_special)
                winnings += special_winning

            for i, row in enumerate(self.fruits):
                win = self.calculate_best_from_begginging(row)
                if win:
                    self.game.win_lines[i] = True
                winnings += win

            pom_list = []
    
            # no 4
            pom_list = [self.array[0], self.array[6], self.array[12], self.array[8], self.array[4]]
            win = self.calculate_best_from_begginging(pom_list)
            if win:
                self.game.win_lines[3] = True
            winnings += win

            # no 5
            pom_list = [self.array[10], self.array[6], self.array[2], self.array[8], self.array[14]]
            win = self.calculate_best_from_begginging(pom_list)
            if win:
                self.game.win_lines[4] = True
            winnings += win
    
            # no 6
            pom_list = [self.array[0], self.array[6], self.array[2], self.array[8], self.array[4]]
            win = self.calculate_best_from_begginging(pom_list)
            if win:
                self.game.win_lines[5] = True
            winnings += win
    
            # no 7
            pom_list = [self.array[5], self.array[11], self.array[7], self.array[13], self.array[9]]
            win = self.calculate_best_from_begginging(pom_list)
            if win:
                self.game.win_lines[6] = True
            winnings += win
    
            # no 8
            pom_list = [self.array[5], self.array[1], self.array[7], self.array[3], self.array[9]]
            win = self.calculate_best_from_begginging(pom_list)
            if win:
                self.game.win_lines[7] = True
            winnings += win
    
            # no 9
            pom_list = [self.array[10], self.array[6], self.array[12], self.array[8], self.array[14]]
            win = self.calculate_best_from_begginging(pom_list)
            if win:
                self.game.win_lines[8] = True
            winnings += win
    
            # no 10
            pom_list = [self.array[0], self.array[6], self.array[12], self.array[13], self.array[14]]
            win = self.calculate_best_from_begginging(pom_list)
            if win:
                self.game.win_lines[9] = True
            winnings += win
    
            self.payToPlayer(winnings)

            if self.free_bets == 0:
                self.special_symbol = None
                self.active_special = False

    def payToMachine(self, money) -> Boolean:
        if self.free_bets > 0:
            self.free_bets -= 1
            # self.calculateWinnings()
            # TODO mozda ce biti bag, ako ima free betove, mora da se uzima previously, odnosno da mu se onesposobi da menja
            return True 
        elif self.player_money - self.money_invested >= 0:
            self.set_current_winnings(0.0)
            self.player_money -= money
            self.bank_money += money
            self.money_invested = money
            return True
        else:
            return False

    def payToPlayer(self, money):
        self.player_money += money
        self.set_current_winnings(money)
    
    def calculateRTP(self):
        pass

