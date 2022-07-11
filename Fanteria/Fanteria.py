from pygame import *
from random import randint
from time import time as timer #импортировать под названием таймер
import ctypes
import sys
import math

#user32 = ctypes.windll.user32
#win_x = user32.GetSystemMetrics(0)
#win_y = user32.GetSystemMetrics(1)

win_x = 1366
win_y = 768

window = display.set_mode((win_x,win_y),flags=FULLSCREEN)
display.set_caption('')
background = transform.scale(image.load('fon.png'),(win_x,win_y))

global Game
Game = True
Finish = False

font.init()
font1 = font.SysFont('Verdana',50)
font2 = font.SysFont('Verdana',35)
font_reload = font.SysFont('Verdana',28)

FPS = 60
clock = time.Clock()

bullets = sprite.Group()
enemy = sprite.Group()
enemy_left_group = sprite.Group()
enemy_up_group = sprite.Group()
enemy_down_group = sprite.Group()

rel_time = False
num_fire = 0
lost = 0
score = 0

mixer.init()
music = randint(1,2)
pusto_pistol_sound = mixer.Sound('pusto_pistol.ogg') #попытка выстрелить с пустым магазином
fire_sound2 = mixer.Sound('fire2.ogg') #звук выстрела из пистолета 2
lose_sound1 = mixer.Sound('sad1.ogg') #музыка при поражении 1
lose_sound2 = mixer.Sound('sad2.ogg') #музыка при поражении 2 

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.size_x = size_x
        self.size_y = size_y
        self.original_image = transform.scale(image.load(player_image),(size_x,size_y))
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    def image_reset(self,new_image,size_x,size_y): 
        self.image = transform.scale(image.load(new_image),(size_x,size_y))
        self.reset()

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed() 
        if not keys[K_LSHIFT]:
            if self.rect.x >= 400:
                if keys[K_a]:
                    self.image_reset('Hero_left.png',100,175)
                    self.rect.x -= self.speed
            if self.rect.x <= 782:
                if keys[K_d]:
                    self.image_reset('Hero_right.png',100,175)
                    self.rect.x += self.speed
            if self.rect.y <= 450:
                if keys[K_s]:
                    self.image_reset('Hero_zad.png',175,100)
                    self.rect.y += self.speed
            if self.rect.y >= 270:
                if keys[K_w]:
                    self.image_reset('Hero.png',175,100)
                    self.rect.y -= self.speed
        if keys[K_LSHIFT]:
            if self.rect.x >= 400:
                if keys[K_a]:
                    self.rect.x -= self.speed+10
            if self.rect.x <= 782:
                if keys[K_d]:
                    self.rect.x += self.speed+10
            if self.rect.y <= 450:
                if keys[K_s]:
                    self.rect.y += self.speed+10
            if self.rect.y >= 270:
                if keys[K_w]:
                    self.rect.y -= self.speed+10
    
    def skin(self):
        keys = key.get_pressed() 
        if keys[K_UP]:
            self.image_reset('Hero.png',175,100)
        if keys[K_DOWN]:
            self.image_reset('Hero_zad.png',175,100)
        if keys[K_LEFT]:
            self.image_reset('Hero_left.png',100,175)
        if keys[K_RIGHT]:
            self.image_reset('Hero_right.png',100,175)
    
    def rotate(self):
        mouse_x, mouse_y = mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y

        angle = math.atan2(rel_y, rel_x)
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

        self.image = transform.rotate(self.original_image, int(angle))
        position = self.rect.x, self.rect.y
        self.rect = self.image.get_rect(center=position)
    
    def fire_left(self):
        bullet = Bullet('Bullet_left.png',self.rect.x+27,self.rect.y+54 ,10,5,15)
        bullets.add(bullet)
    
    def fire_right(self):
        bullet_right = Bullet_right('Bullet_right.png',self.rect.x+60, self.rect.y+116, 10,5,15)
        bullets.add(bullet_right)
    
    def fire_up(self):
        bullet_up = Bullet_up('Bullet_up.png',self.rect.x+116, self.rect.y+45, 5,10,15)
        bullets.add(bullet_up)
    
    def fire_down(self):
        bullet_down = Bullet_down('Bullet_down.png',self.rect.x+55, self.rect.y+55, 5,10,15)
        bullets.add(bullet_down)

class Bullet(GameSprite):
    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < 0 or self.rect.x > win_x:
            self.kill()

class Bullet_right(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x < 0 or self.rect.x > win_x:
            self.kill()

class Bullet_up(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0 or self.rect.y > win_y:
            self.kill()

class Bullet_down(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0 or self.rect.y > win_y:
            self.kill()

class Enemy_left(GameSprite):
    def update(self):
        self.rect.x -= self.speed
        global lost
        if self.rect.x < 782:
            self.rect.x = win_x-100
            self.rect.y = randint(280,440)
            lost += 1

class Enemy_right(GameSprite):
    def update(self):
        self.rect.x += self.speed
        global lost
        if self.rect.x > 400:
            self.rect.x = 0
            self.rect.y = randint(280,440)
            lost += 1

class Enemy_down(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 270:
            self.rect.x = Hero.rect.x
            self.rect.y = 0
            lost += 1

class Enemy_up(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        global lost
        if self.rect.y < 450:
            self.rect.x = randint(500,600)
            self.rect.y = win_y
            lost += 1

class Button():
    def __init__(self, color, x, y, w, h, text, txt_color):

        self.width = w
        self.height = h
        self.color = color

        self.image = Surface([self.width, self.height])
        self.image.fill((color))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.text = text
        self.txt_color = txt_color
        self.txt_image = font1.render(text, True, txt_color)

    def draw(self, shift_x, shift_y): # цей метод малює кнопку із тектом в середині. Сам текст зміщенний на величини shift_x та shift_y
        window.blit(self.image, (self.rect.x, self.rect.y))
        window.blit(self.txt_image, (self.rect.x + shift_x, self.rect.y + shift_y))
       
    def fill(self,color):
       draw.rect(window, color, self.rect)
    
    def outline(self, frame_color, thickness): #обводка
       draw.rect(window, frame_color, self.rect, thickness)
      

def menu(): # меню

    menu = True
    # фонова музика
    #mixer.music.load('sounds/menu.ogg')
    #mixer.music.play()
    global window, Game

    while menu:

        for e in event.get(): # закриваємо вікно гри
            if e.type == QUIT: 
                menu = False

        clock.tick(FPS)
        pos_x, pos_y = mouse.get_pos() # де сховався вказівник?

        background = transform.scale(image.load('fon.png'),(win_x,win_y))
        window.blit(background,(0,0))
        # відображення кнопок
        btn_exit.draw(100,10)
        btn_exit.outline((0,0,0),3)

        btn_settings.draw(70,10)
        btn_settings.outline((0,0,0),3)

        btn_play.draw(100,10)
        btn_play.outline((0,0,0),3)

        btn_education.draw(10,13)
        btn_education.outline((0,0,0),3)

        for e in event.get():
      
            if btn_exit.rect.collidepoint((pos_x, pos_y)) and e.type == MOUSEBUTTONDOWN:
                #click.play()
                Game = False
                menu = False
            
            if btn_settings.rect.collidepoint((pos_x,pos_y)) and e.type == MOUSEBUTTONDOWN:
                settings()
            
            if btn_play.rect.collidepoint((pos_x,pos_y)) and e.type == MOUSEBUTTONDOWN:
                play()

            if btn_education.rect.collidepoint((pos_x,pos_y)) and e.type == MOUSEBUTTONDOWN:
                education()
            #if btn_exit.rect.collidepoint(mousePos):  
                #btn_exit.fill((102,102,102))

            if e.type == QUIT:
                Game = False
                menu = False
        
            if e.type == KEYDOWN:
                if e.key == K_1:
                    window = display.set_mode((win_x,win_y),flags=FULLSCREEN) #ПОЛНОЭКРАННЫЙ
                if e.key == K_ESCAPE:
                    window = display.set_mode((win_x,win_y),flags=RESIZABLE) #ОКОННЫЙ

        display.update()

def settings(): 
    global window, Game, menu, win_x, win_y, play, FPS
    settings = True
    screen = 0
    #mixer.music.stop()

    while settings:

        for e in event.get(): # закриваємо вікно гри
        
            if e.type == KEYDOWN:
                    if e.key == K_1:
                        window = display.set_mode((win_x,win_y),flags=FULLSCREEN) #ПОЛНОЭКРАННЫЙ
                    if e.key == K_ESCAPE:
                        window = display.set_mode((win_x,win_y),flags=RESIZABLE) #ОКОННЫЙ

        #time.delay(15)
        # відображення тексту з правилами керування
        
        background = transform.scale(image.load('Settings.png'),(win_x,win_y))
        window.blit(background,(0,0))

        btn1280_720.draw(70,10)
        btn1280_720.outline((0,0,0),3)

        btn1366_768.draw(70,10)
        btn1366_768.outline((0,0,0),3)

        btn_FPS30.draw(8,10)
        btn_FPS30.outline((0,0,0),3)

        btn_FPS60.draw(8,10)
        btn_FPS60.outline((0,0,0),3)

        btn_fullscreen.draw(8,10)
        btn_fullscreen.outline((0,0,0),3)

        btn_windowscreen.draw(0,10)
        btn_windowscreen.outline((0,0,0),3)

        pos_x, pos_y = mouse.get_pos()

        for e in event.get():
            # повернення до меню
            if btn1280_720.rect.collidepoint((pos_x, pos_y)) and e.type == MOUSEBUTTONDOWN:
                win_x = 1280
                win_y = 720
                if screen == FULLSCREEN or screen == RESIZABLE:
                    window = display.set_mode((win_x,win_y), flags=screen)
                else:
                    window = display.set_mode((win_x,win_y))
                background = transform.scale(image.load('settings.png'),(win_x,win_y))
            
            if btn1366_768.rect.collidepoint((pos_x,pos_y)) and e.type == MOUSEBUTTONDOWN:
                win_x = 1366
                win_y = 768
                if screen == FULLSCREEN or screen == RESIZABLE:
                    window = display.set_mode((win_x,win_y), flags=screen)
                else:
                    window = display.set_mode((win_x,win_y))
                background = transform.scale(image.load('settings.png'),(win_x,win_y))
            
            if btn_FPS30.rect.collidepoint((pos_x,pos_y)) and e.type == MOUSEBUTTONDOWN:
                FPS = 30
            
            if btn_FPS60.rect.collidepoint((pos_x,pos_y)) and e.type == MOUSEBUTTONDOWN:
                FPS = 60
            
            if FPS == 60:
                btn_FPS60.color = (0,255,0)
                btn_FPS30.color = (255,0,0)
                btn_FPS60.image.fill((0,255,0))
                btn_FPS30.image.fill((255,0,0))
            
            if FPS == 30:
                btn_FPS60.color = (255,0,0)
                btn_FPS30.color = (0,255,0)
                btn_FPS60.image.fill((255,0,0))
                btn_FPS30.image.fill((0,255,0))
            
            if btn_fullscreen.rect.collidepoint((pos_x,pos_y)) and e.type == MOUSEBUTTONDOWN:
                screen = FULLSCREEN
                window = display.set_mode((win_x,win_y), flags=screen)
            
            if btn_windowscreen.rect.collidepoint((pos_x,pos_y)) and e.type == MOUSEBUTTONDOWN:
                screen = RESIZABLE
                window = display.set_mode((win_x,win_y), flags=screen)

            # закриваємо вікно
            if e.type == QUIT:
                menu = False
                Game = False
                settings = False
        
            if e.type == KEYDOWN:
                if e.key == K_1:
                    window = display.set_mode((win_x,win_y),flags=FULLSCREEN) #ПОЛНОЭКРАННЫЙ
                if e.key == K_ESCAPE:
                    window = display.set_mode((win_x,win_y),flags=RESIZABLE) #ОКОННЫЙ

        display.update()

def play():
    global window, Game, menu, win_x, win_y,settings,rel_time,num_fire,score,lost,music, FPS
    play = True
    # фонова музика
    mixer.music.load('fon_sound.mp3')
    mixer.music.play()

    while play:

        pos_x, pos_y = mouse.get_pos() # де сховався вказівник?

        background = transform.scale(image.load('Map.png'),(win_x,win_y))
        window.blit(background,(0,0))
        Hero.reset()
        Hero.update()
        Hero.skin()
        bullets.update()
        bullets.draw(window) 
        enemy.update()
        enemy.draw(window) 
        enemy_left_group.update()
        enemy_left_group.draw(window) 
        enemy_up_group.update()
        enemy_up_group.draw(window)
        enemy_down_group.update()
        enemy_down_group.draw(window)

        score_text = font1.render('Счёт:'+str(score),1,(23,114,69))
        window.blit(score_text,(20,10))

        text_lose = font1.render('Пропущено:' + str(lost),1,(150,0,0))
        window.blit(text_lose,(20,60))

        collides1 = sprite.groupcollide(enemy,bullets,True,True)
        collides2 = sprite.groupcollide(enemy_left_group,bullets,True,True)
        collides3 = sprite.groupcollide(enemy_up_group,bullets,True,True)
        collides4 = sprite.groupcollide(enemy_down_group,bullets,True,True)

        for c in collides1:
            score = score + 1
            enemy_right = Enemy_right('Enemy_right.png',0,randint(280,440),100,175,randint(3,10))
            enemy.add(enemy_right)
        
        for c in collides2:
            score = score + 1
            enemy_left = Enemy_left('Enemy_left.png',win_x-100,randint(280,440),100,175,randint(3,10))
            enemy_left_group.add(enemy_left)
        
        for c in collides3:
            score = score + 1
            enemy_up = Enemy_up('Enemy.png',randint(500,600),win_y,175,100,randint(3,10))
            enemy_up_group.add(enemy_up)
        
        for c in collides4:
            score = score + 1
            enemy_down = Enemy_down('Enemy_zad.png',Hero.rect.x,0,175,100,randint(3,10))
            enemy_down_group.add(enemy_down)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font_reload.render('Перезарядка пистолета...',1,(150,0,0))
                window.blit(reload,(Hero.rect.x,Hero.rect.y-30))
            else:
                num_fire = 0
                rel_time = False
                #patrons_pistolet = 5

        if int(lost) >= 15:
            mixer.music.pause()
            if music == 1:
                lose_sound1.play()
                music = 0
            if music == 2:
                lose_sound2.play()
                music = 0
            for c in enemy:
                c.kill()
            
            for c in enemy_up_group:
                c.kill()

            for c in enemy_left_group:
                c.kill()
            
            for c in enemy_down_group:
                c.kill()
            
            lose = font1.render('ВЫ ПРОИГРАЛИ!',1,(150,0,0))
            window.blit(lose,(win_x/2-230,win_y/2-10))

        for e in event.get():

            if e.type == QUIT:
                play = False

            if e.type == KEYDOWN:
                if e.key == K_1:
                    window = display.set_mode((win_x,win_y),flags=FULLSCREEN) #ПОЛНОЭКРАННЫЙ
                if e.key == K_ESCAPE:
                    window = display.set_mode((win_x,win_y),flags=RESIZABLE) #ОКОННЫЙ
            
                if e.key == K_LEFT:
                    if num_fire < 5 and rel_time == False:
                        num_fire += 1
                        Hero.fire_left()
                        fire_sound2.play()
                    #if patrons_pistolet != 0:
                        #patrons_pistolet -= 1
                    if num_fire >=5 and rel_time == False:
                        last_time = timer()
                        rel_time = True
                    if num_fire >= 5 and rel_time == True:
                        pusto_pistol_sound.play()
                
                if e.key == K_RIGHT:
                    if num_fire < 5 and rel_time == False:
                        num_fire += 1
                        Hero.fire_right()
                        fire_sound2.play()
                    #if patrons_pistolet != 0:
                        #patrons_pistolet -= 1
                    if num_fire >=5 and rel_time == False:
                        last_time = timer()
                        rel_time = True
                    if num_fire >= 5 and rel_time == True:
                        pusto_pistol_sound.play()

                if e.key == K_UP:
                    if num_fire < 5 and rel_time == False:
                        num_fire += 1
                        Hero.fire_up()
                        fire_sound2.play()
                    #if patrons_pistolet != 0:
                        #patrons_pistolet -= 1
                    if num_fire >=5 and rel_time == False:
                        last_time = timer()
                        rel_time = True
                    if num_fire >= 5 and rel_time == True:
                        pusto_pistol_sound.play()
                
                if e.key == K_DOWN:
                    if num_fire < 5 and rel_time == False:
                        num_fire += 1
                        Hero.fire_down()
                        fire_sound2.play()
                    #if patrons_pistolet != 0:
                        #patrons_pistolet -= 1
                    if num_fire >=5 and rel_time == False:
                        last_time = timer()
                        rel_time = True
                    if num_fire >= 5 and rel_time == True:
                        pusto_pistol_sound.play()

        display.update()
        clock.tick(FPS)

def education():
    global window, Game, play, settings, menu, win_x, win_y,settings,rel_time,num_fire,score,lost,music,background,FPS
    rule = True

    while rule:

        background = transform.scale(image.load('rules.png'),(win_x,win_y))
        window.blit(background,(0,0))

        #time.delay(15)
        # відображення тексту з правилами керування
        educ_1 = font2.render('[1] Для перемещения используйте W,A,S,D',1,(0,255,0))
        educ_2 = font2.render('[2] Для стрельбы используйте стрелочки',1,(0,255,0))
        educ_3 = font2.render('[3] Нажмите 1 или ESCAPE, чтобы включить',1,(0,255,0))
        educ_3b = font2.render('или выключить полноэкранный режим',1,(0,255,0))
        educ_4 = font2.render('[4] Для выхода в меню нажмите на крестик в оконном режиме',1,(0,255,0))
        
        window.blit(educ_1,(50,275))
        window.blit(educ_2,(50,375))
        window.blit(educ_3,(50,475))
        window.blit(educ_3b,(50,525))
        window.blit(educ_4,(50,625))

        pos_x, pos_y = mouse.get_pos()

        for e in event.get(): # закриваємо вікно гри
            if e.type == QUIT: 
                rule = False
                
            if e.type == KEYDOWN:
                    if e.key == K_1:
                        window = display.set_mode((win_x,win_y),flags=FULLSCREEN) #ПОЛНОЭКРАННЫЙ
                    if e.key == K_ESCAPE:
                        window = display.set_mode((win_x,win_y),flags=RESIZABLE) #ОКОННЫЙ

        display.update()

btn_exit = Button((0,100,255),1366/2-200,600,400,100,'Выход',(0,0,0))
btn_settings = Button((0,100,255),1366/2-200,450,400,100,'Настройки',(0,0,0))
btn_play = Button((0,100,255),1366/2-200,300,400,100,'Играть',(0,0,0))
btn_education = Button((0,100,255),1366/2+200,450,50,100,'?',(0,0,0))

btn1280_720 = Button((255,255,0),1366/2-200,300,400,100, '1280х720',(0,0,0))
btn1366_768 = Button((255,255,0),1366/2-200,450,400,100, '1366x768',(0,0,0))
btn_FPS30 = Button((255,255,0),1366/2-200,600,80,80, '30',(0,0,0)) 
btn_FPS60 = Button((255,255,0),1366/2-100,600,80,80, '60',(0,0,0))
btn_fullscreen = Button((255,255,0), 1366/2+10,600,80,80, 'FS', (0,0,0))
btn_windowscreen = Button((255,255,0),1366/2+120,600,82,80,'WS',(0,0,0))

Hero = Player('Hero.png',1366/2,300,175,100,25)
for i in range(1,2):
    enemy_left = Enemy_left('Enemy_left.png',win_x-100,randint(280,440),100,175,randint(3,10))
    enemy_left_group.add(enemy_left)

    enemy_right = Enemy_right('Enemy_right.png',0,randint(280,440),100,175,randint(3,10))
    enemy.add(enemy_right)

    enemy_down = Enemy_down('Enemy_zad.png',Hero.rect.x,0,175,100,randint(3,10))
    enemy_down_group.add(enemy_down)

    enemy_up = Enemy_up('Enemy.png',randint(500,600),win_y,175,100,randint(3,10))
    enemy_up_group.add(enemy_up)
    

while Game:
    menu()
    #window.blit(background,(0,0))

    display.update()

    for e in event.get():
        if e.type == QUIT:
            Game = False
        
        if e.type == KEYDOWN:
            if e.key == K_1:
                window = display.set_mode((win_x,win_y),flags=FULLSCREEN) #ПОЛНОЭКРАННЫЙ
            if e.key == K_ESCAPE:
                window = display.set_mode((win_x,win_y),flags=RESIZABLE) #ОКОННЫЙ

    clock.tick(FPS)
