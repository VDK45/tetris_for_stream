import pygame
import os
import sys
import webbrowser
from copy import deepcopy
from random import choice, randrange
import threading
import server
import socket
import pyperclip

thread1 = threading.Thread(target=server.run, args=())
thread1.start()
try:
    file = open('ip_server.txt', 'r')
    line = file.readline()
    file.close()
    ip = line
    print(f'Connecting to: {ip}')
except FileNotFoundError:
    ip = 'vdk45.ddns.net'


def client_send(mes):
    global ip
    mes = mes.encode('utf-8')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, 4545))
        sock.send(mes)  # send byte
    except (TimeoutError, OSError) as err:
        print("Не удалось установить соединение.")
        print("Проверьте IP адрес!")
        sock.close()
        ip_server()
    sock.close()


def test():
    print('Conecting to server')
    client_send('Test connect')
    print(f'Connected to ip {ip}')


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


icon_win = resource_path('img/icon.png')
pygame.display.set_icon(pygame.image.load(icon_win))

# game option
FPS = 15
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
pygame.display.set_caption("Tetris twitch play")  # Название окна
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
    global mess
    W, H = 10, 20
    TILE = 45
    GAME_RES = W * TILE, H * TILE
    RES = 750, 940
    sc = pygame.display.set_mode(RES)
    game_sc = pygame.Surface(GAME_RES)

    grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

    figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],  # Палка
                   [(0, -1), (-1, -1), (-1, 0), (0, 0)],  # Квадрат
                   [(-1, 0), (-1, 1), (0, 0), (0, -1)],  # Z
                   [(0, 0), (-1, 0), (0, 1), (-1, -1)],  # S
                   [(0, 0), (0, -1), (0, 1), (-1, -1)],  # 7
                   [(0, 0), (0, -1), (0, 1), (1, -1)],  # Г
                   [(0, 0), (0, -1), (0, 1), (-1, 0)]]  # т

    figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
    figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
    field = [[0 for i in range(W)] for j in range(H)]
    anim_count, anim_speed, anim_limit = 0, 60, 2000
    bg = resource_path('img/bg2_green.jpg')
    game_bg = pygame.image.load(bg).convert()

    font_ttf = resource_path('font/font.ttf')
    main_font = pygame.font.Font(font_ttf, 65)

    font = pygame.font.Font(font_ttf, 45)

    title_tetris = main_font.render('TETRIS', True, pygame.Color('darkorange'))
    title_score = font.render('score:', True, pygame.Color('green'))
    title_record = font.render('record:', True, pygame.Color('purple'))

    get_color = lambda: (randrange(30, 256), randrange(0, 10), randrange(30, 256))

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
        # sc.blit(bg, (0, 0))
        sc.fill((0, 255, 0))
        sc.blit(game_sc, (20, 20))
        game_sc.blit(game_bg, (0, 0))
        # delay for full lines
        for i in range(lines):
            pygame.time.wait(200)
        # control
        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                server.status = False
                server.stop()
                pygame.quit()
                sys.exit()

            if even.type == pygame.KEYDOWN:
                if even.key == pygame.K_LEFT:
                    dx = -1
                elif even.key == pygame.K_RIGHT:
                    dx = 1
                elif even.key == pygame.K_DOWN:
                    anim_limit = 100
                elif even.key == pygame.K_UP:
                    rotate = True
                if even.key == pygame.K_a:
                    dx = -1
                elif even.key == pygame.K_d:
                    dx = 1
                elif even.key == pygame.K_s:
                    anim_limit = 100
                elif even.key == pygame.K_w:
                    rotate = True
                elif even.key == pygame.K_SPACE:
                    rotate = True

            if even.type == pygame.KEYUP:
                if even.key == pygame.K_ESCAPE:
                    main_menu()
        # socket control
        if server.message == b'!down':
            anim_limit = 100
            server.message = b''
        if server.message == b'!left':
            dx = -1
            server.message = b''
        if server.message == b'!right':
            dx = 1
            server.message = b''
        if server.message == b'!up':
            rotate = True
            server.message = b''
        if server.message == b'!jump':
            print(type(server.message))
            rotate = True
            server.message = b''
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
        [pygame.draw.rect(game_sc, (0, 0, 0), i_rect, 1) for i_rect in grid]
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


def ip_server():
    global FPS
    global ip
    click = False
    win = pygame.display.set_mode((750, 940))
    font = pygame.font.Font(tf2build_font1, 30)
    # clock = pygame.time.Clock()
    input_box = pygame.Rect(100, 150, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    ok_text = ''

    while True:
        win.fill(gray)

        # button_my_ip
        mx, my = pygame.mouse.get_pos()
        button_my_ip = pygame.Rect(50, 500, 350, 50)
        if button_my_ip.collidepoint((mx, my)):
            if click:
                print(' VDK45 IP')
                ip = 'vdk45.ddns.net'
                f = open('ip_server.txt', 'w+')
                f.write(f'{ip}')
                f.close()
        pygame.draw.rect(win, blue, button_my_ip)
        click = False

        keys_pres = pygame.key.get_pressed()
        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                pygame.quit()
                server.status = False
                server.stop()
                sys.exit()
            if keys_pres[pygame.K_ESCAPE]:
                server.stop()
                main_menu()

            if even.type == pygame.MOUSEBUTTONDOWN:
                if button_my_ip.collidepoint(even.pos):
                    if even.button == 1:
                        click = True
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(even.pos):
                    ip = pyperclip.paste()  # Paste copy
                    text_hind = ''
                    f = open('ip_server.txt', 'w+')
                    f.write(f'{ip}')
                    f.close()
                    # Toggle the active variable.
                    active = not active
                    ok_text = 'ESC Для выхода'
                else:
                    active = False
                    ok_text = 'ESC Для выхода'
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if even.type == pygame.KEYDOWN:
                if even.key == pygame.K_RETURN:
                    f = open('ip_server.txt', 'w+')
                    f.write(f'{ip}')
                    f.close()
                    print(ip)
                    ip = ''
                    ok_text = 'ESC Для выхода'
                elif even.key == pygame.K_BACKSPACE:
                    ip = ip[:-1]
                else:
                    ip += even.unicode
                    ok_text = 'ESC Для выхода'

        # Render the current text.
        txt_surface = font.render(ip, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        # Blit the text.
        win.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Blit the input_box rect.
        pygame.draw.rect(win, color, input_box, 2)
        draw_text('Enter ip stream and restart app!', font, (0, 0, 0), win, 50, 50)
        draw_text('Введите ip стримера', font, (0, 0, 0), win, 50, 90)
        draw_text('И перезагрузить программу!', font, (0, 0, 0), win, 50, 250)
        draw_text(ok_text, font, red, win, 50, 300)
        draw_text('Мой IP', font, white, win, 150, 510)
        draw_text('IP:', font, (0, 0, 0), win, 50, 155)

        pygame.display.update()
        clock.tick(FPS)


def joystick():
    win = pygame.display.set_mode((750, 400))
    global FPS
    click = False
    while True:
        win.fill(gray)
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(150, 50, 100, 100)
        button_2 = pygame.Rect(150, 250, 100, 100)
        button_3 = pygame.Rect(50, 150, 100, 100)
        button_4 = pygame.Rect(250, 150, 100, 100)
        button_5 = pygame.Rect(450, 250, 200, 100)

        if button_1.collidepoint((mx, my)):
            if click:
                print('w')
        if button_2.collidepoint((mx, my)):
            if click:
                print('s')
        if button_3.collidepoint((mx, my)):
            if click:
                print('a')
        if button_4.collidepoint((mx, my)):
            if click:
                print('d')
        if button_5.collidepoint((mx, my)):
            if click:
                print('Space')
        pygame.draw.rect(win, blue, button_1)
        pygame.draw.rect(win, blue, button_2)
        pygame.draw.rect(win, blue, button_3)
        pygame.draw.rect(win, blue, button_4)
        pygame.draw.rect(win, blue, button_5)
        click = False
        keys_pres = pygame.key.get_pressed()
        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                pygame.quit()
                server.status = False
                server.stop()
                sys.exit()
            if even.type == pygame.KEYDOWN:
                if even.key == pygame.K_a:
                    client_send('!left')
                    print('a')
                elif even.key == pygame.K_d:
                    client_send('!right')
                    print('d')
                elif even.key == pygame.K_s:
                    client_send('!down')
                    print('s')
                elif even.key == pygame.K_w:
                    client_send('!up')
                    print('w')
                elif even.key == pygame.K_SPACE:
                    client_send('!jump')
                    print('space')
            if keys_pres[pygame.K_ESCAPE]:
                main_menu()
            if even.type == pygame.MOUSEBUTTONDOWN:
                if button_1.collidepoint(even.pos):
                    if even.button == 1:
                        click = True
                        client_send('!up')
                if button_2.collidepoint(even.pos):
                    if even.button == 1:
                        click = True
                        client_send('!down')
                if button_3.collidepoint(even.pos):
                    if even.button == 1:
                        click = True
                        client_send('!left')
                if button_4.collidepoint(even.pos):
                    if even.button == 1:
                        click = True
                        client_send('!right')
                if button_5.collidepoint(even.pos):
                    if even.button == 1:
                        click = True
                        client_send('!jump')

        draw_text('w', font_menu, (255, 255, 255), win, 185, 85)
        draw_text('s', font_menu, (255, 255, 255), win, 185, 285)
        draw_text('a', font_menu, (255, 255, 255), win, 85, 185)
        draw_text('d', font_menu, (255, 255, 255), win, 285, 185)
        draw_text('Space', font_menu, (255, 255, 255), win, 500, 285)
        pygame.display.update()
        clock.tick(FPS)


def main_menu():
    global FPS
    click = False
    win = pygame.display.set_mode((750, 940))
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
                webbrowser.open('https://cloud.mail.ru/public/tLP4/AqunGUtGG')
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
                server.status = False
                server.stop()
                sys.exit()
            if keys_pres[pygame.K_ESCAPE]:
                play()
            if even.type == pygame.MOUSEBUTTONDOWN:
                if button_1.collidepoint(even.pos):
                    if even.button == 1:
                        click = True
                        play()
                if button_2.collidepoint(even.pos):
                    if even.button == 1:
                        click = True
                        ip_server()
                if button_3.collidepoint(even.pos):
                    if even.button == 1:
                        click = True
                        joystick()
                if button_4.collidepoint(even.pos):
                    if even.button == 1:
                        click = True
                if button_5.collidepoint(even.pos):
                    if even.button == 1:
                        click = True

        draw_text('Начать', font_menu, (255, 255, 255), win, 80, 115)
        draw_text('ip стримера', font_menu, (255, 255, 255), win, 80, 215)
        draw_text('Джойстик', font_menu, (255, 255, 255), win, 80, 310)
        draw_text('Поддержать меня', font_menu, (255, 255, 255), win, 65, 515)
        draw_text('скачать приложение', smallfon, (255, 255, 255), win, 63, 569)
        pygame.display.update()
        clock.tick(FPS)


test()
main_menu()
