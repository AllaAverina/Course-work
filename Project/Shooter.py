import pygame
import random
import sys
from os import path

width = 1200
height = 900
FPS = 26


class Player(pygame.sprite.Sprite):
    # направление выстрелов
    direction_x = 0
    direction_y = 1

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.current_time = 0
        self.animation_time = 1.2
        self.last_update = pygame.time.get_ticks()
        self.image = player_walk_top[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)
        self.speed_x = 0
        self.speed_y = 0
        self.lives = 3
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        # управление персонажем и анимация его передвижений
        self.speed_x = 0
        self.speed_y = 0

        pressed = pygame.mouse.get_pressed(3)
        if pressed[0]:
            self.shoot()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.shoot()

        if keys[pygame.K_a] and keys[pygame.K_w]:
            self.speed_x = -4
            self.speed_y = -4
            self.current_time += 0.3
            if self.current_time >= self.animation_time:
                self.current_time = 0
                self.index += 1
                if self.index > len(player_walk_top_left) - 1:
                    self.index = 0
                self.image = player_walk_top_left[self.index]
            self.direction_x = -1
            self.direction_y = -1
        elif keys[pygame.K_d] and keys[pygame.K_w]:
            self.speed_x = 4
            self.speed_y = -4
            self.current_time += 0.3
            if self.current_time >= self.animation_time:
                self.current_time = 0
                self.index += 1
                if self.index > len(player_walk_top_right) - 1:
                    self.index = 0
                self.image = player_walk_top_right[self.index]
            self.direction_x = 1
            self.direction_y = -1
        elif keys[pygame.K_a] and keys[pygame.K_s]:
            self.speed_x = -4
            self.speed_y = 4
            self.current_time += 0.3
            if self.current_time >= self.animation_time:
                self.current_time = 0
                self.index += 1
                if self.index > len(player_walk_bottom_left) - 1:
                    self.index = 0
                self.image = player_walk_bottom_left[self.index]
            self.direction_x = -1
            self.direction_y = 1
        elif keys[pygame.K_d] and keys[pygame.K_s]:
            self.speed_x = 5
            self.speed_y = 4
            self.current_time += 0.3
            if self.current_time >= self.animation_time:
                self.current_time = 0
                self.index += 1
                if self.index > len(player_walk_bottom_right) - 1:
                    self.index = 0
                self.image = player_walk_bottom_right[self.index]
            self.direction_x = 1
            self.direction_y = 1
        elif keys[pygame.K_a]:
            self.speed_x = -4
            self.current_time += 0.3
            if self.current_time >= self.animation_time:
                self.current_time = 0
                self.index += 1
                if self.index > len(player_walk_left) - 1:
                    self.index = 0
                self.image = player_walk_left[self.index]
            self.direction_y = 0
            self.direction_x = -1
        elif keys[pygame.K_d]:
            self.speed_x = 5
            self.current_time += 0.3
            if self.current_time >= self.animation_time:
                self.current_time = 0
                self.index += 1
                if self.index > len(player_walk_right) - 1:
                    self.index = 0
                self.image = player_walk_right[self.index]
            self.direction_y = 0
            self.direction_x = 1
        elif keys[pygame.K_w]:
            self.speed_y = -5
            self.current_time += 0.3
            if self.current_time >= self.animation_time:
                self.current_time = 0
                self.index += 1
                if self.index > len(player_walk_bottom) - 1:
                    self.index = 0
                self.image = player_walk_bottom[self.index]
            self.direction_x = 0
            self.direction_y = -1
        elif keys[pygame.K_s]:
            self.speed_y = 5
            self.current_time += 0.3
            if self.current_time >= self.animation_time:
                self.current_time = 0
                self.index += 1
                if self.index > len(player_walk_top) - 1:
                    self.index = 0
                self.image = player_walk_top[self.index]
            self.direction_x = 0
            self.direction_y = 1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # ограничение передвижения персонажа
        if self.rect.right > 1100:
            self.rect.right = 1100
        if self.rect.left < 100:
            self.rect.left = 100
        if self.rect.bottom > 800:
            self.rect.bottom = 800
        if self.rect.top < 100:
            self.rect.top = 100

    # функция выстрела

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction_x, self.direction_y)
            all_sprites.add(bullet)
            bullets.add(bullet)
            random.choice(shoot_sounds).play()


class EnemiesTop(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = en_t_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(200, 1000)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(4, 7)

    def update(self):
        self.rect.y += self.speed_y
        # после выхода за границы, враг не удаляется, а переносится на противоположную сторону
        if self.rect.top > height + 10:
            self.rect.x = random.randrange(200, 1000)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(4, 7)


class EnemiesRight(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = en_r_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(-100, -40)
        self.rect.y = random.randrange(200, 700)
        self.speed_x = random.randrange(4, 7)

    def update(self):
        self.rect.x += self.speed_x
        # после выхода за границы, враг не удаляется, а переносится на противоположную сторону
        if self.rect.right > width + 20:
            self.rect.x = random.randrange(-100, -40)
            self.rect.y = random.randrange(200, 700)
            self.speed_x = random.randrange(4, 7)


class EnemiesBottom(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = en_b_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(200, 1000)
        self.rect.y = random.randrange(1000, 1040)
        self.speed_y = random.randrange(4, 7)

    def update(self):
        self.rect.y -= self.speed_y
        # после выхода за границы, враг не удаляется, а переносится на противоположную сторону
        if self.rect.top < -50:
            self.rect.x = random.randrange(200, 1000)
            self.rect.y = random.randrange(1000, 1040)
            self.speed_y = random.randrange(4, 7)


class EnemiesLeft(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = en_l_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(1240, 1300)
        self.rect.y = random.randrange(200, 700)
        self.speed_x = random.randrange(4, 7)

    def update(self):
        self.rect.x -= self.speed_x
        # после выхода за границы, враг не удаляется, а переносится на противоположную сторону
        if self.rect.left < -50:
            self.rect.x = random.randrange(1240, 1300)
            self.rect.y = random.randrange(200, 700)
            self.speed_x = random.randrange(4, 7)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.speed_x = 15 * dx
        self.speed_y = 15 * dy

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # удаление энергоразряда после вылета за границы
        if self.rect.bottom < 0 or self.rect.top > height or self.rect.right > width or self.rect.left < 0:
            self.kill()


class Heart(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = heart_img
        self.rect = self.image.get_rect()
        self.spawn_points = [[random.randrange(200, 1000), -40],
                             [-40, random.randrange(200, 700)],
                             [random.randrange(200, 1000), 940],
                             [1240, random.randrange(200, 700)]]
        self.points = random.randrange(0, 4)
        self.rect.x = self.spawn_points[self.points][0]
        self.rect.y = self.spawn_points[self.points][1]
        if self.points == 0:
            self.speed_x = 0
            self.speed_y = 5
        elif self.points == 1:
            self.speed_x = 5
            self.speed_y = 0
        elif self.points == 2:
            self.speed_x = 0
            self.speed_y = -5
        else:
            self.speed_x = -5
            self.speed_y = 0

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # удаление сердечка после вылета за границы
        if self.rect.bottom < -70 or self.rect.top > 970 or self.rect.right > 1270 or self.rect.left < -70:
            self.kill()


# главное меню
def main_menu():
    pygame.mouse.set_visible(True)
    screen.blit(menu_img, menu_rect)
    draw_text(screen, 'ИГРАТЬ', 50, width / 2, 600)
    draw_text(screen, 'ВЫХОД', 50, width / 2, 700)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        screen.blit(menu_img, menu_rect)
        mp = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.KEYUP:
                waiting = False
            if e.type == pygame.MOUSEMOTION:
                if width / 2 - 100 < mp[0] < width / 2 + 100 and 580 < mp[1] < 660:
                    draw_text(screen, 'ИГРАТЬ', 56, width / 2, 600, (255, 255, 0))
                else:
                    draw_text(screen, 'ИГРАТЬ', 50, width / 2, 600)
                if width / 2 - 100 < mp[0] < width / 2 + 100 and 680 < mp[1] < 760:
                    draw_text(screen, 'ВЫХОД', 56, width / 2, 700, (255, 255, 0))
                else:
                    draw_text(screen, 'ВЫХОД', 50, width / 2, 700)
                pygame.display.flip()
            if e.type == pygame.MOUSEBUTTONUP and width / 2 - 100 < mp[0] < width / 2 + 100 and 580 < mp[1] < 660:
                if e.button == 1:
                    waiting = False
            if e.type == pygame.MOUSEBUTTONUP and width / 2 - 100 < mp[0] < width / 2 + 100 and 680 < mp[1] < 760:
                if e.button == 1:
                    sys.exit()


# проигрыш
def over():
    record = int(get_record())
    if score > record:
        draw_text(screen, 'Новый рекорд!', 44, width / 2, 200, (255, 0, 0))
        set_record(score)
    pygame.mouse.set_visible(True)
    screen.fill((0, 0, 0))
    draw_text(screen, 'ВЫ ПРОИГРАЛИ', 100, width / 2, 100)
    draw_text(screen, 'Счёт: ' + str(score), 60, width / 2, 300)
    draw_text(screen, 'Рекорд: ' + str(record), 60, width / 2, 400)
    draw_text(screen, 'ИГРАТЬ ЗАНОВО', 50, width / 2, 600)
    draw_text(screen, 'ГЛАВНОЕ МЕНЮ', 50, width / 2, 700)
    pygame.display.flip()
    game_over_sound.play()
    waiting = True
    while waiting:
        clock.tick(FPS)
        screen.fill((0, 0, 0))
        draw_text(screen, 'ВЫ ПРОИГРАЛИ', 100, width / 2, 100)
        if score > record:
            draw_text(screen, 'Новый рекорд!', 44, width / 2, 200, (255, 0, 0))
        draw_text(screen, 'Счёт: ' + str(score), 60, width / 2, 300)
        draw_text(screen, 'Рекорд: ' + str(record), 60, width / 2, 400)
        mp = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.MOUSEMOTION:
                if width / 2 - 180 < mp[0] < width / 2 + 180 and 580 < mp[1] < 660:
                    draw_text(screen, 'ИГРАТЬ ЗАНОВО', 56, width / 2, 600, (255, 255, 0))
                else:
                    draw_text(screen, 'ИГРАТЬ ЗАНОВО', 50, width / 2, 600)
                if width / 2 - 180 < mp[0] < width / 2 + 180 and 680 < mp[1] < 760:
                    draw_text(screen, 'ГЛАВНОЕ МЕНЮ', 56, width / 2, 700, (255, 255, 0))
                else:
                    draw_text(screen, 'ГЛАВНОЕ МЕНЮ', 50, width / 2, 700)
                pygame.display.flip()
            if e.type == pygame.MOUSEBUTTONUP and width / 2 - 180 < mp[0] < width / 2 + 180 and 580 < mp[1] < 660:
                if e.button == 1:
                    waiting = False
            if e.type == pygame.MOUSEBUTTONUP and width / 2 - 180 < mp[0] < width / 2 + 180 and 680 < mp[1] < 760:
                if e.button == 1:
                    waiting = False
                    main_menu()


# пауза
def pause():
    pygame.mouse.set_visible(True)
    screen.fill((0, 0, 0))
    draw_text(screen, 'ПАУЗА', 100, width / 2, 100)
    draw_text(screen, 'ПРОДОЛЖИТЬ', 50, width / 2, 600)
    draw_text(screen, 'ГЛАВНОЕ МЕНЮ', 50, width / 2, 700)
    draw_text(screen, 'Счёт: ' + str(score), 60, width / 2, 400)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        screen.fill((0, 0, 0))
        draw_text(screen, 'ПАУЗА', 100, width / 2, 100)
        draw_text(screen, 'Счёт: ' + str(score), 60, width / 2, 400)
        mp = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.MOUSEMOTION:
                if width / 2 - 180 < mp[0] < width / 2 + 180 and 580 < mp[1] < 660:
                    draw_text(screen, 'ПРОДОЛЖИТЬ', 56, width / 2, 600, (255, 255, 0))
                else:
                    draw_text(screen, 'ПРОДОЛЖИТЬ', 50, width / 2, 600)
                if width / 2 - 180 < mp[0] < width / 2 + 180 and 680 < mp[1] < 760:
                    draw_text(screen, 'ГЛАВНОЕ МЕНЮ', 56, width / 2, 700, (255, 255, 0))
                else:
                    draw_text(screen, 'ГЛАВНОЕ МЕНЮ', 50, width / 2, 700)
                pygame.display.flip()
            if e.type == pygame.MOUSEBUTTONUP and width / 2 - 180 < mp[0] < width / 2 + 180 and 580 < mp[1] < 660:
                if e.button == 1:
                    waiting = False
            if e.type == pygame.MOUSEBUTTONUP and width / 2 - 180 < mp[0] < width / 2 + 180 and 680 < mp[1] < 760:
                if e.button == 1:
                    waiting = False
                    main_menu()


# получить рекорд из файла
def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


# записать рекорд в файл
def set_record(current_score):
    new_record = current_score
    with open('record', 'w') as f:
        f.write(str(new_record))


# функция добавления врагов случайного типа (верхние, нижние, правые или левые)
def spawn_enemies():
    generate = random.randrange(1, 5)
    if generate == 1:
        en_top = EnemiesTop()
        all_sprites.add(en_top)
        enemies.add(en_top)
    if generate == 2:
        en_right = EnemiesRight()
        all_sprites.add(en_right)
        enemies.add(en_right)
    if generate == 3:
        en_left = EnemiesLeft()
        all_sprites.add(en_left)
        enemies.add(en_left)
    if generate == 4:
        en_bottom = EnemiesBottom()
        all_sprites.add(en_bottom)
        enemies.add(en_bottom)


# функция загрузки изображений и их обработки для дальнейшего использования
def load_image(name, color_key=None):
    image = pygame.image.load(path.join('data/images', name)).convert()
    if color_key is not None:
        if color_key == 1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


# функция загрузки звуковых эффектов
def load_sound(name, volume):
    sound = pygame.mixer.Sound(path.join('data/sounds', name))
    sound.set_volume(volume)
    return sound


# функция добавления текста
def draw_text(surf, text, size, x, y, color=(255, 255, 255)):
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Robot Bodygun vs Demons')
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))

# загрузка в массивы спрайтов персонажа
player_walk_top = [load_image('player_top1.png', 1), load_image('player_top2.png', 1), load_image('player_top1.png', 1),
                   load_image('player_top3.png', 1), ]
player_walk_bottom = [load_image('player_bottom1.png', 1), load_image('player_bottom2.png', 1),
                      load_image('player_bottom1.png', 1), load_image('player_bottom3.png', 1)]
player_walk_left = [load_image('player_left1.png', 1), load_image('player_left2.png', 1),
                    load_image('player_left1.png', 1), load_image('player_left3.png', 1)]
player_walk_right = [load_image('player_right1.png', 1), load_image('player_right2.png', 1),
                     load_image('player_right1.png', 1), load_image('player_right3.png', 1)]
player_walk_top_right = [load_image('player_top_right1.png', 1), load_image('player_top_right2.png', 1),
                         load_image('player_top_right1.png', 1), load_image('player_top_right3.png', 1)]
player_walk_top_left = [load_image('player_top_left1.png', 1), load_image('player_top_left2.png', 1),
                        load_image('player_top_left1.png', 1), load_image('player_top_left3.png', 1)]
player_walk_bottom_right = [load_image('player_bottom_right1.png', 1), load_image('player_bottom_right2.png', 1),
                            load_image('player_bottom_right1.png', 1), load_image('player_bottom_right3.png', 1)]
player_walk_bottom_left = [load_image('player_bottom_left1.png', 1), load_image('player_bottom_left2.png', 1),
                           load_image('player_bottom_left1.png', 1), load_image('player_bottom_left3.png', 1)]

# загрузка изображений
en_r_img = load_image('enemy_right.png', 1)
en_l_img = load_image('enemy_left.png', 1)
en_t_img = load_image('enemy_top.png', 1)
en_b_img = load_image('enemy_bottom.png', 1)
bullet_img = load_image('bullet.png')
background_img = load_image('bg.png')
background_rect = background_img.get_rect()
lives3_img = load_image('heart3.png')
lives2_img = load_image('heart2.png')
lives1_img = load_image('heart1.png')
image_lives = lives3_img
heart_img = load_image('heart.png', 1)
menu_img = load_image('menu.png')
menu_rect = menu_img.get_rect()
pygame.display.set_icon(player_walk_top[0])

# добавление спрайты в группы
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
hearts = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# загрузка завуковых эффектов и фоновой музыки
shoot_sounds = [load_sound('shoot.wav', 0.4), load_sound('shoot1.wav', 0.4)]
healing_sound = load_sound('healing.wav', 0.6)
hit_enemy_sound = load_sound('hit_enemy.wav', 0.7)
hit_player_sound = load_sound('hit.wav', 0.7)
game_over_sound = load_sound('game_over.wav', 0.9)
pygame.mixer.music.load(path.join('data/sounds', 'music.mp3'))
pygame.mixer.music.set_volume(0.3)

# каждые две минуты появляется сердечко, увеличивающее количество жизней игрока
spawn_heart_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_heart_event, 120000)

# добавление в игру первых пяти врагов
for i in range(5):
    spawn_enemies()

# cчётчики убийств и полученных очков
kill_counter = 0
score = 0

state_music = 1
pygame.mixer.music.play(loops=-1)

game_over = False
menu = True
pause_game = False
# основной цикл
running = True
while running:
    if menu:
        main_menu()
        menu = False

    if pause_game:
        pause()
        pause_game = False

    if game_over:
        over()
        game_over = False
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        hearts = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(5):
            spawn_enemies()
        score = 0

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == spawn_heart_event:
            heart = Heart()
            all_sprites.add(heart)
            hearts.add(heart)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                state_music = -state_music
                if state_music == 1:
                    pygame.mixer.music.play(loops=-1)
                elif state_music == -1:
                    pygame.mixer.music.stop()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause_game = True

    screen.blit(background_img, background_rect)
    pygame.mouse.set_visible(False)
    all_sprites.update()

    # обработка столкновений врагов и игрока
    hits = pygame.sprite.spritecollide(player, enemies, True)
    if hits:
        hit_player_sound.play()
        player.lives -= 1
        spawn_enemies()

    # обработка получения жизни игроком
    hits = pygame.sprite.spritecollide(player, hearts, True)
    if hits:
        player.lives += 1
        healing_sound.play()

    # обработка столкновений врагов и выстрелов
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        hit_enemy_sound.play()
        kill_counter += 1
        score += 10
        spawn_enemies()

    # добавление нового врага случайного типа после каждого третьего убийства
    if kill_counter == 3:
        spawn_enemies()
        kill_counter = 0

    # отображение количества жизней персонажа
    if player.lives > 3:
        player.lives = 3
    elif player.lives == 3:
        image_lives = lives3_img
    elif player.lives == 2:
        image_lives = lives2_img
    elif player.lives == 1:
        image_lives = lives1_img
    elif player.lives <= 0:
        player.life = 0
        game_over = True
    screen.blit(image_lives, (410, 30))

    all_sprites.draw(screen)
    draw_text(screen, 'Счет: ' + str(score), 36, 800, 20)
    draw_text(screen, 'Жизни: ', 36, 350, 20)
    pygame.display.flip()
