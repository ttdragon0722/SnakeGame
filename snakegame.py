import pygame,sys,random,os
from pygame.math import Vector2

class SNAKE():
    def __init__(self):
        self.body=[Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction=Vector2(0,0)
        self.new_block=False

        self.head_up=pygame.image.load(os.path.join("imgs","head_up.png")).convert_alpha()
        self.head_down=pygame.image.load(os.path.join("imgs","head_down.png")).convert_alpha()
        self.head_right=pygame.image.load(os.path.join("imgs","head_right.png")).convert_alpha()
        self.head_left=pygame.image.load(os.path.join("imgs","head_left.png")).convert_alpha()

        self.tail_up=pygame.image.load(os.path.join("imgs","tail_up.png")).convert_alpha()
        self.tail_down=pygame.image.load(os.path.join("imgs","tail_down.png")).convert_alpha()
        self.tail_right=pygame.image.load(os.path.join("imgs","tail_right.png")).convert_alpha()
        self.tail_left=pygame.image.load(os.path.join("imgs","tail_left.png")).convert_alpha()

        self.body_tr=pygame.image.load(os.path.join("imgs","body_tr.png")).convert_alpha()
        self.body_tl=pygame.image.load(os.path.join("imgs","body_tl.png")).convert_alpha()
        self.body_br=pygame.image.load(os.path.join("imgs","body_br.png")).convert_alpha()
        self.body_bl=pygame.image.load(os.path.join("imgs","body_bl.png")).convert_alpha()

        self.body_vertical=pygame.image.load(os.path.join("imgs","body_vertical.png")).convert_alpha()
        self.body_horizontal=pygame.image.load(os.path.join("imgs","body_horizontal.png")).convert_alpha()

        self.eat_sound=pygame.mixer.Sound(os.path.join("sounds","Sound_crunch.wav"))

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos=int(block.x*cell_size)
            y_pos=int(block.y*cell_size)
            block_rect=pygame.Rect(x_pos,y_pos,cell_size,cell_size)

            if index==0:
                SCREEN.blit(self.head,block_rect)
            elif index == len(self.body)-1:
                SCREEN.blit(self.tail,block_rect)
            else:
                previous_block=self.body[index+1]-block
                next_block=self.body[index-1]-block
                if previous_block.x==next_block.x:
                    SCREEN.blit(self.body_vertical,block_rect)
                elif previous_block.y==next_block.y:
                    SCREEN.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x==-1 and next_block.y==-1 or previous_block.y==-1 and next_block.x==-1:
                        SCREEN.blit(self.body_tl,block_rect)
                    elif previous_block.x==-1 and next_block.y==1 or previous_block.y==1 and next_block.x==-1:
                        SCREEN.blit(self.body_bl,block_rect)
                    elif previous_block.x==1 and next_block.y==-1 or previous_block.y==-1 and next_block.x==1:
                        SCREEN.blit(self.body_tr,block_rect)
                    elif previous_block.x==1 and next_block.y==1 or previous_block.y==1 and next_block.x==1:
                        SCREEN.blit(self.body_br,block_rect)

        
    def update_head_graphics(self):
        head_relation=self.body[1]-self.body[0]
        if head_relation==Vector2(1,0):self.head=self.head_left
        elif head_relation==Vector2(-1,0):self.head=self.head_right
        elif head_relation==Vector2(0,1):self.head=self.head_up
        elif head_relation==Vector2(0,-1):self.head=self.head_down
            
    def update_tail_graphics(self):
        head_relation=self.body[-2]-self.body[-1]
        if head_relation==Vector2(1,0):self.tail=self.tail_left
        elif head_relation==Vector2(-1,0):self.tail=self.tail_right
        elif head_relation==Vector2(0,1):self.tail=self.tail_up
        elif head_relation==Vector2(0,-1):self.tail=self.tail_down
            
        
    def play_sound(self):
        self.eat_sound.play()

    def move_snake(self):
        if self.new_block==True:
            body_copy=self.body[:]
            body_copy.insert(0,body_copy[0]+self.direction)
            self.body=body_copy[:]
            self.new_block=False
        else:
            body_copy=self.body[:-1]
            body_copy.insert(0,body_copy[0]+self.direction)
            self.body=body_copy[:]

    def addblock(self):
        self.new_block=True

    def reset(self):
        self.body=[Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction=Vector2(0,0)

class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect=pygame.Rect(int(self.pos.x*cell_size),int(self.pos.y*cell_size),cell_size,cell_size)
        SCREEN.blit(apple_img,fruit_rect)
        # pygame.draw.rect(SCREEN,RED,fruit_rect)

    def randomize(self):
        self.x=random.randint(0,cell_num-1)
        self.y=random.randint(0,cell_num-1)
        self.pos=Vector2(self.x,self.y)

class MAIN():
    def __init__(self):
        self.snake=SNAKE()
        self.fruit=FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_colloision()
        self.check_fail()

    def draw_elemants(self):
        self.draw_grass()
        self.snake.draw_snake()
        self.fruit.draw_fruit()
        self.draw_score()

    def check_colloision(self):
        if self.fruit.pos==self.snake.body[0]:
            self.fruit.randomize()
            self.snake.addblock()
            self.snake.play_sound()
        for block in self.snake.body[1:]:
            if block ==self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x <cell_num or not 0 <= self.snake.body[0].y <cell_num: 
            self.game_over()

        for block in self.snake.body[1:]:
            if block==self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()

    def draw_grass(self):
        grass_color=(167,209,61)
        for row in range(cell_num):
            if row%2==0:
                for col in range(cell_num):
                    if col%2==0:
                        grass_rect=pygame.Rect(col*cell_size,row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(SCREEN,grass_color,grass_rect)
            else:
                for col in range(cell_num):
                    if col%2!=0:
                        grass_rect=pygame.Rect(col*cell_size,row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(SCREEN,grass_color,grass_rect)
    
    def draw_score(self):
        score_text=str(len(self.snake.body)-3)
        score_surface= game_font.render(score_text,True,(56,74,12))
        score_x=int(cell_size*cell_num-60)
        score_y=int(cell_size*cell_num-40)
        score_rect=score_surface.get_rect(center=(score_x,score_y))
        apple_rect=apple_img.get_rect(midright=(score_rect.left,score_rect.centery))
        bg_rect=pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width+score_rect.width+6,apple_rect.height)

        pygame.draw.rect(SCREEN,(167,209,61),bg_rect)
        SCREEN.blit(score_surface,score_rect)
        SCREEN.blit(apple_img,apple_rect)
        pygame.draw.rect(SCREEN,(56,74,12),bg_rect,2)
        

BLACK=(0,0,0)
GREEN=(175,215,70)
RED=(255,0,0)

FPS=60
clock=pygame.time.Clock()

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_size=40
cell_num=20
SCREEN=pygame.display.set_mode((cell_size*cell_num,cell_size*cell_num))
font=os.path.join("fonts","Pixel.ttf")
game_font=pygame.font.Font(font,30)


apple_img=pygame.image.load(os.path.join("imgs","apple.png")).convert_alpha()

SCREEN_UPDATE=pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

main_game=MAIN()
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            main_game.game_over()
            pygame.quit()
            sys.exit()
        if event.type==SCREEN_UPDATE:
            main_game.update()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                if main_game.snake.direction.y!=1:
                    main_game.snake.direction=Vector2(0,-1)
            if event.key==pygame.K_RIGHT:
                if main_game.snake.direction.x!=-1:
                    main_game.snake.direction=Vector2(1,0)
            if event.key==pygame.K_LEFT:
                if main_game.snake.direction.x!=1:
                    main_game.snake.direction=Vector2(-1,0)
            if event.key==pygame.K_DOWN:
                if main_game.snake.direction.y!=-1:
                    main_game.snake.direction=Vector2(0,1)
    
    SCREEN.fill(GREEN)
    main_game.draw_elemants()
    pygame.display.update()