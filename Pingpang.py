import pygame,sys,random
from pygame.locals import*
pygame.init()
clock = pygame.time.Clock()
screen_width =1000
screen_height = 660
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Ping-Pang Ball")
Black=(0,0,0)
# Red=(255,0,0)
# Green = (0,255,0)
# Blue=(0,0,255)
# DISPLAYSURF.fill(Black)
# pygame.draw.line(DISPLAYSURF,Blue,(250,60),(350,60),4)
# pygame.draw.circle(DISPLAYSURF,Green,(300,80),20,4)

def ball_animation():
    global ball_speed_x,ball_speed_y,player_score,opponent_score,score_time
     #Move
    ball.x+=ball_speed_x
    ball.y+=ball_speed_y
    #Bound(change direction by multy -1)&& (consider the colission(condition) outside of screen--> change direction )
    if ball.top<=0 or ball.bottom>=screen_height:
        ball_speed_y*=-1
    if ball.left<=0:
        # ball_restart()
        score_time=pygame.time.get_ticks()
        player_score+=1
    if ball.right>=screen_width:
        # ball_restart()
        score_time=pygame.time.get_ticks()
        opponent_score+=1
    #Colission for player and opponent
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x*=-1
def ball_restart():
    global score_time
    ball.center=(screen_width/2-8,screen_height/2-3)
    current_time=pygame.time.get_ticks()
    #Within the timmer, the ball stays in the center and does not move
    if current_time-score_time<=700:
        number_three=game_font.render("3",False,light_grey)
        screen.blit(number_three,(495,360))
    if 700<current_time-score_time<=1400:
        number_two=game_font.render("2",False,light_grey)
        screen.blit(number_two,(495,360))
    if 1400<current_time-score_time<700:
        number_three=game_font.render("3",False,light_grey) 
        screen.blit(number_three,(495,360))
    if  current_time-score_time<2000:
        ball_speed_x=0
        ball_speed_y=0
    #After timmer ends, the ball randomly goes to any direction
    else:
        ball_speed_x=10*random.choice((-1,1))
        ball_speed_y=10*random.choice((-1,1))
        score_time=None
#In order not move the player out of screen, limie the maxmum and minimum position
def player_moveLimit():
    player.y+=player_speed
    if player.top<=0:
        player.top=0
    if player.bottom>=screen_height:
        player.bottom=screen_height    
#creat AI movement
def opponent_movement():
    #if opponent rectangle above the ball--->move down--->increase y
    if opponent.top<ball.y:
        opponent.top+=opponent_speed
    #if opponent rectangle below the ball--->move up--->decrease y
    if opponent.bottom>ball.y:
        opponent.bottom-=opponent_speed
    if opponent.top<=0:
        opponent.top=0
    if opponent.bottom>=screen_height:
        opponent.bottom=screen_height       
#Game rectangles
ball =pygame.Rect(screen_width/2-15,screen_height/2-15,30,30)
player= pygame.Rect(screen_width-20,screen_height/2-70,10,100)
opponent= pygame.Rect(10,screen_height/2-70,10,100)
#Color
bg_color=pygame.Color('grey12')
light_grey=(200,200,200)
#Speed Variable
ball_speed_x=7*random.choice((-1,1))
ball_speed_y=7*random.choice((-1,1))
player_speed=0
opponent_speed=7
#Text Variable
player_score=0
opponent_score=0
game_font = pygame.font.Font("freesansbold.ttf",32)
#Timmer
score_time=None

while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        #check whether user has clicked any keyboard
        if event.type == pygame.KEYDOWN:
        #check whether user has clicked downarrow
            if event.key == pygame.K_DOWN:
                player_speed+=7
            if event.key == pygame.K_UP:
                player_speed-=7
        #So far you can only press up or down key once and it will in out of bound
        #Check if we release the key
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed-=7
            if event.key == pygame.K_UP:
                player_speed+=7

    ball_animation()
    player_moveLimit()
    opponent_movement()
    # opponent_movement()
    #Drawing
    screen.fill(bg_color)
    pygame.draw.rect(screen,light_grey,player)
    pygame.draw.rect(screen,light_grey,opponent)
    pygame.draw.ellipse(screen,light_grey,ball)
    pygame.draw.aaline(screen,light_grey,(screen_width/2,0),(screen_width/2,screen_height))

    if score_time:
        ball_restart()
    
    player_text=game_font.render(f"{player_score}",False,light_grey)
    screen.blit(player_text,(520,300))
    opponent_text=game_font.render(f"{opponent_score}",False,light_grey)
    screen.blit(opponent_text,(467,300))
   
   
    pygame.display.flip()
    clock.tick(60)