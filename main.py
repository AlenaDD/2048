# Функция для красиваго отображения массива
# При выполнении функции печати ставим * чтобы убрать лишние скобки и знаки
#  Импортируем все что есть в модуле logics
import pygame
import sys
from logics import *
from database import get_best, cur, insert_result
import json
import os

GAMERS_DB = get_best()
if GAMERS_DB:
    best_score = GAMERS_DB[0][1]
else:
    best_score = 0


def draw_top_gamers():
    font_top = pygame.font.SysFont('Times New Roman', 25)
    font_gamers = pygame.font.SysFont('Times New Roman', 16)
    text_head = font_top.render('Best tries:', True, COLOR_TEXT)
    screen.blit(text_head, (300, 5))
    for index, gamer in enumerate(GAMERS_DB):
        name, score = gamer
        s = f"{index + 1}. {name} - {score}"
        text_gamer = font_gamers.render(s, True, COLOR_TEXT)
        screen.blit(text_gamer, (300, 35 + 25 * index))
        print(index, name, score)


def draw_interface(score, delta=0):
    pygame.draw.rect(screen, WHITE, TITLE_REC)
    font = pygame.font.SysFont('comicsansms', 70)
    font_score = pygame.font.SysFont('Times New Roman', 48)
    font_delta = pygame.font.SysFont('Times New Roman', 32)
    text_score = font_score.render("Score: ", True, COLOR_TEXT)
    text_score_value = font_score.render(f"{score}", True, COLOR_TEXT)
    screen.blit(text_score, (20, 25))
    screen.blit(text_score_value, (175, 25))
    if delta > 0:
        text_delta = font_delta.render(f"+{delta}", True, COLOR_TEXT)
        screen.blit(text_delta, (170, 65))
    pretty_print(mas)
    draw_top_gamers()
    for row in range(BLOCK):
        for column in range(BLOCK):
            value = mas[row][column]
            text = font.render(f'{value}', True, BLACK)
            w = column * SIZE_BLOCK + (column + 1) * MARGIN
            h = row * SIZE_BLOCK + (row + 1) * MARGIN + SIZE_BLOCK
            pygame.draw.rect(screen, COLORS[value], (w, h, SIZE_BLOCK, SIZE_BLOCK))
            if value != 0:
                font_w, font_h = text.get_size()
                text_x = w + (SIZE_BLOCK - font_w) / 2
                text_y = h + (SIZE_BLOCK - font_h) / 2
                screen.blit(text, (text_x, text_y))


# Положить в массив два значения

COLOR_TEXT = (255, 127, 0)
COLORS = {
    0: (130, 130, 130),
    2: (255, 255, 255),
    4: (255, 255, 128),
    8: (255, 255, 0),
    16: (255, 235, 255),
    32: (255, 232, 128),
    64: (255, 232, 0),
    128: (255, 105, 200),
    256: (255, 50, 255),
    512: (240, 255, 40),
    1024: (0, 250, 0),
    2048: (200, 130, 20),
    4096: (1, 255, 5)

}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (130, 130, 130)
BLOCK = 4
SIZE_BLOCK = 110
MARGIN = 10
WIDTH = BLOCK * SIZE_BLOCK + (BLOCK + 1) * MARGIN
HEIGHT = WIDTH + 110
TITLE_REC = pygame.Rect(0, 0, WIDTH, 110)


def init_const():
    global score, mas
    mas = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    empty = get_empty_list(mas)
    random.shuffle(empty)
    random_num1 = empty.pop()
    random_num2 = empty.pop()
    x1, y1 = get_index_from_number(random_num1)
    mas = insert_2_or_4(mas, x1, y1)
    x2, y2 = get_index_from_number(random_num2)
    mas = insert_2_or_4(mas, x2, y2)
    score = 0


mas = None
Score = None
USERNAME = None
path = os.getcwd()
if 'data.txt' in os.listdir():
    with open('data.txt') as file:
        data = json.load(file)
        mas = data['mas']
        Score = data['score']
        USERNAME = data['user']
    full_path = os.path.join(path, 'data.txt')
    os.remove(full_path)
else:
    init_const()

print(get_empty_list(mas))
pretty_print(mas)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")


def draw_intro():
    img2048 = pygame.image.load('2048.jpg')
    font = pygame.font.SysFont('comicsansms', 50)
    text_welcome = font.render("Welcome!", True, WHITE)
    name = 'Введите имя'
    is_find_name = False
    while not is_find_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    if name == 'Введите имя':
                        name = event.unicode
                    else:
                        name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(name) > 2:
                        global USERNAME
                        USERNAME = name
                        is_find_name = True
                        break

        screen.fill(BLACK)
        text_name = font.render(name, True, WHITE)
        rect_name = text_name.get_rect()
        rect_name.center = screen.get_rect().center
        screen.blit(pygame.transform.scale(img2048, [200, 200]), [10, 10])
        screen.blit(text_welcome, (230, 90))
        screen.blit(text_name, rect_name)
        pygame.display.update()
    screen.fill(BLACK)


def draw_game_over():
    global USERNAME, mas, GAMERS_DB
    img2048 = pygame.image.load('2048.jpg')
    font = pygame.font.SysFont('comicsansms', 50)
    text_game_over = font.render("Game over!", True, WHITE)
    text_score = font.render(f"Вы набрали {score}", True, WHITE)
    best_score = GAMERS_DB[0][1]
    if score > best_score:
        text = "Рекорд побит!"
    else:
        text = f"Рекорд  {best_score}"
    text_record = font.render(text, True, WHITE)
    insert_result(USERNAME, score)
    GAMERS_DB = get_best()
    make_decision = False
    while not make_decision:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # restart game with name
                    make_decision = True
                    init_const()
                elif event.key == pygame.K_RETURN:
                    # restart game without name
                    USERNAME = None
                    make_decision = True
                    init_const()
        screen.fill(BLACK)
        screen.blit(text_game_over, (220, 90))
        screen.blit(text_score, (30, 250))
        screen.blit(text_record, (30, 300))
        # уменьшает размер картинки и размещает ее в левом верхнем углу
        screen.blit(pygame.transform.scale(img2048, [200, 200]), [10, 10])
        pygame.display.update()

    screen.fill(BLACK)


def save_game():
    data = {
        'user': USERNAME,
        'score': score,
        'mas': mas
    }
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)


def game_loop():
    # начинаем цикл игры
    # ждем от пользователя команды
    global score, mas
    draw_interface(score)
    pygame.display.update()
    is_mas_move = False
    while is_zero_in_mas(mas) or can_move(mas):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game()
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                delta = 0
                if event.key == pygame.K_LEFT:
                    mas, delta, is_mas_move = move_left(mas)
                elif event.key == pygame.K_RIGHT:
                    mas, delta, is_mas_move = move_right(mas)
                elif event.key == pygame.K_UP:
                    mas, delta, is_mas_move = move_up(mas)
                elif event.key == pygame.K_DOWN:
                    mas, delta, is_mas_move = move_down(mas)
                score += delta

                if is_zero_in_mas(mas) and is_mas_move:
                    # input()
                    # ищем пустые клетки
                    empty = get_empty_list(mas)
                    random.shuffle(empty)
                    random_num = empty.pop()
                    x, y = get_index_from_number(random_num)
                    mas = insert_2_or_4(mas, x, y)
                    print(f'Мы заполнили элемент под номером {random_num}')
                    is_mas_move = False

                draw_interface(score, delta)
                pygame.display.update()

    print(USERNAME)


while True:
    if USERNAME is None:
        draw_intro()
    game_loop()
    draw_game_over()
