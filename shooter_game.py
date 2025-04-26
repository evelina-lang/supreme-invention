#Создай собственный Шутер!
from random import randint
from pygame import *
win_widh = 700
win_heh = 500
im_back = "galaxy.jpg"
im_hero = "rocket.png"
im_enemy = "ufo.png"
im_bullet = "bullet.png"

font.init()
font2 = font.Font(None, 36)
score = 0
lost = 0
max_lost = 3
max_score = 10
win = font2.render('YOU WIN!', True, (255, 228, 181))
lose = font2.render('YOU LOSE!', True, (255, 228, 181))
window = display.set_mode((win_widh, win_heh))
display.set_caption('Шутер')
background = transform.scale(image.load(im_back), (win_widh, win_heh))



class  GameSprite (sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset (self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_widh - 80:
            self.rect.x += self.speed 
    def fire(self):
        bullet = Bullet(im_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
ship = Player(im_hero, 5, win_heh - 100, 80, 100, 20)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_heh:
            self.rect.x = randint(80, win_widh - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
    

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(im_enemy, randint(80, win_widh - 80), -40, 80, 50, randint(1,5))
    monsters.add(monster)

bullets = sprite.Group()


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_soun = mixer.Sound('fire.ogg')

finish = False
run = True
while  run :
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_soun.play()
                ship.fire()
    if not finish:
        window.blit(background,  (0, 0))
        
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        ship.update()
        ship.reset()
        
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1 
            monster = Enemy(im_enemy, randint(80, win_widh - 80), - 40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
        if score >= max_score:
            finish = True
            window.blit(win, (200, 200))

        
        text = font2.render('Счет: ' + str(score), 1, (255, 228, 181))
        window.blit(text, (10, 20))
        text_lost = font2.render('Пропущенно: ' + str(lost), 1, (255, 228, 181))
        window.blit(text_lost, (10, 50))
        
        display.update()
    else:
        finish = False 
        score = 0
        lost = 0
        for t in bullets:
            t.kill()
        for m in monsters:
            m.kill()
        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(im_enemy, randint(80, win_widh - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
    time.delay(50)














