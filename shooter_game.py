from pygame import *
from random import randint
from time import time as timer
import sys
import os
 
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    elif hasattr(sys, "_MEIPASS2"):
        return os.path.join(sys._MEIPASS2, relative_path)
    else:
        return os.path.join(os.path.abspath("."), relative_path)
 
image_folder = resource_path(".")
# Инциализация
mixer.init()
font.init()
 
# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 150, 0)
RED = (150, 0, 0)
YELLOW = (150, 150, 0)
 
# Параметры
WIDTH = 700
HEIGHT = 500
FPS = 60
 
# Спрайты и звуки
img_hero = os.path.join(image_folder, "rocket.png")
img_back = os.path.join(image_folder, "galaxy.jpg")
img_ufo = os.path.join(image_folder, "ufo.png")
img_bullet = os.path.join(image_folder, "bullet.png")
img_asteroid = os.path.join(image_folder, "asteroid.png")
 
music_back = os.path.join(image_folder,"space.ogg")
sound_fire = os.path.join(image_folder,"fire.ogg")
 
# Настройки звука
mixer.music.load(music_back)
mixer.music.play()
mixer.music.set_volume(0.1)
 
fire = mixer.Sound(sound_fire)
 
# Текст и шрифты
font_score = font.Font(None, 36)
font_text = font.Font(None, 80)
 
win_text = font_text.render("YOU WIN!!!", True, GREEN)
lose_text = font_text.render("YOU LOSE!!!", True, RED)
 
# Счёт
score = 0
lost = 0
max_score = 10
max_lost = 30
life = 3
 
# Основной экран
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Шутер")
backgorund = transform.scale(image.load(img_back), (WIDTH, HEIGHT))
clock = time.Clock()
 
class GameSprite(sprite.Sprite):
    def __init__(self, p_img: str, x: int, y: int, w: int, h: int, speed: int):
        super().__init__()
        self.image = transform.scale(image.load(p_img), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
class Player(GameSprite):
    def __init__(self, p_img: str, x: int, y: int, w: int, h: int, speed: int, max_bullets: int):
        super().__init__(p_img, x, y, w, h, speed)
        self.max_bullets = max_bullets
        self.current_bullets = max_bullets
        self.last_reload_time = 0
        self.reload_duration = 3
        self.reloading = False
 
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < WIDTH - 60:
            self.rect.x += self.speed 
 
    def fire(self):
        if self.current_bullets > 0:
            bullet = Bullet(img_bullet, self.rect.centerx - 8, self.rect.top, 15, 20, 15)
            bullets.add(bullet)
            self.current_bullets -= 1
        else:
            self.start_reload()
 
    def start_reload(self):
        self.reloading = True
        self.last_reload_time = timer()
 
    def reload(self):
        if self.reloading:
            now_time = timer()
            if now_time - self.last_reload_time >= self.reload_duration:
                self.current_bullets = self.max_bullets
                self.reloading = False
 
class AmmoIndicator(sprite.Sprite):
    def __init__(self, p_img: str, x: int, y: int, w: int, h: int, max_bullets: int):
        super().__init__()
        self.image = transform.scale(image.load(p_img), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
        self.max_bullets = max_bullets
 
    def update(self, current_bullets):
        self.rect.x = WIDTH - self.rect.width - 10
        self.rect.y = HEIGHT - self.rect.height - 10
        for i in range(self.max_bullets):
            if i < current_bullets:
                window.blit(self.image, (self.rect.x - i * (self.rect.width + 5), self.rect.y))
 
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= HEIGHT:
            self.rect.x = randint(10, WIDTH - 100)
            self.rect.y = 0
            lost += 1 # lost = lost + 1
 
class Astetoid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= HEIGHT:
            self.rect.x = randint(10, WIDTH - 100)
            self.rect.y = 0
 
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed # (15) или self.rect.y += self.speed (-15)
        if self.rect.y < 0:
            self.kill()
 
def restart_game():
    global score, lost, finish, life
    score = 0
    lost = 0
    life = 3
    finish = False
    mixer.music.play()
 
    player.reload()
 
    for m in monsters:
        m.kill()
 
    for b in bullets:
        b.kill()
 
    for a in asteroids:
        a.kill()
 
    time.delay(3000) # 3 sec.
 
    for i in range(6):
        monster = Enemy(img_ufo, randint(10, WIDTH - 100), -50, 100, 50, randint(1, 5))
        monsters.add(monster)
 
    for i in range(3):
        asteroid = Astetoid(img_asteroid, randint(10, WIDTH - 100), -50, 50, 50, randint(1, 3))
        asteroids.add(asteroid)
 
player = Player(img_hero, 5, HEIGHT - 100, 60, 100, 10, 5)
bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()
 
ammo_indicator = AmmoIndicator(img_bullet, WIDTH - 10, HEIGHT - 10, 15, 20, 5)
 
for i in range(6):
    monster = Enemy(img_ufo, randint(10, WIDTH - 100), -50, 100, 50, randint(1, 5))
    monsters.add(monster)
 
for i in range(3):
    asteroid = Astetoid(img_asteroid, randint(10, WIDTH - 100), -50, 50, 50, randint(1, 3))
    asteroids.add(asteroid)
 
# Основной цикл
run = True
finish = False
 
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN: # MOUSEBUTTONDOWN
            if e.key == K_SPACE: # key.button == 1
                player.fire()
                fire.play()
            if e.key == K_r:
                restart_game()
 
    if not finish: # finish != False
        window.blit(backgorund, (0, 0))
        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
 
        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()
 
        ammo_indicator.update(player.current_bullets)
 
        if player.reloading:
            reload_text = font_text.render("ПЕРЕЗАРЯДКА...", True, RED)
            window.blit(reload_text, (260, 460))
            player.reload()
 
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for collide in collides:
            score += 1
            monster = Enemy(img_ufo, randint(10, WIDTH - 100), -50, 100, 50, randint(1, 5))
            monsters.add(monster)
 
        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, monsters, True)
            sprite.spritecollide(player, asteroids, True)
            life -= 1
 
        sprite.groupcollide(asteroids, bullets, False, True)
 
        if score >= max_score:
            finish = True
            window.blit(win_text, (200, 200))
            mixer.music.stop()
            # restart_game()
 
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose_text, (200, 200))
            mixer.music.stop()
            # restart_game()
 
        score_text = font_score.render("Счёт: " + str(score), True, WHITE)
        window.blit(score_text, (10, 20))
 
        lost_text = font_score.render("Пропущено: " + str(lost), True, WHITE)
        window.blit(lost_text, (10, 50))
 
        if life >= 3:
            life_color = GREEN
        if life == 2:
            life_color = YELLOW
        if life == 1:
            life_color = RED
 
        text_life = font_score.render("Жизни: " + str(life), True, life_color)
        window.blit(text_life, (570, 10))
 
    display.update()
    clock.tick(FPS)