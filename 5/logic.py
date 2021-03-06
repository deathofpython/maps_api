import sys
import pygame
import requests
from threading import Thread
from interface import MyWidget
from params import get_map_params
from PyQt5.QtWidgets import QApplication

q = 0

coords = [10.0, 10.0]
spn = 10
value = 5

dx = 10
dy = 10

map_api_server = "http://static-maps.yandex.ru/1.x/"

pygame.init()
screen = pygame.display.set_mode((600, 450))


def check_key_event():
    global spn, value, dx, dy, q
    if pygame.key.get_pressed()[pygame.K_PAGEUP]:
        if spn < 90:
            spn += value
    if pygame.key.get_pressed()[pygame.K_PAGEDOWN]:
        if spn > 0:
            spn -= value

    if pygame.key.get_pressed()[pygame.K_UP]:
        if coords[1] != 80:
            coords[1] += dy
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        if coords[1] != -80:
            coords[1] -= dy
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        if coords[0] != 170:
            coords[0] += dx
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        if coords[0] != -180:
            coords[0] -= dx
    if pygame.key.get_pressed()[pygame.K_q]:
        q += 1


def show_picture():
    response = requests.get(map_api_server, params=get_map_params(','.join([str(coords[0]), str(coords[1])]), str(spn) + ',' + str(spn), q))
    file = open('file.png', 'wb')
    file.write(response.content)
    screen.blit(pygame.image.load('file.png'), (0, 0))


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()


def main():
    global coords
    while pygame.event.wait().type != pygame.QUIT:
        if ex.answer:
            try:
                coords[0] = float(ex.answer[:ex.answer.index(',')])
                coords[1] = float(ex.answer[ex.answer.index(',') + 1:])
                ex.answer = ''
            except ValueError:
                print('wrong coords')
        check_key_event()
        try:
            show_picture()
        except:
            print('wrong coords')
        pygame.display.update()


Thread(target=main()).start()
sys.exit(app.exec())
