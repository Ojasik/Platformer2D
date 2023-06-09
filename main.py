import os  # importējam os moduli, kas palīdzēs strādāt ar failiem un direktorijām
import random  # importējam random moduli, lai izmantotu gadījuma skaitļus
import math  # importējam math moduli, lai izmantotu matemātiskas funkcijas
import pygame  # importējam pygame moduli, kas palīdzēs radīt spēles
from os import listdir  # no os importējam listdir funkciju, kas atgriež sarakstu ar failiem direktorijā
from os.path import isfile, join  # no os.path importējam isfile un join funkcijas

pygame.init()  # inicializē pygame moduli

pygame.display.set_caption("2D Platformer") # nosaka loga virsrakstu

WIDTH, HEIGHT = 1000, 800 # nosaka ekrāna izmēru
FPS = 60 # nosaka bilžu attēlošanas ātrumu
PLAYER_VEL = 5 # nosaka spēlētāja ātrumu

window = pygame.display.set_mode((WIDTH, HEIGHT))  # izveido spēles logu ar definētu izmēru


def flip(sprites):  # šī funkcija atgriež sarakstu ar horizontāli apgrieztiem sprites.
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]  # atgriež sprites


def load_sprite_sheets(dir1, dir2, width, height, direction=False):  # definē funkciju, lai ielādētu sprite lapas
    path = join("assets", dir1, dir2)  # konstruē ceļu uz sprite lapu
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {} # uzskaita visus direktorijā esošos failus

    for image in images:  # loops caur visiem attēliem, kas atrasti direktorijā
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()  # ielādē attēlu kā sprite lapu

        sprites = []  # inicializē tukšu sarakstu, kurā tiek saglabāti visi sprites, kas iegūti no sprite lapas.
        for i in range(sprite_sheet.get_width() // width):  # Izraksta katru sprite no sprite lapas un pievieno to sprite sarakstam.
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        # ja virziena karodziņš ir iestatīts uz True, pievieno sprites vārdnīcai ar nosaukumu
        # "[sprite_name]_right" and "[sprite_name]_left"
        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:  # pretējā gadījumā pievieno sprites vārdnīcai ar nosaukumu "[sprite_name]".
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites  # Atgriež visu sprites vārdnīcu


def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")  # attēla faila ceļa noteikšana
    image = pygame.image.load(path).convert_alpha()  # ielāde attēlu un konverte to alfa formātā
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)  # izveido jaunu virsmu ar norādīto izmēru un alfa kanālu
    rect = pygame.Rect(96, 0, size, size)  # izveido taisnstūra objektu ar norādīto izmēru un pozīciju attēlā
    surface.blit(image, (0, 0), rect)  # attēla daļas, ko nosaka taisnstūra objekts, pārklāšana uz jaunās virsmas
    return pygame.transform.scale2x(surface)  # mēroga virsmas mērogošana ar koeficientu 2, izmantojot bilineāro interpolāciju


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


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)  # inicialize vecāku klasi Objekts ar pozīciju (x, y) un izmēriem (size, size)
        block = get_block(size)  # bloka attēla ielāde ar norādīto izmēru
        self.image.blit(block, (0, 0))  # attēla pārklāšana uz bloka objekta attēla
        self.mask = pygame.mask.from_surface(self.image)  # izveido sadursmes masku no attēla


class Fire(Object):
    ANIMATION_DELAY = 3  # iestata animācijas aizkavi sprite lapai

    def __init__(self, x, y, width, height):  # define Fire klases konstruktora metodi
        super().__init__(x, y, width, height, "fire")  # izsauca Object klases konstruktora metodi un nododiet Fire objekta īpašības
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)  # Fire sprite lapas ielāde no resursu mapes, izmantojot palīgfunkciju load_sprite_sheets
        self.image = self.fire["off"][0]  # Fire objekta sākotnējā attēla iestatīšana
        self.mask = pygame.mask.from_surface(self.image)  # izveido Fire objekta masku no attēla virsmas
        self.animation_count = 0  # iestaja animāciju skaitu uz 0
        self.animation_name = "off"  # sākotnējās animācijas nosaukuma iestatīšana uz "off"

    def on(self):  # define metodi, lai ieslēgtu Fire objektu
        self.animation_name = "on"  # iestaja animācijas nosaukumu "on"

    def off(self):  # define metodi Fire objekta izslēgšanai
        self.animation_name = "off"  # iestaja animācijas nosaukumu "off"

    def loop(self):  # define Fire objekta galvenās cikla metodi
        sprites = self.fire[self.animation_name]  # iegūsta pašreizējās animācijas sprites no Fire sprites lapas
        sprite_index = (self.animation_count //  # aprēķina pašreizējo sprīta indeksu, pamatojoties uz animāciju skaitu un animācijas aizkavi.
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]  # Fire objekta pašreizējā attēla iestatīšana uz pašreizējo sprite
        self.animation_count += 1  # palielina animāciju skaitu

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))  # atjaunina Fire objekta taisnstūra pozīciju uz pašreizējo pozīciju
        self.mask = pygame.mask.from_surface(self.image)  # atjaunina Fire objekta masku no jaunās attēla virsmas

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):  # atiestata animāciju skaitu, ja tas pārsniedz animācijā iekļauto sprites skaitu
            self.animation_count = 0


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


def handle_vertical_collision(player, objects, dy):
    collided_objects = []

    for obj in objects:  # iterēt cauri katram objektam objektu sarakstā
        if pygame.sprite.collide_mask(player, obj):  # pārbauda, vai spēlētājs saskaras ar objektu
            if dy > 0:  # pārbauda, vai spēlētājs pārvietojas uz leju
                player.rect.bottom = obj.rect.top  # iestaja spēlētāja apakšdaļu uz sadursmes objekta augšdaļu.
                player.landed()  # iestaja spēlētāja statusu landed
            elif dy < 0:  # pārbauda, vai spēlētājs pārvietojas uz augšu
                player.rect.top = obj.rect.bottom  # iestaja spēlētāja augšdaļu uz sadursmes objekta apakšdaļu
                player.hit_head()  # iestaja spēlētāja statusu uz hit head

            collided_objects.append(obj)  # pievieno objektu, ar kuru notikusi sadursme, sadurto objektu sarakstam

    return collided_objects  # atgrieza sadūrušos objektu sarakstu


def collide(player, objects, dx):
    player.move(dx, 0)  # pārvieto spēlētāju horizontāli par dx
    player.update()  # atjaunina spēlētāja rect un attēlu
    collided_object = None  # inicialize sadursmes objektu kā None
    for obj in objects:  # itere cauri katram objektam objektu sarakstā
        if pygame.sprite.collide_mask(player, obj):  # pārbauda, vai spēlētājs saskaras ar objektu
            collided_object = obj  # iestaja sadursmes objektu kā pašreizējo objektu
            break  # iziet no cikla

    player.move(-dx, 0)  # pārvieto spēlētāju atpakaļ par -dx
    player.update()  # atjaunina spēlētāja rect un attēlu
    return collided_object  # atgrieza sadursmes objektu


def handle_move(player, objects):
    keys = pygame.key.get_pressed()  # iegūt nospiestos taustiņus

    player.x_vel = 0  # spēlētāja sākotnējā ātruma iestatīšana uz nulli.
    collide_left = collide(player, objects, -PLAYER_VEL * 2)  # pārbauda vai spēlētājs saskaras ar objektu pa kreisi vai pa labi.
    collide_right = collide(player, objects, PLAYER_VEL * 2)  # pārbauda, vai spēlētājs saskaras ar objektu pa kreisi vai pa labi.

    if keys[pygame.K_LEFT] and not collide_left:  # ja spēlētājs nospiež kreisās bulttaustiņu taustiņu un nesaskaras ar objektu pa kreisi, pārvietojiet spēlētāju pa kreisi.
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:  # ja spēlētājs nospiež labās bulttaustiņu taustiņu un nesaskaras ar objektu labajā pusē, pārvietojiet spēlētāju pa labi.
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)  # pārbauda, vai spēlētājam nav vertikālu saskares ar objektiem.
    to_check = [collide_left, collide_right, *vertical_collide] # izveido objektu sarakstu, lai pārbaudītu saskares esamību

    for obj in to_check:  # pārbauda, vai kāds no to_check sarakstā esošajiem objektiem ir "fire" objekts, un, ja tas tā ir, tad spēlētājam tiek nodarīts kaitējums.
        if obj and obj.name == "fire":
            player.make_hit()


def main(window):  # galvenais logs, atbild par spēlēs uzsākšanu un ielādešanu (iestatījumi)
    clock = pygame.time.Clock()
    background, bg_image = get_background("Purple.png")  # ielāde fonu

    block_size = 96  # bloka izmers

    player = Player(100, 100, 50, 50)  # spēlētaja objekts
    fire = Fire(100, HEIGHT - block_size - 64, 16, 32)  # uguns objekts
    fire.on()
    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    objects = [*floor, Block(0, HEIGHT - block_size * 2, block_size),
               Block(block_size * 3, HEIGHT - block_size * 4, block_size), fire]

    offset_x = 0
    scroll_area_width = 200  # scroll platums

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        player.loop(FPS)  # atjauno spēlētāju
        fire.loop()  # atjauno uguni
        handle_move(player, objects)  # apstrāda spēlētāja kustību
        draw(window, background, bg_image, player, objects, offset_x)  # zīme spēles objektus

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()
    quit()


if __name__ == "__main__":  # Izsauca galveno funkciju, lai sāktu spēli
    main(window)
