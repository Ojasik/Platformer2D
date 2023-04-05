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


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1  # piespiež spēlētāju uz leju
    SPRITES = load_sprite_sheets("MainCharacters", "MaskDude", 32, 32, True)  # spēlētāja izskata attēli
    ANIMATION_DELAY = 3 # kad daudzums sasniedz noteiktu vērtību, animācija tiks atjaunināta

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)  # spēlētāja kaste
        self.x_vel = 0  # spēlētāja x virziena ātrums
        self.y_vel = 0  # spēlētāja y virziena ātrums
        self.mask = None  # spēlētāja kastes maska
        self.direction = "left"  # spēlētāja virziena vērtība
        self.animation_count = 0  # kāds skaitlis tiek pievienots katrai animācijai
        self.fall_count = 0  # spēlētāja kritiena skaitītājs
        self.jump_count = 0  # spēlētāja lēciena skaitītājs
        self.hit = False  # vai spēlētājs ir ietriecies objektā
        self.hit_count = 0  # laiks, kurā spēlētājs ir ietriecies objektā

    def jump(self):
        self.y_vel = -self.GRAVITY * 8  # spēlētāja lēkšana
        self.animation_count = 0
        self.jump_count += 1  # spēlētāja lēciena skaitītāja palielināšana
        if self.jump_count == 1:
            self.fall_count = 0  # ja spēlētājs ir sācis lēkt, tad iestatām kritiena skaitītāju uz nulli

    def move(self, dx, dy):
        self.rect.x += dx  # spēlētāja x virziena pārvietošana
        self.rect.y += dy  # spēlētāja y virziena pārvietošana

    def make_hit(self):
        self.hit = True  # spēlētājs ir saskāries ar objektu

    def move_left(self, vel):
        self.x_vel = -vel  # spēlētāja kustība pa kreisi
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0  # mainot spēlētāja virzienu, animācija tiek atjaunināta

    def move_right(self, vel):
        self.x_vel = vel  # spēlētāja kustība pa labi
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0  # mainot spēlētāja virzienu, animācija tiek atjaunināta

    def loop(self, fps):  # metode, kas atkārto spēli ar noteiktu kadru skaitu sekundē (fps).
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):  # metode, kas norāda, ka spēlētājs ir nolaidies uz zemes.
        self.fall_count = 0
        self.y_vel = 0  # spēlētajs neparvietojas pa y asi
        self.jump_count = 0  # lecieni beidzas

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):  # metode, kas atjauno spēlētāja animāciju.
        sprite_sheet = "idle"  # izmantots default modelis
        if self.hit:  # ja spēlētajs ir traumēts
            sprite_sheet = "hit"  # mainās modelis
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"  # ja spēlētajs palecas 1 reizi, tad mainas modelis
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"  # ja spēlētajs palecas 2 reizes, tad mainas modelis
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"  # ja spēlētajs krit, tad mainas modelis
        elif self.x_vel != 0:
            sprite_sheet = "run"  # ja spēlētajs skrien, tad mainas modelis

        sprite_sheet_name = sprite_sheet + "_" + self.direction  # ši daļa izvelas sprites
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):  # metode, kas zīmē sprite spēles ekrānā noteiktā pozīcijā.
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))


class Object(pygame.sprite.Sprite):  # izveido spēles objektu (konstruktors).
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):  # izmanto Pygame funkciju "blit", lai uzzīmētu objekta attēlu logā pašreizējā pozīcijā, kas tiek aprēķināta kā starpība starp objekta x koordinātu un offset_x vērtību.
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


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
