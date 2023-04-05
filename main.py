import os  # importējam os moduli, kas palīdzēs strādāt ar failiem un direktorijām
import random  # importējam random moduli, lai izmantotu gadījuma skaitļus
import math  # importējam math moduli, lai izmantotu matemātiskas funkcijas
import pygame  # importējam pygame moduli, kas palīdzēs radīt spēles
from os import listdir  # no os importējam listdir funkciju, kas atgriež sarakstu ar failiem direktorijā
from os.path import isfile, join  # no os.path importējam isfile un join funkcijas

pygame.init()  # inicializē pygame moduli

pygame.display.set_caption("2D Platformer") # nosaka loga virsrakstu

BG_COLOR = (255, 255, 255) # nosaka fona krāsu
WIDTH, HEIGHT = 1000, 800 # nosaka ekrāna izmēru
FPS = 60 # nosaka bilžu attēlošanas ātrumu
PLAYER_VEL = 5 # nosaka spēlētāja ātrumu

window = pygame.display.set_mode((WIDTH, HEIGHT))  # izveido spēles logu ar definētu izmēru


def get_background(name):  # funkcija, lai iegūtu fona elementus un attēlu
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


def draw(window, background, bg_image, player, objects, offset_x):  # funkcija objektu zīmēšanai uz ekrāna
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)

    pygame.display.update()



def main(window):  #galvenais logs, atbild par spēlēs uzsākšanu (iestatījumi)
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

    pygame.quit()
    quit()

    if __name__ == "__main__":
        main(window)
