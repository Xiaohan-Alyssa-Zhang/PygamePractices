import pygame, sys,random
 
#Manage floor movement
def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,400))
    screen.blit(floor_surface,(floor_x_pos+400,400))

#Pipe category
def creat_pip():
    random_pip_pos=random.choice(pipe_height)
    bottom_pipe= pipe_surface.get_rect(midtop = (370,random_pip_pos))
    top_pipe= pipe_surface.get_rect(midbottom = (370,random_pip_pos-200))
    return bottom_pipe, top_pipe
#move pipe left-forward
def move_pipes(pipes):
    for i in pipes:
        i.centerx-=5
    return pipes
def draw_pipes(pipes):
    for i in pipes:
        if i.bottom>=300:
            screen.blit(pipe_surface,i)
        else:
            # Use transform.flip to reverse the pipe image
            flip_pipe=pygame.transform.flip(pipe_surface,False, True)
            screen.blit(flip_pipe,i)
#Check whether the bird rectangle has collision with pipe rectangle
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top<=-10 or bird_rect.bottom>=500:
        return False
    return True
#Rotation
def rotated_bird(bird):
    new_bird=pygame.transform.rotozoom(bird,-bird_movement*6,1)
    return new_bird
#Score Display on screen
def score_display(game_situation):
    if game_situation=="active":
        score_surface=game_font.render(str(int(score)),True,(255,255,255))
        score_rect= score_surface.get_rect(center=(200,120))
        screen.blit(score_surface,score_rect)
    if game_situation=="over":
        score_surface=game_font.render(f"Score:{int(score)}",True,(255,255,255))
        score_rect= score_surface.get_rect(center=(200,120))
        screen.blit(score_surface,score_rect)

        high_score_surface=game_font.render(f"High Score:{int(high_score)}",True,(255,255,255))
        high_score_rect= high_score_surface.get_rect(center=(200,145))
        screen.blit(high_score_surface,high_score_rect)
#deal with high score
def update_score(score,high_score):
    if score>high_score:
        high_score=score
    return high_score
    

pygame.init()
screen=pygame.display.set_mode((400,500))
clock= pygame.time.Clock()
game_font=pygame.font.Font("freesansbold.ttf",26)
# def bird_animation():
#     new_bird=bird_frames[bird_index]
#     new_bird_rect=new_bird.get_rect(center = (50,200))
#     return new_bird,new_bird_rect

#Variables
gravity=0.25
bird_movement=0
game_active=True
score=0
high_score=0
#Add background page //Convert() helps run faster and easy in pygame
bg_surface=pygame.image.load('image_audio/background-day.png').convert()
bg_surface=pygame.transform.scale(bg_surface,(500,500))

#Floor image control the size
floor_surface=pygame.image.load("image_audio/base.png").convert()
floor_surface=pygame.transform.scale(floor_surface,(500,200))
floor_x_pos=0

# Bird image center is the bird's start point 
bird_surface=pygame.image.load("image_audio/bluebird-midflap.png").convert_alpha()
bird_surface=pygame.transform.scale(bird_surface,(30,30))
bird_rect= bird_surface.get_rect(center = (50,200))


# bird_downflap = pygame.transform.scale(pygame.image.load('image_audio/bluebird-downflap.png'),(30,30)).convert_alpha()
# bird_midflap = pygame.transform.scale(pygame.image.load('image_audio/bluebird-midflap.png'),(30,30)).convert_alpha()
# bird_upflap = pygame.transform.scale(pygame.image.load('image_audio/bluebird-upflap.png'),(30,30)).convert_alpha()
# bird_frames = [bird_downflap,bird_midflap,bird_upflap]
# bird_index = 0
# bird_surface = bird_frames[bird_index]
# bird_rect = bird_surface.get_rect(center = (50,200))

# BIRDFLAP = pygame.USEREVENT + 1
# pygame.time.set_timer(BIRDFLAP,800)


#pipe surface
pipe_surface = pygame.image.load("image_audio/pipe-green.png").convert()
pipe_surface=pygame.transform.scale(pipe_surface,(60,200))
pipe_list=[]
#Creat pipe by timer loop/ 1.2s 
SPAWNPIPE=pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,800)

pipe_height=[360,300,330,260]

game_over_surface=pygame.image.load("image_audio/message.png").convert_alpha()
game_over_surface=pygame.transform.scale(game_over_surface,(330,370))
game_over_rect=game_over_surface.get_rect(center=(200,200))

while True: 
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        #Check whether user has pressed any keyboard
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                bird_movement=0
                bird_movement-=7
            if event.key==pygame.K_SPACE and game_active==False:
                game_active=True
                pipe_list.clear()
                bird_rect.center=(50,200)
                bird_movement=0
                score=0
        # Add new pip to the pip_list
        if event.type==SPAWNPIPE:
            #if there is only one pipe use append, otherwise extend tuple to the list
            #pipe_list.append(creat_pip())
            pipe_list.extend(creat_pip())
        # if event.type==BIRDFLAP:
        #     if bird_index<2:
        #         bird_index+=1
        #     else:
        #         bird_index=0
        #     bird_surface,bird_rect=bird_animation()
              
    #show background image on pygame
    screen.blit(bg_surface,(0,0))
    if game_active:
        #change the movement up and down using gravity
        bird_movement+=gravity
        bird_rect.centery+=bird_movement
        #show bird image on pygame
        screen.blit(rotated_bird(bird_surface),bird_rect)
        game_active=check_collision(pipe_list)
        #Draw Pipes on screen 
        pipe_list=move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score+=0.01
        score_display("active")
    else:
        screen.blit(game_over_surface,(30,20))
        high_score=update_score(score,high_score)
        score_display("over")
        
        
    floor_x_pos-=1
    draw_floor()
    
    #if floor run to far on the left, resign the x to 0
    if floor_x_pos<=-400:
        floor_x_pos=0
        
    pygame.display.update()
    clock.tick(120)