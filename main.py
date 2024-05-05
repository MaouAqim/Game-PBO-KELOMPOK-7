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

pause = False

def pause_screen():
    draw_text(layar, "Pause", 50, WIDTH / 2, HEIGHT / 2)
    draw_text(layar, "Press P to Resume", 30, WIDTH / 2, HEIGHT / 2 + 50)
    # pygame.display.flip()

#Class Player(Class Child)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(image.player,(145,115))
        self.rect=self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom=HEIGHT - 20
        self.speedx = 8
        self.score_val = 0
        self.life = 5
        self.button = 1
        self.button_time = pygame.time.get_ticks()
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 250

    #artibuted movement
    def update(self):

        if self.button >= 2 and pygame.time.get_ticks() - self.button_time > 5000:
            self.button -= 1
            self.button_time = pygame.time.get_ticks()

        key_pressed = pygame.key.get_pressed()
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
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top  = 0

    def buttonup(self):
        self.button += 1
        self.button_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.button == 1:
                bullet = Bullet(pygame.Vector2(self.rect.centerx,self.rect.top))
                all_sprites.add(bullet)
                bullets.add(bullet)
                sound.missile.play()
            elif self.button >= 2:
                bullet1 = Bullet(pygame.Vector2(self.rect.centerx-20,self.rect.top))
                all_sprites.add(bullet1)
                bullets.add(bullet1)
                bullet2 = Bullet(pygame.Vector2(self.rect.centerx+20,self.rect.top))
                all_sprites.add(bullet2)
                bullets.add(bullet2)
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
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT or self.rect.left>WIDTH or self.rect.right<0:
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

#Class Bullet(Class Child)
class Bullet(pygame.sprite.Sprite):
    def __init__(self,position:pygame.Vector2,angle:float=-90):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.rotate(pygame.transform.scale(image.bullet,(25,35)),-angle+180+90)
        self.rect=self.image.get_rect()
        self.rect.midbottom=position
        speedy = 10
        self.velocity = pygame.math.Vector2(math.cos(math.radians(angle))*speedy,math.sin(math.radians(angle))*speedy)

    def update(self):
        self.rect.midbottom += self.velocity
        if self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
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
        self.alt = not self.alt
        if self.alt:
            bullet = Bullet(pygame.Vector2(self.rect.centerx-30,self.rect.bottom), -self.angle)
        else :
            bullet = Bullet(pygame.Vector2(self.rect.centerx+30,self.rect.bottom), -self.angle)
        all_sprites.add(bullet)
        hazard.add(bullet)


    def update(self):
        self.rect.y += self.move_in.y
        if self.move_in.y > 0:
            self.move_in.y *= 0.95

        self.tick += 1

        p_center = player.rect.center
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
    layar.blit(pygame.transform.scale(image.background,(1000,600)),(0,0))
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
    layar.blit(pygame.transform.scale(image.background,(1000,600)),(0,0))
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
    layar.blit(pygame.transform.scale(image.background,(1000,600)),(0,0))
    draw_text(layar, "Game Over", 50, WIDTH/2, HEIGHT/8)    

    yvar=350
    xvar=500

    draw_text(layar, "START", 55, WIDTH/2, yvar-25)
    draw_text(layar, f"Your score : {player.score_val}", 20, WIDTH/2, 130)
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
                    player.score_val = 0
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
hp = 0
sound.bgmusic.play(loops=-1)        
while running:
    fps.tick(FPS)
    # waiting screen ketika gameover dan akan memulai game
    if game_over:
        game_over = False
        all_sprites = pygame.sprite.Group()
        hazard = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        level = 1

        all_sprites.add(player)

        for i in range(4):
            ufo=Ufo()
            all_sprites.add(ufo)
            hazard.add(ufo)
        player.score_val = 0
        # Test alienBoss
        # if player.score_val % 100 == 0:
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
                pause = not pause
            if event.key==pygame.K_SPACE: # keyboard spasi untuk menembak
                player.shoot()
            elif event.key==pygame.K_1: #cheat menambah skor dengan keyboard angka 1
                player.score_val +=1
            elif event.key==pygame.K_2: #shorcut untuk langsung game over dengan keyboard angka 2
                menuGameOver()  
                game_over = True
            elif event.key==pygame.K_3: #cheat menambah peluru menjadi 2 dengan keyboard angka 3
                player.button=2
                player.shoot()
            elif event.key==pygame.K_4: #cheat menambah skor +25 dengan keyboard angka 4
                player.score_val +=50
            elif event.key==pygame.K_5: #cheat untuk menambah health point +1
                player.life +=1
            elif event.key==pygame.K_6: #cheat menambah speed tembakan
                player.shoot_delay -=250



    all_sprites.update()
    hits=pygame.sprite.groupcollide(hazard,bullets,False,True)


    for hit in hits:
        # cek apakah peluru mengenai lawan
        if isinstance(hit, Ufo):
            sound.exlp2.play()
            hit.kill()
            ufo=Ufo()
            all_sprites.add(ufo)
            hazard.add(ufo)
            player.score_val +=1

            if player.score_val % 30 == 0:
                hp += 50 #setiap skor kelipatan 30 HP alienBoss bertambah 50
                alienBoss = AlienBoss(hp)
                all_sprites.add(alienBoss)
                hazard.add(alienBoss)
                player.buttonup()
                level += 1
                player.life += 1
            elif player.score_val % 10 == 0:
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

    layar.blit(pygame.transform.scale(image.background,(1000,600)),(0,0))
    draw_text(layar, f"Level {level}", 20, WIDTH/2, HEIGHT-590)
    all_sprites.draw(layar)
    player.show_score()
    player.show_lifepoints()

    if pause:
        pause_screen()
    pygame.display.update()

    hits = pygame.sprite.spritecollide(player,hazard,False,pygame.sprite.collide_circle)
    # jika player terkena hit, life akan berkurang
    for hit in hits:
        if isinstance(hit, Ufo):
            sound.expl.play()
            hit.kill()
            ufo=Ufo()
            all_sprites.add(ufo)
            hazard.add(ufo)
            player.life -= 1
        elif isinstance(hit, Bullet):
            sound.expl.play()
            hit.kill()
            player.life -= 1
        else:
            hit.kill()
            sound.buttonup.play()
            player.buttonup()

        if player.life < 0:
            game_over = True
            menuGameOver() 


pygame.quit()
