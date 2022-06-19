import pygame, sys
from pygame import *
import random

FPS = 120
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
pygame.init()
pygame.display.set_caption("Turn 'Em Off")
FramePerSec = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
s_switchon = pygame.image.load("Switchy/switchon.png")
s_switchoff = pygame.image.load("Switchy/switchoff.png")
s_bulb = pygame.image.load("Switchy/bulb.png")
s_title = pygame.image.load('Switchy/title.png')
s_stopwatch = pygame.image.load("Switchy/stopwatch.png")
s_ice = pygame.image.load("Switchy/ice.png")
s_glasses = pygame.image.load("Switchy/glasses.png")
s_red = pygame.image.load('Switchy/switchred.png')
text = pygame.font.SysFont("calibri", 40)
text_score = pygame.font.SysFont('calibri', 64)
phrase = "But why don’t you just turn off your computer???"


class Switchy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(s_switchon, (50, 75))
        self.rect = self.image.get_rect(
            center=(random.randint(25, SCREEN_WIDTH - 50), random.randint(137, SCREEN_HEIGHT - 75)))
        self.clicked = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def switch(self):
        if not self.clicked:
            self.image = pygame.transform.scale(s_switchoff, (50, 75))
        else:
            self.image = pygame.transform.scale(s_switchon, (50, 75))


class Lights(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(s_bulb, (80, 80))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH - 50, 50))
        self.image.set_alpha(255)

    def draw(self, surface, percentage):
        alpha = percentage * 255
        self.image.set_alpha(alpha)
        surface.blit(self.image, self.rect)


class Button(pygame.sprite.Sprite):
    def __init__(self, img, height):
        super().__init__()
        self.clicked = False
        self.hasDrawn = False
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, height))
        self.hasImage = True

    def draw(self, surface):
        action = False
        surface.blit(self.image, self.rect)

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                mixer.music.load("Switchy/click.wav")
                mixer.music.play()
                self.clicked = True
                return True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        self.hasDrawn = True
        return action


class Powerup(pygame.sprite.Sprite):
    def __init__(self, img, x, y, cd):
        super().__init__()
        self.clicked = False
        self.hasDrawn = False
        self.image = img
        self.rect = self.image.get_rect(center=(x, y))
        self.hasImage = True
        self.maxTime = cd * FPS
        self.cooldown = 0
        self.x = x
        self.y = y

    def draw(self, surface):
        pygame.draw.rect(screen, WHITE, pygame.Rect(self.x - 60, 90, 15, - 80), 3, 5)
        pygame.draw.rect(screen, WHITE, pygame.Rect(self.x - 60, 90, 13, - (1 - self.cooldown / self.maxTime) * 80), 0,
                         5)
        alpha = (1 - self.cooldown / self.maxTime) * 255
        self.image.set_alpha(alpha)
        action = False
        surface.blit(self.image, self.rect)

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False and self.cooldown == 0:
                action = True
                mixer.music.load("Switchy/click.wav")
                mixer.music.play()
                self.clicked = True
                self.cooldown = self.maxTime
                return True

        if self.cooldown < 0:
            self.cooldown = 0
        else:
            self.cooldown -= 1

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        self.hasDrawn = True
        return action


class Player():
    def __init__(self):
        self.highscores = [0, 0, 0]


Light = Lights()
b_start = Button("Switchy/play.png", SCREEN_HEIGHT - 75)
b_stopwatch = Powerup(s_stopwatch, 280, 50, 10)
b_ice = Powerup(s_ice, 400, 50, 8)
b_glasses = Powerup(s_glasses, 520, 50, 12)
P1 = Player()


def play():
    score = 0
    percentage = 0.5
    timer_max = 1000
    switchy_max = 20
    switchy_list = list()
    SPAWN_TIMER = pygame.USEREVENT + 1
    SPEED_TIMER = pygame.USEREVENT + 2
    COUNT_TIMER = pygame.USEREVENT + 3
    pygame.time.set_timer(SPAWN_TIMER, timer_max)
    pygame.time.set_timer(SPEED_TIMER, 750)
    pygame.time.set_timer(COUNT_TIMER, 2000)
    switchy_list.append(Switchy())

    stopped = 0
    glasses_stop = 0
    while percentage < 0.8:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SPAWN_TIMER and stopped == 0:
                switchy_list.append(Switchy())
            if event.type == SPEED_TIMER:
                if timer_max > 100:
                    timer_max -= 50
                pygame.time.set_timer(SPAWN_TIMER, timer_max)
            if event.type == COUNT_TIMER:
                switchy_max += 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                for s in switchy_list:
                    if s.rect.collidepoint(pos):
                        s.kill()
                        s.switch()
                        if s.clicked:
                            s.clicked = False
                            score -= 10
                        else:
                            s.clicked = True
                            score += 10

        b_stopwatch.draw(screen)
        b_ice.draw(screen)
        b_glasses.draw(screen)

        if stopped < 0:
            stopped = 0
        else:
            stopped -= 1

        if b_stopwatch.clicked:
            stopped = 4 * FPS
            b_stopwatch.clicked = False

        if b_ice.clicked:
            timer_max += 100
            b_ice.clicked = False

        if glasses_stop < 0:
            glasses_stop = 0
            for s in switchy_list:
                if not s.clicked:
                    s.image = pygame.transform.scale(s_switchon, (50, 75))
        else:
            glasses_stop -= 1

        if b_glasses.clicked:
            glasses_stop = 1 * FPS
            b_glasses.clicked = False

        if glasses_stop > 0:
            for s in switchy_list:
                if not s.clicked:
                    s.image = pygame.transform.scale(s_red, (50, 75))

        turned_off = 0
        total = len(switchy_list)
        for s in switchy_list:
            if not s.clicked:
                turned_off += 1
        percentage = turned_off / (total + 1)
        Light.draw(screen, percentage)

        if total > switchy_max:
            switchy_list[0].kill()
            switchy_list.pop(0)

        for switchy in switchy_list:
            switchy.draw(screen)

        score_display = text.render(str(score) + " watts", True, WHITE, BLACK)
        screen.blit(score_display, (25, 25))

        # percentage_display = text.render(str(percentage), True, WHITE, BLACK)
        # screen.blit(percentage_display, (300, 25))

        pygame.draw.rect(screen, RED, pygame.Rect(SCREEN_WIDTH - 100, 90, 15, - 0.8 * 80), 3, 5)
        pygame.draw.rect(screen, WHITE, pygame.Rect(SCREEN_WIDTH - 100, 90, 15, - 80), 3, 5)
        pygame.draw.rect(screen, WHITE, pygame.Rect(SCREEN_WIDTH - 99, 90, 13, - percentage * 80), 0, 5)

        pygame.draw.rect(screen, WHITE, pygame.Rect(0, 0, SCREEN_WIDTH, 100), 5, 7)

        pygame.display.update()
        FramePerSec.tick(FPS)

    P1.highscores.append(score)
    P1.highscores.sort(reverse=True)
    P1.highscores = P1.highscores[:3]

    return score


def ending_screen(x):
    ENDING_TIMER = pygame.USEREVENT + 4
    pygame.time.set_timer(ENDING_TIMER, 100)
    quote = ""
    i = 0
    mixer.music.load("Switchy/typing.wav")
    mixer.music.play()
    while len(quote) < len(phrase):
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ENDING_TIMER:
                quote = phrase[:i]
                i += 1
        screen_score = text_score.render(f"You Saved {str(x)} Watts!", True, WHITE, BLACK)
        screen.blit(screen_score, (100, SCREEN_HEIGHT / 2 - 100))

        message = text.render(quote, True, WHITE, BLACK)
        screen.blit(message, (20, 400))

        pygame.display.update()
        FramePerSec.tick(FPS)


def main_menu():
    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        b_start.draw(screen)

        title = pygame.transform.scale(s_title, (SCREEN_WIDTH - 40, 100))
        title_rect = title.get_rect(center=(SCREEN_WIDTH / 2, 60))
        screen.blit(title, title_rect)

        highscore_display = text.render("HIGHSCORES", True, WHITE, BLACK)
        highscore_display_1 = text.render(f"{str(P1.highscores[0])}", True, WHITE, BLACK)
        highscore_display_2 = text.render(f"{str(P1.highscores[1])}", True, WHITE, BLACK)
        highscore_display_3 = text.render(f"{str(P1.highscores[2])}", True, WHITE, BLACK)
        highscore_display_rect = highscore_display.get_rect(center=(SCREEN_WIDTH / 2, 180))
        highscore_display_1_rect = highscore_display_1.get_rect(center=(SCREEN_WIDTH / 2, 250))
        highscore_display_2_rect = highscore_display_2.get_rect(center=(SCREEN_WIDTH / 2, 320))
        highscore_display_3_rect = highscore_display_3.get_rect(center=(SCREEN_WIDTH / 2, 390))
        screen.blit(highscore_display, highscore_display_rect)
        screen.blit(highscore_display_1, highscore_display_1_rect)
        screen.blit(highscore_display_2, highscore_display_2_rect)
        screen.blit(highscore_display_3, highscore_display_3_rect)

        pygame.draw.rect(screen, WHITE, pygame.Rect(250, 140, 300, 300), 5, 7)

        bulb_left = pygame.transform.scale(s_bulb, (300, 300))
        bulb_left_rect = bulb_left.get_rect(center=(100, 300))
        bulb_right = pygame.transform.scale(s_bulb, (300, 300))
        bulb_right_rect = bulb_right.get_rect(center=(SCREEN_WIDTH - 100, 300))
        screen.blit(bulb_left, bulb_left_rect)
        screen.blit(bulb_right, bulb_right_rect)

        if b_start.clicked:
            x = play()
            b_start.clicked = False
            ending_screen(x)

        pygame.display.update()
        FramePerSec.tick(FPS)


main_menu()
