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
        self.startx, self.starty = self.mid_w - 210, 230

        self.creditsx, self.creditsy = self.mid_w - 220, 380

        self.background_img = pygame.image.load('./data/images/background.png')
        self.background_img = pygame.transform.scale(self.background_img,(game.DISPLAY_W,game.DISPLAY_H))

        self.startgame_img = pygame.image.load('./data/images/start.png').convert_alpha()

        self.credits_img = pygame.image.load('./data/images/credits.png').convert_alpha()

        self.startgame_button = button.Button(self.startx, self.starty, self.startgame_img, 2)

        self.credits_button = button.Button(self.creditsx, self.creditsy, self.credits_img, 2)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()

            self.game.display.fill(self.game.BLACK)
            self.game.display.blit(self.background_img, (0, 0))
            self.game.draw_text('Main Menu', 100, self.game.DISPLAY_W / 2, 100)
            if self.startgame_button.draw(self.game.display):
                self.game.playing = True
                self.run_display = False

            if self.credits_button.draw(self.game.display):
                self.game.curr_menu = self.game.credits
                self.run_display = False

            self.blit_screen()

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.background_img = pygame.image.load('./data/images/background.png')
        self.background_img = pygame.transform.scale(self.background_img, (game.DISPLAY_W, game.DISPLAY_H))
        self.return_img = pygame.image.load('./data/images/return.png')
        self.return_button = button.Button(60, 30, self.return_img, 0.1)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.game.display.fill(self.game.BLACK)
            self.game.display.blit(self.background_img, (0, 0))
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False

            if self.return_button.draw(self.game.display):
                self.game.curr_menu = self.game.main_menu
                self.run_display= False


            self.game.draw_text('Credits', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('sound icons= https://www.flaticon.com/free-icons/sound', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.game.draw_text('https://www.flaticon.com/free-icons/mute', 15, self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2 + 30)


            self.blit_screen()
