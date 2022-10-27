import pygame
import random

#初始化

FPS=60
cell_size=40
cell_num=20
WIDTH=cell_size*cell_num
HEIGHT=cell_size*cell_num

#顏色
BLACK=(0,0,0)
GREEN=(0,255,0)
WHITE=(0,0,0)
GRAY=(192,192,192)
RED=(255,0,0)


pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Snake Game")
clock =pygame.time.Clock()

#載入圖片

#載入音樂

#函式區
def new_point():
    p=Point()
    all_sprites.add(p)
    points.add(p)


#SPRITES

class Snake(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((cell_size,cell_size))
        self.image.fill(GREEN)
        self.rect=self.image.get_rect()
        self.x=0
        self.y=19
        self.rect.x=self.x*cell_size
        self.rect.y=self.y*cell_size
        
        # self.speed=5
        self.moveMode="right"

    def update(self):
        #持續移動
        if self.moveMode=="up":
            if self.y!=0:
                self.y-=1
            elif self.y==0:
                self.y=cell_num-1
            self.rect.y=self.y*cell_size
        if self.moveMode=="down":
            if self.y!=cell_num-1:
                self.y+=1
            elif self.y ==cell_num-1:
                self.y=0
            self.rect.y=self.y*cell_size
        if self.moveMode=="right":
            if self.x!=cell_num-1:
                self.x+=1
            elif self.x ==cell_num-1:
                self.x=0
            self.rect.x=self.x*cell_size
        if self.moveMode=="left":
            if self.x!=0:
                self.x-=1
            elif self.x==0:
                self.x=cell_num-1
            self.rect.x=self.x*cell_size
        print(str(self.x)+","+str(self.y))


        #偵測輸入
        key_pressed=pygame.key.get_pressed()
        if key_pressed[pygame.K_UP] and self.moveMode!="down":
            self.moveMode="up"

        if key_pressed[pygame.K_DOWN] and self.moveMode!="up":
            self.moveMode="down"
            
        if key_pressed[pygame.K_RIGHT] and self.moveMode!="left":
            self.moveMode="right"
        
        if key_pressed[pygame.K_LEFT] and self.moveMode!="right":
            self.moveMode="left"
        
        #偵測邊界
        # if self.x==cell_num:
        #     self.x=0
        # if self.y<0:
        #     self.y=cell_num
        # if self.x<0:
        #     self.x=cell_num
        # if self.y==cell_num:
        #     self.y=0
        
class Point(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((cell_size,cell_size))
        self.image.fill(RED)
        self.rect=self.image.get_rect()
        self.x=random.randint(0,cell_num-1)
        self.y=random.randint(0,cell_num-1)
        self.rect.x=self.x*cell_size
        self.rect.y=self.y*cell_size


        #random.randint(1,cell_num)
        

#新增至遊戲
all_sprites=pygame.sprite.Group()
points=pygame.sprite.Group()
players=pygame.sprite.Group()

player=Snake()
point=Point()

all_sprites.add(player)
players.add(player)
all_sprites.add(point)
points.add(point)


#遊戲循環

running=True

while running:

    clock.tick(FPS)
    #取得輸入

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    #更新遊戲
    hits=pygame.sprite.groupcollide(players,points,False,True)
    for hit in hits:
        new_point()
        
    
    all_sprites.update()
    

    #畫上去

    screen.fill(BLACK)
    all_sprites.draw(screen)    
    
    pygame.display.update()

pygame.quit()