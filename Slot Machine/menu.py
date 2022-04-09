import pygame
import button


class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w - 200, 150
        self.optionsx, self.optionsy = self.mid_w - 200, 300
        self.creditsx, self.creditsy = self.mid_w - 200, 450

        self.background_img = pygame.image.load('./data/images/background.png')
        self.background_img = pygame.transform.scale(self.background_img,(game.DISPLAY_W,game.DISPLAY_H))

        self.startgame_img = pygame.image.load('./data/images/start.png').convert_alpha()
        self.options_img = pygame.image.load('./data/images/options.png').convert_alpha()
        self.credits_img = pygame.image.load('./data/images/credits.png').convert_alpha()

        self.startgame_button = button.Button(self.startx, self.starty, self.startgame_img, 2)
        self.options_button = button.Button(self.optionsx, self.optionsy, self.options_img, 2)
        self.credits_button = button.Button(self.creditsx, self.creditsy, self.credits_img, 2)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()

            self.game.display.fill(self.game.BLACK)
            self.game.display.blit(self.background_img, (0, 0))
            self.game.draw_text('Main Menu', 20, self.game.DISPLAY_W / 2, 100)
            if self.startgame_button.draw(self.game.display):
                self.game.playing = True
                self.run_display = False
            if self.options_button.draw(self.game.display):
                self.game.curr_menu = self.game.options
                self.run_display = False
            if self.credits_button.draw(self.game.display):
                self.game.curr_menu = self.game.credits
                self.run_display = False

            self.blit_screen()


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('Options', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text("Volume", 15, self.volx, self.voly)
            self.game.draw_text("Controls", 15, self.controlsx, self.controlsy)

            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            # TO-DO: Create a Volume Menu and a Controls Menu
            pass


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Credits', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Made by me', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.blit_screen()
