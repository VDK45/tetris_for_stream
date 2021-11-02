import pygame
import os
import sys
import webbrowser
from copy import deepcopy
from random import choice, randrange


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


FPS = 60
white = (255, 255, 255)
black = (0, 0, 0)
gray = (120, 120, 120)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
pygame.init()
pygame.font.init()
shrift = resource_path('font/comicsansms3.ttf')
my_font = pygame.font.Font(shrift, 30)
win = pygame.display.set_mode((750, 940))  # Размер окна
pygame.display.set_caption("Голосуем за")  # Название окна
pygame.font.init()
tf2build_font1 = resource_path('font/tf2build.ttf')
tf2secondary_font1 = resource_path('font/tf2secondary.ttf')
smallfon = pygame.font.Font(tf2build_font1, 18)
myfont = pygame.font.Font(tf2build_font1, 16)
font_menu = pygame.font.Font(tf2build_font1, 30)
font2 = pygame.font.Font(tf2build_font1, 50)
clock = pygame.time.Clock()


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def play():
    W, H = 10, 20
    TILE = 45
    GAME_RES = W * TILE, H * TILE
    RES = 750, 940
    sc = pygame.display.set_mode(RES)
    game_sc = pygame.Surface(GAME_RES)

    grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

    figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                   [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                   [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                   [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                   [(0, 0), (0, -1), (0, 1), (-1, -1)],
                   [(0, 0), (0, -1), (0, 1), (1, -1)],
                   [(0, 0), (0, -1), (0, 1), (-1, 0)]]

    figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
    figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
    field = [[0 for i in range(W)] for j in range(H)]
    anim_count, anim_speed, anim_limit = 0, 60, 2000
    bg = pygame.image.load('img/bg.jpg').convert()
    game_bg = pygame.image.load('img/bg2.jpg').convert()

    main_font = pygame.font.Font('font/font.ttf', 65)
    font = pygame.font.Font('font/font.ttf', 45)

    title_tetris = main_font.render('TETRIS', True, pygame.Color('darkorange'))
    title_score = font.render('score:', True, pygame.Color('green'))
    title_record = font.render('record:', True, pygame.Color('purple'))

    get_color = lambda: (randrange(30, 256), randrange(30, 256), randrange(30, 256))

    figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
    color, next_color = get_color(), get_color()

    score, lines = 0, 0
    scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

    def check_borders():
        if figure[i].x < 0 or figure[i].x > W - 1:
            return False
        elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
            return False
        return True

    def get_record():
        try:
            with open('record') as f:
                return f.readline()
        except FileNotFoundError:
            with open('record', 'w') as f:
                f.write('0')

    def set_record(record, score):
        rec = max(int(record), score)
        with open('record', 'w') as f:
            f.write(str(rec))

    while True:
        record = get_record()
        dx, rotate = 0, False
        sc.blit(bg, (0, 0))
        sc.blit(game_sc, (20, 20))
        game_sc.blit(game_bg, (0, 0))
        # delay for full lines
        for i in range(lines):
            pygame.time.wait(200)
        # control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_RIGHT:
                    dx = 1
                elif event.key == pygame.K_DOWN:
                    anim_limit = 100
                elif event.key == pygame.K_UP:
                    rotate = True
        # move x
        figure_old = deepcopy(figure)

        for i in range(4):

            figure[i].x += dx
            if not check_borders():
                figure = deepcopy(figure_old)
                break
        # move y
        anim_count += anim_speed
        if anim_count > anim_limit:
            anim_count = 0
            figure_old = deepcopy(figure)
            for i in range(4):
                figure[i].y += 1
                if not check_borders():
                    for i in range(4):
                        field[figure_old[i].y][figure_old[i].x] = color
                    figure, color = next_figure, next_color
                    next_figure, next_color = deepcopy(choice(figures)), get_color()
                    anim_limit = 2000
                    break
        # rotate
        center = figure[0]
        figure_old = deepcopy(figure)
        if rotate:
            for i in range(4):
                x = figure[i].y - center.y
                y = figure[i].x - center.x
                figure[i].x = center.x - x
                figure[i].y = center.y + y
                if not check_borders():
                    figure = deepcopy(figure_old)
                    break
        # check lines
        line, lines = H - 1, 0
        for row in range(H - 1, -1, -1):
            count = 0
            for i in range(W):
                if field[row][i]:
                    count += 1
                field[line][i] = field[row][i]
            if count < W:
                line -= 1
            else:
                anim_speed += 3
                lines += 1
        # compute score
        score += scores[lines]
        # draw grid
        [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]
        # draw figure
        for i in range(4):
            figure_rect.x = figure[i].x * TILE
            figure_rect.y = figure[i].y * TILE
            pygame.draw.rect(game_sc, color, figure_rect)
        # draw field
        for y, raw in enumerate(field):
            for x, col in enumerate(raw):
                if col:
                    figure_rect.x, figure_rect.y = x * TILE, y * TILE
                    pygame.draw.rect(game_sc, col, figure_rect)
        # draw next figure
        for i in range(4):
            figure_rect.x = next_figure[i].x * TILE + 380
            figure_rect.y = next_figure[i].y * TILE + 185
            pygame.draw.rect(sc, next_color, figure_rect)
        # draw titles
        sc.blit(title_tetris, (485, -10))
        sc.blit(title_score, (535, 780))
        sc.blit(font.render(str(score), True, pygame.Color('white')), (550, 840))
        sc.blit(title_record, (525, 650))
        sc.blit(font.render(record, True, pygame.Color('gold')), (550, 710))
        # game over
        for i in range(W):
            if field[0][i]:
                set_record(record, score)
                field = [[0 for i in range(W)] for i in range(H)]
                anim_count, anim_speed, anim_limit = 0, 60, 2000
                score = 0
                for i_rect in grid:
                    pygame.draw.rect(game_sc, get_color(), i_rect)
                    sc.blit(game_sc, (20, 20))
                    pygame.display.flip()
                    clock.tick(200)

        pygame.display.flip()
        clock.tick(FPS)


def ip():
    pass


def joystick():
    pass


def main_menu():
    global FPS
    click = False
    while True:

        win.fill(gray)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(50, 100, 220, 50)
        button_2 = pygame.Rect(50, 200, 250, 50)
        button_3 = pygame.Rect(50, 300, 300, 50)
        button_4 = pygame.Rect(50, 500, 350, 50)
        button_5 = pygame.Rect(50, 560, 240, 30)
        if button_1.collidepoint((mx, my)):
            if click:
                print('Play')
        if button_2.collidepoint((mx, my)):
            if click:
                print('Button_2')
        if button_3.collidepoint((mx, my)):
            if click:
                print('Button_3')
        if button_4.collidepoint((mx, my)):
            if click:
                print('Donation')
                webbrowser.open('https://www.donationalerts.com/r/vdk45')
        if button_5.collidepoint((mx, my)):
            if click:
                print('download')
                webbrowser.open('https://cloud.mail.ru/public/BHJJ/6djS1G3qZ')
        pygame.draw.rect(win, blue, button_1)
        pygame.draw.rect(win, (20, 120, 120), button_2)
        pygame.draw.rect(win, (20, 120, 120), button_3)
        pygame.draw.rect(win, (255, 120, 0), button_4)
        pygame.draw.rect(win, blue, button_5)
        click = False
        keys_pres = pygame.key.get_pressed()
        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if keys_pres[pygame.K_ESCAPE]:
                play()
            if even.type == pygame.MOUSEBUTTONDOWN:
                if button_1.collidepoint(even.pos):
                    print('ok')
                    if even.button == 1:
                        click = True
                        play()
                if button_2.collidepoint(even.pos):
                    print('ok')
                    if even.button == 1:
                        click = True
                        ip()
                if button_3.collidepoint(even.pos):
                    print('ok')
                    if even.button == 1:
                        click = True
                        joystick()
                if button_4.collidepoint(even.pos):
                    print('ok')
                    if even.button == 1:
                        click = True
                if button_5.collidepoint(even.pos):
                    print('ok')
                    if even.button == 1:
                        click = True

        draw_text('Начать', font_menu, (255, 255, 255), win, 80, 115)
        draw_text('ip стримера', font_menu, (255, 255, 255), win, 80, 215)
        draw_text('Джойстик', font_menu, (255, 255, 255), win, 80, 310)
        draw_text('Поддержать меня', font_menu, (255, 255, 255), win, 65, 515)
        draw_text('скачать приложение', smallfon, (255, 255, 255), win, 63, 569)
        pygame.display.update()
        clock.tick(FPS)


main_menu()
