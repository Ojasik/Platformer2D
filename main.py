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
