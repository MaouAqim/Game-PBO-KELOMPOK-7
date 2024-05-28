import math  #Modul math untuk melakukan operasi matematika
import pygame, sys #Modul yang menjadi dasar dari game, berperan sebagai class parent
import random #Modul random untuk mengacak posisi musuh
import image #Modul yang berisi file gambar
import sound #Modul sound untuk mengatur suara melalui file sound
from helper import draw_text
import os


#fitur display/pembangun game
FPS=60
WIDTH=1000
HEIGHT=600
RED = (255, 255, 255, 255)

#class pygame (Class Utama/Parent)
pygame.init()
layar = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Starborne Strife")
fps = pygame.time.Clock()
background = pygame.image.load(os.path.abspath("image/bg.png"))
background = pygame.transform.scale(background,(layar.get_width(),layar.get_height()))
pause = False

def pause_screen():
    draw_text(layar, "Pause", 50, WIDTH / 2, HEIGHT / 2)
    draw_text(layar, "Press P to Resume", 30, WIDTH / 2, HEIGHT / 2 + 50)
    # pygame.display.flip()

def pause_game(self):
    self.game_pause = True

    while self.game.is_pause:
        PauseMenu()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.game.is_pause = False
            if event.type == pygame.QUIT:
                self.game.is_pause = False
                self.run()

#Class Pilot (Class Child)
class Pilot(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(image.Pilot,(145,115))
        self.rect=self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom= layar.get_height() - 20
        self.speedx = 8
        self.score_val = 0
        self.life = 5
        self.button = 1
        self.button_time = pygame.time.get_ticks()
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 250
        self.pause = False

    #artibuted movement
    def update(self):
        if self.button >= 2 and pygame.time.get_ticks() - self.button_time > 5000:
            self.button -= 1
            self.button_time = pygame.time.get_ticks()

        key_pressed = pygame.key.get_pressed()
        if not updated:
            if key_pressed[pygame.K_RIGHT]:
                self.rect.x += self.speedx
            if key_pressed[pygame.K_LEFT]:
                self.rect.x -= self.speedx
            if key_pressed[pygame.K_UP]:
                self.rect.y -= self.speedx
            if key_pressed[pygame.K_DOWN]:
                self.rect.y += self.speedx

            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.bottom > layar.get_height():
                self.rect.bottom = layar.get_height()
            if self.rect.top < 0:
                self.rect.top  = 0

    def buttonup(self):
        self.button += 1
        self.button_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay and  not updated:
            self.last_shot = now
            if self.button == 1:
                blast = Blast(pygame.Vector2(self.rect.centerx,self.rect.top))
                all_sprites.add(blast)
                blasts.add(blast)
                sound.missile.play()
            elif self.button >= 2:
                blast1 = Blast(pygame.Vector2(self.rect.centerx-20,self.rect.top))
                all_sprites.add(blast1)
                blasts.add(blast1)
                blast2 = Blast(pygame.Vector2(self.rect.centerx+20,self.rect.top))
                all_sprites.add(blast2)
                blasts.add(blast2)
                sound.missile.play()  

    def show_lifepoints(self):
        draw_text(layar, f"life points : {self.life}", 20, WIDTH-115, HEIGHT-590)

    def show_score(self):
        draw_text(layar, f"Score : {self.score_val}", 20, WIDTH-920, HEIGHT-590)

#Class Musuh atau Lawan
class Ufo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(image.ufo,(80,95))
        self.rect=self.image.get_rect()
        self.radius=self.rect.width*0.1/2
        self.rect.x=random.randrange(0,WIDTH-self.rect.width)
        self.rect.y=random.randrange(-50,-10)
        self.speedx=random.randrange(-1,2)
        self.speedy=random.randrange(1,2)

#Atributed movement
    def update(self):
        if not updated:
            self.rect.x += self.speedx
            self.rect.y += self.speedy
        if self.rect.top > layar.get_height() or self.rect.left>WIDTH or self.rect.right<0:
            self.rect.x=random.randrange(0,WIDTH-self.rect.width)
            self.rect.y=random.randrange(-100,-40)
            self.speedx=random.randrange(-3,3)
            self.speedy=random.randrange(2,8)

#Class Button atau Peluru Tambahan
class Button(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image.button,(35,55))
        self.rect = self.image.get_rect()
        self.radius=self.rect.width*0.1/2
        self.rect.x=random.randrange(0,WIDTH-self.rect.width)
        self.speedy = 5

#Atributed movement
    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()

#Class Blast(Class Child)
class Blast(pygame.sprite.Sprite):
    def __init__(self,position:pygame.Vector2,angle:float=-90):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.rotate(pygame.transform.scale(image.Blast,(25,35)),-angle+180+90)
        self.rect=self.image.get_rect()
        self.rect.midbottom=position
        speedy = 10
        self.velocity = pygame.math.Vector2(math.cos(math.radians(angle))*speedy,math.sin(math.radians(angle))*speedy)

    def update(self):
        if not updated:
            self.rect.midbottom += self.velocity
        if self.rect.bottom < 0 or self.rect.top > layar.get_height() or self.rect.left > WIDTH or self.rect.right < 0:
            self.kill()

#Class Healthbar(Class Child)
#Implementasi Polymorphism
class Healthbar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((WIDTH*4/5, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = 80

#Class AlienBoss(Class Child)
class AlienBoss(pygame.sprite.Sprite):
    def __init__(self, max_health:int, attack_speed:int = 50):
        pygame.sprite.Sprite.__init__(self)
        self.source_image = pygame.transform.rotate(pygame.transform.scale(image.alienBoss,(110,130)),90)
        self._angle = 180
        self.image = pygame.transform.rotate(self.source_image, self.angle)
        self.rect=self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom  = 0

        self.max_health = max_health
        self._health = 0
        self.healthbar = Healthbar()
        self.health = self.max_health
        self.move_in = pygame.Vector2(0,15)
        all_sprites.add(self.healthbar)
        self.tick = 0
        self.alt = False
        self.attack_speed = attack_speed

#Static Method
    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value
        self.healthbar.image.fill((255,0 , 0))
        self.healthbar.image.fill((0, 255, 0), (0, 0, self.healthbar.image.get_width()*self.health/self.max_health, self.healthbar.image.get_height()))

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        if value != self._angle:
            self._angle = value
            self.on_angle_change()

    def on_angle_change(self):
        self.image = pygame.transform.rotate(self.source_image, self.angle)

    def hurt(self, value:int = 10):
        self.health -= value
        if self.health <= 0:
            self.kill()
            self.healthbar.kill()


    def shoot(self):
        if not updated:
            self.alt = not self.alt
            if self.alt:
                blast = Blast(pygame.Vector2(self.rect.centerx-30,self.rect.bottom), -self.angle)
            else :
                blast = Blast(pygame.Vector2(self.rect.centerx+30,self.rect.bottom), -self.angle)
            all_sprites.add(blast)
            hazard.add(blast)


    def update(self):
        if not updated:
            self.rect.y += self.move_in.y
            if self.move_in.y > 0:
                self.move_in.y *= 0.95

            self.tick += 1

            p_center = Pilot.rect.center
            s_center = self.rect.center
            angle_in_rads = math.atan2(p_center[1] - s_center[1], p_center[0] - s_center[0])

            self.angle = -math.degrees(angle_in_rads)
            if self.tick > self.attack_speed:
                self.tick = 0
                self.shoot()

    def kill(self):
        self.healthbar.kill()
        return super().kill()


#Tampilan kedua setelah menu()
def waiting_screen():
    layar.blit(pygame.transform.scale(image.background,(layar.get_width(),layar.get_height())),(0,0))
    draw_text(layar, "STARBORNE STRIFE", 50, WIDTH/2, HEIGHT/4)
    draw_text(layar, "Press any key to play", 25, WIDTH/2, HEIGHT/2+20)
    draw_text(layar, "Arrow keys to move, Space key to Shoot", 18, WIDTH/2, HEIGHT*3/4+60)

    pygame.display.flip()
    waiting = True
    while waiting:
        fps.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

#Tampilan awal
def menu():
    layar.blit(pygame.transform.scale(image.background,(layar.get_width(),layar.get_height())),(0,0))
    draw_text(layar, "STARBORNE STRIFE", 65, WIDTH/2, HEIGHT/7)    
    pygame.display.flip()
    yvar=350
    xvar=500
    draw_text(layar, "START", 55, WIDTH/2, yvar-25) 
    draw_text(layar, "QUIT",30, WIDTH/2, 550)  
    pygame.draw.circle(layar, (RED), (xvar,yvar), 112,5)

    waiting = True
    while waiting:
        fps.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                xpos, ypos = pygame.mouse.get_pos()
                cek = math.sqrt((xvar - xpos)**2 + (yvar - ypos)**2)
                if cek <= 70:
                    waiting = False
                    waiting_screen()
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                xpos, ypos = pygame.mouse.get_pos()
                cek = math.sqrt((xvar - xpos)**2 + (550 - ypos)**2)
                if cek <= 25:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

#Tampilan ketika GameOver
def menuGameOver():
    layar.blit(pygame.transform.scale(image.background,(layar.get_width(),layar.get_height())),(0,0))
    draw_text(layar, "Game Over", 50, WIDTH/2, HEIGHT/8)    

    yvar=350
    xvar=500

    draw_text(layar, "START", 55, WIDTH/2, yvar-25)
    draw_text(layar, f"Your score : {Pilot.score_val}", 20, WIDTH/2, 130)
    draw_text(layar, f"Your level : {level}", 17, WIDTH/2, 210)
    draw_text(layar, "QUIT",30, WIDTH/2, 550) 
    pygame.draw.circle(layar, (RED), (xvar,yvar), 112,5)

    waiting = True
    while waiting:
        fps.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                xpos, ypos = pygame.mouse.get_pos()
                cek = math.sqrt((xvar - xpos)**2 + (yvar - ypos)**2)
                if cek <= 70:
                    Pilot.score_val = 0
                    waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                xpos, ypos = pygame.mouse.get_pos()
                cek = math.sqrt((xvar - xpos)**2 + (550 - ypos)**2)
                if cek <= 25:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


game_over = True
running=True
menu()
updated=False
hp = 0
sound.bgmusic.play(loops=-1)        
while running:
    fps.tick(FPS)
    # waiting screen ketika gameover dan akan memulai game
    if game_over:
        game_over = False
        all_sprites = pygame.sprite.Group()
        hazard = pygame.sprite.Group()
        blasts = pygame.sprite.Group()
        Pilot = Pilot()
        level = 1

        all_sprites.add(Pilot)

        for i in range(4):
            ufo=Ufo()
            all_sprites.add(ufo)
            hazard.add(ufo)
        Pilot.score_val = 0
        # Test alienBoss
        # if Pilot.score_val % 100 == 0:
        #     test = alienBoss(100)
        #     all_sprites.add(test)
        #     hazard.add(test)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
            pygame.quit()
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            if event.key == pygame.K_p:
                updated =False
                pause = not pause
            if event.key==pygame.K_SPACE: # keyboard spasi untuk menembak
                Pilot.shoot()
            elif event.key==pygame.K_1: #cheat menambah skor dengan keyboard angka 1
                Pilot.score_val +=1
            elif event.key==pygame.K_2: #shorcut untuk langsung game over dengan keyboard angka 2
                menuGameOver()  
                game_over = True
            elif event.key==pygame.K_3: #cheat menambah peluru menjadi 2 dengan keyboard angka 3
                Pilot.button=2
                Pilot.shoot()
            elif event.key==pygame.K_4: #cheat menambah skor +25 dengan keyboard angka 4
                Pilot.score_val +=50
            elif event.key==pygame.K_5: #cheat untuk menambah health point +1
                Pilot.life +=1
            elif event.key==pygame.K_6: #cheat menambah speed tembakan
                Pilot.shoot_delay -=250
            if event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()



    all_sprites.update()
    hits=pygame.sprite.groupcollide(hazard,blasts,False,True)


    for hit in hits:
        # cek apakah peluru mengenai lawan
        if isinstance(hit, Ufo):
            sound.exlp2.play()
            hit.kill()
            ufo=Ufo()
            all_sprites.add(ufo)
            hazard.add(ufo)
            Pilot.score_val +=1

            if Pilot.score_val % 30 == 0:
                hp += 50 #setiap skor kelipatan 30 HP alienBoss bertambah 50
                alienBoss = AlienBoss(hp)
                all_sprites.add(alienBoss)
                hazard.add(alienBoss)
                Pilot.buttonup()
                level += 1
                Pilot.life += 1
            elif Pilot.score_val % 10 == 0:
                button=Button()
                all_sprites.add(button)
                hazard.add(button)

        # cek apakah peluru mengenai alienBoss        
        elif isinstance(hit, AlienBoss): 
            sound.exlp2.play()
            hit.hurt()


    # ketika level lebih dari 2 alien meluncur lebih cepat
    if level >= 2:
        Ufo.speedx=random.randrange(-5,1)
        Ufo.speedy=random.randrange(5,10)

    layar.blit(pygame.transform.scale(background,(layar.get_width(),layar.get_height())),(0,0))
    draw_text(layar, f"Level {level}", 20, WIDTH/2, HEIGHT-590)
    all_sprites.draw(layar)
    Pilot.show_score()
    Pilot.show_lifepoints()

    if pause:   
        pause_screen()
        if not updated:
            pygame.display.update()
        updated =True
    if not pause:
        pygame.display.update()

    hits = pygame.sprite.spritecollide(Pilot,hazard,False,pygame.sprite.collide_circle)
    # jika Pilot terkena hit, life akan berkurang
    for hit in hits:
        if isinstance(hit, Ufo):
            sound.expl.play()
            hit.kill()
            ufo=Ufo()
            all_sprites.add(ufo)
            hazard.add(ufo)
            Pilot.life -= 1
        elif isinstance(hit, Blast):
            sound.expl.play()
            hit.kill()
            Pilot.life -= 1
        else:
            hit.kill()
            sound.buttonup.play()
            Pilot.buttonup()

        if Pilot.life < 0:
            game_over = True
            menuGameOver() 


pygame.quit()
