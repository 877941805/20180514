# 定义方向
LEFT = [0,-1]
RIGHT = [0,1]
UP = [-1,0]
DOWN = [1,0]
DIRECTION = [LEFT,RIGHT,UP,DOWN]
score1=0
score2=0



# 机器放置炸弹后躲开的20种路径（8种走2步，12种走3步）
WALKOUTBOMB2 = []
WALKOUTBOMB3 = []
for i in DIRECTION:
    for j in DIRECTION:
        if (j != i) and (j != [-i[0],-i[1]]):
            WALKOUTBOMB2.append([i,j])
            WALKOUTBOMB3.append([i,i,j])       
    WALKOUTBOMB3.append([i,i,i])
WALKOUTBOMB = WALKOUTBOMB2 + WALKOUTBOMB3

WhetherBombed=[False,False]
# PLAYERONE = [25,0]
PLAYERONE = [10,9]
PLAYERTWO = [10,6]

# P(Machine Places Bomb) per movement
BOMBPRO = 0.9

# Bomb Pool
BOMBSTACK = []  # first in first out

# Machine Walk Time Lag
MACHINEMOVETIMELAG = 0.5
# new

# Machine Run Away Speed (Time Lag) after placing bomb
MACHINERUNAWAY = 0.08

# MACHINERUNAWAY*3 < MACHINEMOVETIMELAG

# Steps of Random Walk Tried by Machine Escaping Dilemma
SURVIVALTRAIL = 100
# Time Lag of Random Walk Tried by Machine Escaping Dilemma
SURVIVALSPEED = 0.01

# SURVIVALSPEED <= 1/SURVIVALTRAIL

# P(suicide) is consider dangerous under random walk
#SUICIDETHRESHOLD = 0.1
SUICIDETHRESHOLD = 0

# Machine Simulation Steps
SLSTEP = 7
SLTIME = 100

# Machine in urgent move or not (state variable)
INURGENTMOVE = False

# Machine in survival mode or not (state variable)
INSURVIVAL = False

import random
import sys
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'
import pygame
from sys import exit
#import threading
import _thread
import time


from pygame.locals import *

# -----------------------------------------------------------------------------
# STATE 1: Game Preparation
# -----------------------------------------------------------------------------

# Load landform
import excel
landform = excel.load_data(file_name = 'script1.csv')
playerOneWin_landform = excel.load_data(file_name = 'playerOneWin.csv')
playerTwoWin_landform = excel.load_data(file_name = 'playerTwoWin.csv')
#playerOneWin_landform = excel.load_data(file_name = 'playerOneWin.csv')
#playerTwoWin_landform = excel.load_data(file_name = 'playerTwoWin.csv')
#draw_landform = excel.load_data(file_name = 'draw.csv')

# Initialize 美工 game setting
cell_size=30
windows_width=cell_size*40
matrix_width = cell_size*30
windows_height = cell_size*26
matrix_height=cell_size*26 #游戏窗口的大小

map_width = int(matrix_width / cell_size)
map_height = int(matrix_height / cell_size)

# 颜色定义
white = (255, 255, 255)
black = (0, 0, 0)
gray = (230, 230, 230)
dark_gray = (40, 40, 40)
DARKGreen = (0, 155, 0)
Green = (0, 255, 0)
Red = (255, 0, 0)
blue = (0, 0, 255)
dark_blue =(0,0,139)
orange = (250,140,53)

BG_COLOR = black #游戏背景颜色

bg_color=BG_COLOR
caption_color=gray
word_color=Red
buttoncolor=black


#初始化screen
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((windows_width, windows_height))
skinfilename = os.path.join('character.png')
skin = pygame.image.load(skinfilename)    
skin = skin.convert()


cell_size=int(skin.get_width()/ 4)
 # Create a pygame window   
screen.fill(BG_COLOR)
pygame.display.set_caption("Crazy Arcade")
clock = pygame.time.Clock()
font = pygame.font.Font('font.ttf', 30)

#def game_intro():
#    window=tk.Tk()
#    window.title('Crazy Arcade')
#    back=tk.Frame(master=window,width=windows_width,height=windows_height,bg=BG_COLOR)
#    back.pack()
#    easy=tk.Button(window,text='Easy',bg=Red,command=lambda:running_game()).pack()
pygame.key.get_focused()
def game_intro():
    global landform
#    global font
    intro=True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                pygame.quit()  
                quit()
        #screen = pygame.display.set_mode((windows_width, windows_height))
        screen.fill(bg_color)
        font = pygame.font.Font('font.ttf', 120)
        cap_font=font
        cap_text = cap_font.render('CRAZY ARCADE', True, gray,bg_color)
        text_rect = cap_text.get_rect()
        text_rect.topleft =(12*cell_size,2*cell_size)
        screen.blit(cap_text, text_rect)
        font = pygame.font.Font('font.ttf', 50)
        word_font=font
        word_text = word_font.render('Choose the Level', True, word_color,bg_color)
        word_rect = word_text.get_rect()
        word_rect.topleft =(16*cell_size,10*cell_size)
        screen.blit(word_text, word_rect)
        
        button('EASY', 150,450 ,220, 100, gray, Red,running_game)  
        button("NORMAL",500, 450, 220, 100, gray,Red,running_game) 
        button("HARD",850, 450, 220, 100, gray,Red,running_game)
        pygame.display.update()
          
       
       
                
def button (msg, x, y, w, h, ic, ac,action=None): 
        global SLSTEP
        global SLTIME
#        global font
        mouse =pygame.mouse.get_pos()  
        click = pygame.mouse.get_pressed()  
        (click)  

        if x + w > mouse[0] > x and y + h > mouse[1] > y:  
            pygame.draw.rect(screen, ac, (x,y,w,h))  
            if click[0] == 1 and action!=None:
                if msg=='Easy':
                    SLSTEP=3
                    SLTIME=50
                    action()
                elif msg=='Normal':
                    SLSTEP=5
                    SLTIME=100
                    action()
                    
                elif msg=='Hard':
                    SLSTEP=7
                    SLTIME=150
                    action()
                else:
                    action()
                
##                if action == "play":  
##                    action()  
##                if action == "quit":  
##                    pygame.quit()  
##                    quit()  
        else:  
            pygame.draw.rect(screen, ic, (x,y,w,h))
        
        buttonfont =pygame.font.Font('font.ttf', 60)
        textSurface = buttonfont.render(msg, True, buttoncolor)  
        textRect =textSurface.get_rect()  
        textRect.center = ( (x+(w/2)), (y+(h/2)))  
        screen.blit(textSurface, textRect) 
        return SLSTEP,SLTIME
            
        

path_color=(205,112,84)
barrier_color=(238,64,0)
wall_color=(30,30,30)
grid_color=(255,245,238)
bomb_color=white

bomb_zone_col=orange
playerOneCol = Green
playerTwoCol = blue



   











def draw_block(screen):
    global landform
    for i in range(0,len(landform)):
        for j in range(0,len(landform[i])):
            if landform[i][j] == '0':
                #需要知道cell_size (小正方形的边长)
               Rect= pygame.Rect(j*cell_size, i*cell_size, cell_size, cell_size) 
               pygame.draw.rect(screen, black, Rect)
             #using the cartoon image to draw the land form
             #screen.blit(converted image,the place we want to draw on the screen, the position of the target iamge in the whole picture)
            elif landform[i][j] == '1':

                screen.blit(skin, (j*cell_size, i*cell_size), (3*cell_size,0,cell_size,cell_size)) 
            elif landform[i][j] == '2':
                screen.blit(skin, (j*cell_size, i*cell_size), (0,2*cell_size,cell_size,cell_size))
                
            elif landform[i][j] == '3':
                Rect= pygame.Rect(j*cell_size, i*cell_size, cell_size, cell_size) 
                pygame.draw.rect(screen, black, Rect)
                screen.blit(skin, (j*cell_size, i*cell_size), (2*cell_size,3*cell_size,cell_size,cell_size))
               # pygame.draw.circle(screen,bomb_color,(int((j)*cell_size+cell_size/2),int((i)*cell_size+cell_size/2)),int(cell_size/2),0)
            elif landform[i][j] == '-1':
                screen.blit(skin, (j*cell_size, i*cell_size), (3*cell_size,2*cell_size,cell_size,cell_size))
    draw_grid(screen)
def draw_point(screen,index):
    global landform
    i = index[0]
    j = index[1]
    if landform[i][j] == '0':
        Rect= pygame.Rect(j*cell_size, i*cell_size, cell_size, cell_size) 
        pygame.draw.rect(screen, black, Rect)
    elif landform[i][j] == '1':
        screen.blit(skin, (j*cell_size, i*cell_size), (3*cell_size,0,cell_size,cell_size)) 
    elif landform[i][j] == '2':
        screen.blit(skin, (j*cell_size, i*cell_size), (0,2*cell_size,cell_size,cell_size))
    elif landform[i][j] == '3':
        Rect= pygame.Rect(j*cell_size, i*cell_size, cell_size, cell_size) 
        pygame.draw.rect(screen, black, Rect)
        screen.blit(skin, (j*cell_size, i*cell_size), (2*cell_size,3*cell_size,cell_size,cell_size))
    elif landform[i][j] == '-1':
        screen.blit(skin, (j*cell_size, i*cell_size), (3*cell_size,2*cell_size,cell_size,cell_size))
    draw_grid(screen)
    
    

def draw_player(screen):
#    Rect= pygame.Rect(PLAYERONE[1]*cell_size, PLAYERONE[0]*cell_size, cell_size, cell_size)
#    pygame.draw.rect(screen, playerOneCol, Rect)
    screen.blit(skin, (PLAYERONE[1]*cell_size, PLAYERONE[0]*cell_size), (cell_size,0,cell_size,cell_size))
    screen.blit(skin, (PLAYERTWO[1]*cell_size, PLAYERTWO[0]*cell_size), (0,0,cell_size,cell_size))
    draw_grid(screen)
    if PLAYERONE[1]==PLAYERTWO[1] and PLAYERONE[0]==PLAYERTWO[0]:
        screen.blit(skin, (PLAYERONE[1]*cell_size, PLAYERONE[0]*cell_size), (cell_size,0,cell_size,cell_size))
    # 若两个player重合的颜色设置
    pass
        
#画网格
def draw_grid(screen):
    for x in range(0, cell_size*31, cell_size):  # draw 竖直 lines
        pygame.draw.line(screen, dark_gray, (x, 0), (x, windows_height))
    for y in range(0,cell_size*30, cell_size):  # draw 水平 lines
        pygame.draw.line(screen, dark_gray, (0, y), (cell_size*30, y))
def draw_score(screen):
    
    Rect=pygame.Rect(int(30*cell_size),0,int(16*cell_size),int(40*cell_size))
    pygame.draw.rect(screen, black, Rect)
    pygame.display.update()
    
    
    score_font = pygame.font.Font('font.ttf', 36)
    score_text = score_font.render('''Your_1 Score:%s'''%score1, True, Red,BG_COLOR)
    text_rect = score_text.get_rect()
    text_rect.topleft =(matrix_width,25)
    screen.blit(score_text, text_rect)
    pygame.display.update()
    
    score_font = pygame.font.Font('font.ttf', 36)
    score_text = score_font.render('''Machine_2 Score:%s'''%score2, True, Red,BG_COLOR)
    text_rect = score_text.get_rect()
    text_rect.topleft =(matrix_width,18*25)
    screen.blit(score_text, text_rect)
    pygame.display.update()
    
   



# -----------------------------------------------------------------------------
# STATE 2: GAMING
# -----------------------------------------------------------------------------

#运行函数
def game():
    pygame.init() # 模块初始化
    #pygame.font.init(）
    pygame.display.set_caption("Crazy Arcade") #设置标题
    font = pygame.font.Font('font.ttf', 30)
    game_intro()
    
    while True:
        try:
            running_game()
        #show_gameover_info(screen)
        except:
            break
    terminate() 
  
# -----------------------------------------------------------------------------        
#游戏运行主体
def running_game():
    global landform 
    global SLTIME
    global SLSTEP
    
    
    # test
    pygame.event.get()
    pygame.key.get_focused()
    
    # backgound music
    pygame.mixer.init()
    pygame.mixer.music.load('bgm.mp3')
    pygame.mixer.music.play()
    # bgm volume
    pygame.mixer.music.set_volume(0.5)
    
    # Draw landform
    draw_block(screen)
    #draw_grid(screen) # draw_grid放在放在draw_block里面call了
    pygame.display.update()
    
    # Draw players
    draw_player(screen)
    pygame.display.update()
    
    draw_score(screen)
    pygame.display.update()
    
   
    screen.fill(black)
    
    

    #food = get_random_location() #实物随机位置(可以之后做补血包之类的)
    _thread.start_new_thread(MachineMove,(screen,MACHINEMOVETIMELAG))
    draw_score(screen)
    pygame.display.update()
    draw_block(screen)
    pygame.display.update()
    draw_player(screen)
    pygame.display.update()
    while True:
       

        try:
            for event in pygame.event.get():            
                #if event.type == QUIT:
                if event.type == pygame.QUIT:
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_LEFT:
                        # 判断左边是否movable
                        # 如果movable就move (update playerOneLoc和游戏画面)
                        # 以下4个方向同理
                        if legitMove([PLAYERONE[0],PLAYERONE[1]-1]):
                            draw_point(screen,PLAYERONE)
                            PLAYERONE[1] -= 1
                            draw_player(screen)
                            pygame.display.update()
                            if walkIntoBomb(PLAYERONE):
                                bomb_sound = pygame.mixer.Sound('die.wav')
                                bomb_sound.play()
                                displayWinner(screen,2)
    
                    elif event.key == K_RIGHT:
                        if legitMove([PLAYERONE[0],PLAYERONE[1]+1]):
                            draw_point(screen,PLAYERONE)
                            PLAYERONE[1] += 1
                            draw_player(screen)
                            pygame.display.update()
                            if walkIntoBomb(PLAYERONE):
                                bomb_sound = pygame.mixer.Sound('die.wav')
                                bomb_sound.play()
                                displayWinner(screen,2)
    
                    elif event.key == K_UP:
                        if legitMove([PLAYERONE[0]-1,PLAYERONE[1]]):
                            draw_point(screen,PLAYERONE)
                            PLAYERONE[0] -= 1
                            draw_player(screen)
                            pygame.display.update()
                            if walkIntoBomb(PLAYERONE):
                                bomb_sound = pygame.mixer.Sound('die.wav')
                                bomb_sound.play()
                                displayWinner(screen,1)
    
                    elif event.key == K_DOWN:
                        if legitMove([PLAYERONE[0]+1,PLAYERONE[1]]):
                            draw_point(screen,PLAYERONE)
                            PLAYERONE[0] += 1
                            draw_player(screen)
                            pygame.display.update()
                            if walkIntoBomb(PLAYERONE):
                                bomb_sound = pygame.mixer.Sound('die.wav')
                                bomb_sound.play()
                                displayWinner(screen,2)
    
                    elif event.key == K_SPACE:
                        # 放置炸弹
                        landform[PLAYERONE[0]][PLAYERONE[1]] = '3'
                        draw_point(screen,PLAYERONE)
                        pygame.display.update()
                        
                        # updata BombStack
                        BOMBSTACK.append(PLAYERONE)
                        
                        # sound effect
                        bomb_sound = pygame.mixer.Sound('throw_bomb.wav')
                        bomb_sound.play()
                        # bgm volume
                        #pygame.mixer.music.set_volume(0.5)
    
                        bombIndex = PLAYERONE[:]
                        _thread.start_new_thread(userexplode,(screen,bombIndex,3))
                        _thread.start_new_thread(release,(screen,bombIndex,4))
                        
                  
                        # 暂时update炸弹位置为bomb placed(wall属性)
                        # schedule一个timer
                        # 定时5s后爆炸（爆炸的时候：找周围可爆炸区域+爆炸区域变色+音效
                            # +判断是否有人被炸到了）
                            # 若发现有人被炸到了，直接记录胜利者，结束游戏
                        # 定时6s后爆炸完成（改变颜色-根据landform+update被炸到的地方为blank-
                        # landform、游戏界面都变）
        except:
            break 
    
 
    
    terminate()

# -----------------------------------------------------------------------------
def inRegion(index):
    return (index[0]>=0) and (index[0]<=25) and (index[1]>=0) and (index[1]<=29)
# -----------------------------------------------------------------------------
# 判断这一步是否可走（在窗体内+不是barrier/wall/bomb placed）
# 不判断是否走进dangerzone
def legitMove(index):
    return inRegion(index) and (int(landform[index[0]][index[1]]) <= 0)
# -----------------------------------------------------------------------------
# 判断player是否走入爆炸区
def walkIntoBomb(index):
    return landform[index[0]][index[1]] == '-1'
# -----------------------------------------------------------------------------
# 找爆炸影响区域
def bombRegion(index):
    effectList = []
    baseIndex = index[:]
    for i in DIRECTION:
        adjustedIndex = [baseIndex[0]+i[0],baseIndex[1]+i[1]]
        if inRegion(adjustedIndex) and (int(landform[adjustedIndex[0]][adjustedIndex[1]]) < 2):
            effectList.append(adjustedIndex)
            if landform[adjustedIndex[0]][adjustedIndex[1]] == '0':
                adjustedIndex2 = [adjustedIndex[0]+i[0],adjustedIndex[1]+i[1]]
                if inRegion(adjustedIndex2) and (int(landform[adjustedIndex2[0]][adjustedIndex2[1]]) < 2):
                    effectList.append(adjustedIndex2)
    return effectList
# -----------------------------------------------------------------------------
# 找某个炸弹周围被影响的区域
def lastbombRegion(index):
    effectList = [index]
    baseIndex = index[:]
    for i in DIRECTION:
        adjustedIndex = [baseIndex[0]+i[0],baseIndex[1]+i[1]]
        if inRegion(adjustedIndex) and (landform[adjustedIndex[0]][adjustedIndex[1]] == '-1'):
            effectList.append(adjustedIndex) 
        adjustedIndex2 = [adjustedIndex[0]+i[0],adjustedIndex[1]+i[1]]
        if inRegion(adjustedIndex2) and (landform[adjustedIndex2[0]][adjustedIndex2[1]] == '-1'):
            effectList.append(adjustedIndex2)
    return effectList
# -----------------------------------------------------------------------------
# 炸弹爆炸           
def userexplode(screen,index,delay):
    global landform 
    global score1
    global INURGENTMOVE
    time.sleep(delay-0.5)
    # sound effect
    
    if not INURGENTMOVE:
        UrgentMove(screen)
    time.sleep(0.3)
    if not INURGENTMOVE:
        UrgentMove(screen)
    try:
        explode_sound = pygame.mixer.Sound('explode.wav')
        explode_sound.play()
    except:
        pass
    effectZone = bombRegion(index)
    for i in effectZone:
        if landform[i[0]][i[1]]=='1':
            score1+=1
        else:
            score1=score1
        landform[i[0]][i[1]] = '-1'
    draw_block(screen)
    draw_player(screen)
    pygame.display.update()



    font = pygame.font.Font('font.ttf', 36)
    score_font=font
    score_text = score_font.render('Your_1 Score:%s'%score1, True, Red,BG_COLOR)
    text_rect = score_text.get_rect()
    text_rect.topleft =(matrix_width,25)
    screen.blit(score_text, text_rect)
    
    pygame.display.update()

    # see if any player is bombed
    WhetherBombed=[False,False]
    WhetherBombed = playerBombed(effectZone)
    if WhetherBombed[0] and WhetherBombed[1]:
        displayWinner(screen,0)
    elif WhetherBombed[0]:
        displayWinner(screen,2)
    elif WhetherBombed[1]:
        displayWinner(screen,1)
    if not INURGENTMOVE:
        UrgentMove(screen)
def machineexplode(screen,index,delay):
    global landform 
    global score2
    global font    
    global INURGENTMOVE
    time.sleep(delay-0.5)
    # sound effect
    
    if not INURGENTMOVE:
        UrgentMove(screen)
    time.sleep(0.3)
    if not INURGENTMOVE:
        UrgentMove(screen)
    try:
        explode_sound = pygame.mixer.Sound('explode.wav')
        explode_sound.play()
    except:
        pass
    effectZone = bombRegion(index)
    for i in effectZone:
        if landform[i[0]][i[1]]=='1':
            score2+=1
        else:
            score2=score2
        landform[i[0]][i[1]] = '-1'
    draw_block(screen)
    draw_player(screen)
    pygame.display.update() 
    
    font = pygame.font.Font('font.ttf', 36)
    score_font=font
    score_text = score_font.render('''Machine_2 Score:%s'''%score2, True, Red,BG_COLOR)
    text_rect = score_text.get_rect()
    text_rect.topleft =(matrix_width,18*25)
    screen.blit(score_text, text_rect)
    
    pygame.display.update()

    if WhetherBombed[0] and WhetherBombed[1]:
        displayWinner(screen,0)
    elif WhetherBombed[0]:
        displayWinner(screen,2)
    elif WhetherBombed[1]:
        displayWinner(screen,1)
    if not INURGENTMOVE:
        UrgentMove(screen)
    
# -----------------------------------------------------------------------------
# 炸弹爆炸恢复
def release(screen,index,delay):
    global landform
    global INURGENTMOVE
    
    time.sleep(delay-0.5)
    if not INURGENTMOVE:
        UrgentMove(screen)
        
    time.sleep(0.5)

    bombZone = lastbombRegion(index)
    for i in bombZone:
        landform[i[0]][i[1]] = '0'
    draw_block(screen)
    draw_player(screen)
    pygame.display.update()
    
    # update BombStack
    global BOMBSTACK
    BOMBSTACK = BOMBSTACK[1:]
    
    # new!!!
    while InDangerZone(PLAYERTWO):
        UrgentMove(screen)
# -----------------------------------------------------------------------------
def playerBombed(bombregionList,center=[]):
    playerOneDie = PLAYERONE in bombregionList or PLAYERONE == center
    playerTwoDie = PLAYERTWO in bombregionList or PLAYERTWO == center   
    return [playerOneDie,playerTwoDie]
# -----------------------------------------------------------------------------
# STATE 3: GAME OVER
# ----------------------------------------------------------------------------- 
def displayWinner(screen,winnerCode):
    global landform
    global playerOneWin_landform
    global playerTwoWin_landform
    
    if (landform != playerOneWin_landform) and (landform != playerTwoWin_landform):   
        if winnerCode == 1:
            landform = playerOneWin_landform[:]       
        else:
            landform = playerTwoWin_landform[:]  

        draw_block(screen)
        draw_player(screen)
        pygame.display.update()
    
    time.sleep(10)
    
    terminate()
    
# ----------------------------------------------------------------------------- 
# MACHINE SIDE
# -----------------------------------------------------------------------------    
def MachineMove(screen,stepFreq):
    while True:
        BombPlaced = False
        TRAJECTORY = []
        # ---------------------------------------------------------------------
        # BOMB EVENT
        # ---------------------------------------------------------------------
        # perform dice (设置比例*) BOMBPRO
        dice = random.random()
        if dice <= BOMBPRO:
            # evaluate bomb through simulation
            if RunSimulation():
                BombPlaced = True
                # 确定炸弹放置后逃离的trajectory                          
                # while 结构
                TRAJECTORY = []
                trajectoryPool = WALKOUTBOMB[:]
                random.shuffle(trajectoryPool)
                count = 0
                while (len(TRAJECTORY) == 0) and (count <= 19):
                    i = trajectoryPool[count]
                    PotentialLoc = PLAYERTWO[:]
                    CHOOSE = True
                    count2 = 0
                    for j in i:
                        PotentialLoc = [PotentialLoc[0]+j[0],PotentialLoc[1]+j[1]]
                        if count2 < (len(i) - 1):
                            # 不是wall/bomb placed/'-1'/dangerzone  
                            if not(legitMove(PotentialLoc)) or (InDangerZone(PotentialLoc)) or (PotentialLoc == PLAYERTWO):
                                CHOOSE = False
                                # new
                                #break
                        else:
                            # legitMove+不在dangerzone&potential dangerzone 
                            if CHOOSE and legitMove(PotentialLoc) and (PotentialLoc not in bombRegion(PLAYERTWO)) and not(InDangerZone(PotentialLoc)) and (PotentialLoc != PLAYERTWO):
                                TRAJECTORY = i
                                #new
                                break
                        count2 += 1
                    count += 1

             
                # 放置炸弹
                landform[PLAYERTWO[0]][PLAYERTWO[1]] = '3'
                draw_point(screen,PLAYERTWO)
                pygame.display.update()
                    
                # update BombStack
                BOMBSTACK.append(PLAYERTWO)
                
                # sound effect
                try:
                    bomb_sound = pygame.mixer.Sound('throw_bomb.wav')
                    bomb_sound.play()
                except:
                    pass
                
                # schedule炸弹event
                bombIndex = PLAYERTWO[:]
                _thread.start_new_thread(machineexplode,(screen,bombIndex,3))
                _thread.start_new_thread(release,(screen,bombIndex,4))
                
                # 盲目按照已经确定好的trajectory走
                for i in TRAJECTORY:
                    time.sleep(MACHINERUNAWAY)
                    draw_point(screen,PLAYERTWO)
                    PLAYERTWO[0] += i[0]
                    PLAYERTWO[1] += i[1]
                    draw_player(screen)
                    pygame.display.update()
                   
                    if walkIntoBomb(PLAYERTWO):
                        displayWinner(screen,1)
        
                # new***
                if len(TRAJECTORY) == 0:  # Placed a bomb without moving
                    Survive(screen)         
                            
        TRAJECTORY = []
        # ---------------------------------------------------------------------
        # MOVEMENT EVENT
        # ---------------------------------------------------------------------
        # new indent
        if not BombPlaced:
            MachineMoveOneStep(screen)
        
        # new???
        # TRAJECTORY lead to a danger zone?
        # can delete
        # don't move doesn't mean that current location is safe
        while InDangerZone(PLAYERTWO) or (PLAYERTWO in BOMBSTACK):
            if InDilemma(PLAYERTWO):
                if not INSURVIVAL:
                    Survive(screen)
                break
            else:
                MachineMoveOneStep(screen)
        
        # in case that TRAJECTORY doesn't work
        if InDilemma(PLAYERTWO):
            if not INSURVIVAL:
                Survive(screen)
        
        # new position
        time.sleep(stepFreq)
# -----------------------------------------------------------------------------  
def MachineMoveOneStep(screen,STRICT=True):
    # 只random出一个方向，不行就不走
    Direc = DIRECTION[random.randint(0,3)]
    PotentialLoc = [PLAYERTWO[0]+Direc[0],PLAYERTWO[1]+Direc[1]]
    # evaluate 这个方向可不可走，并执行
    if STRICT:
        # new
        if legitMove(PotentialLoc) and not(InDangerZone(PotentialLoc)) and landform[PotentialLoc[0]][PotentialLoc[1]] != '-1':
            draw_point(screen,PLAYERTWO)
            PLAYERTWO[0] += Direc[0]
            PLAYERTWO[1] += Direc[1]
            draw_player(screen)
            pygame.display.update()
            if walkIntoBomb(PLAYERTWO):
                displayWinner(screen,1)
    else:
        if inRegion(PotentialLoc) and (landform[PotentialLoc[0]][PotentialLoc[1]] == '0'):
            draw_point(screen,PLAYERTWO)
            PLAYERTWO[0] += Direc[0]
            PLAYERTWO[1] += Direc[1]
            draw_player(screen)
            pygame.display.update()
            if walkIntoBomb(PLAYERTWO):
                displayWinner(screen,1)
# -----------------------------------------------------------------------------
def SimulateOneStep(initialLoc,VoidLoc,lastStep,ForbiddenZone=[]):
    Direc = DIRECTION[random.randint(0,3)]
    PotentialLoc = [VoidLoc[0]+Direc[0],VoidLoc[1]+Direc[1]]
    # evaluate 这个方向可不可走，并执行
    if lastStep:
        if legitMove(PotentialLoc) and not(InDangerZone(PotentialLoc)) and (PotentialLoc != initialLoc) and (PotentialLoc not in ForbiddenZone):
            VoidLoc[0] += Direc[0]
            VoidLoc[1] += Direc[1]
            return VoidLoc,False
        else:
            if InDilemma(VoidLoc,ForbiddenZone) or (VoidLoc == initialLoc):
                return VoidLoc, True
    else:
        if legitMove(PotentialLoc) and not(InDangerZone(PotentialLoc)) and (PotentialLoc != initialLoc):
            VoidLoc[0] += Direc[0]
            VoidLoc[1] += Direc[1]
            return VoidLoc,False
        else:
            # 在这一步random walk选择不动
            # 如果既动不了，又处于dilemma，就会死
            if InDilemma(VoidLoc,initialLoc):
                return VoidLoc, True
    return VoidLoc,False
# ----------------------------------------------------------------------------- 
# Strictly Dangerous
def InDangerZone(index):
    CurrentStack = BOMBSTACK[:]
    for bombLoc in BOMBSTACK:
        effectZone = bombRegion(bombLoc)
        if index in effectZone:
            return True
    # new: update evaluation of BOMBSTACK danger
    while CurrentStack != BOMBSTACK:
        CurrentStack = BOMBSTACK[:]
        for bombLoc in BOMBSTACK:
            effectZone = bombRegion(bombLoc)
            if index in effectZone:
                return True    
    return False  
# -----------------------------------------------------------------------------
def task(NoMeaning):
    global THREADS
    SUICIDE = 0
    base = PLAYERTWO[:]
    #for i in range(SLTIME):
    VOID_PLAYERTWO = PLAYERTWO[:]
    potentialZone = bombRegion(PLAYERTWO)
    for j in range(SLSTEP):
        # last step: not in potentialZone/InDanger, not in originalLoc
        if j == SLSTEP-1:
            VOID_PLAYERTWO,trapped = SimulateOneStep(base,VOID_PLAYERTWO,True,potentialZone)
        else:
        # middle steps: not in originalLoc
            VOID_PLAYERTWO,trapped = SimulateOneStep(base,VOID_PLAYERTWO,False)
        if trapped:
            SUICIDE = 1
            break
    return SUICIDE
          
# ----------------------------------------------------------------------------- 
def RunSimulation():
    global SuicideTotal   
    from multiprocessing import Pool

    THREADS = 10
    msgs = [0.0 for x in range(SLTIME)]
    
    with Pool(THREADS) as p:
        results = p.map(task,msgs) 
        
    # Prob(Suicide) under random walk
    return (results.count(1)/SLTIME) <= SUICIDETHRESHOLD
# -----------------------------------------------------------------------------
def InDilemma(index,MoreDangerZone = []):
    # Delemma定义:本身位置在dangerzone + 上下左右四个位置 in danger zone/not legit move (strickly)
    #if InDangerZone(index) or (index in MoreDangerZone) or (not legitMove(index)):
    if InDangerZone(index) or (index in MoreDangerZone) or (index in BOMBSTACK):
        #ProbDirec = 0
        for i in DIRECTION:
            adjustedIndex = [index[0]+i[0],index[1]+i[1]]
            if legitMove(adjustedIndex) and not(InDangerZone(adjustedIndex)) and (adjustedIndex not in MoreDangerZone) and (adjustedIndex not in BOMBSTACK):
                #ProbDirec += 1
                return False
        #if ProbDirec == 0:
        return True
    return False
# ----------------------------------------------------------------------------- 
def UrgentMove(screen):
    global INURGENTMOVE
    global INSURVIVAL
    
    INURGENTMOVE = True
    # new
    while InDangerZone(PLAYERTWO) or (PLAYERTWO in BOMBSTACK):
        # new
        if InDilemma(PLAYERTWO):
            if not INSURVIVAL:
                Survive(screen)
            INURGENTMOVE = False
            return
        else:
            MachineMoveOneStep(screen)
            time.sleep(SURVIVALSPEED)
    INURGENTMOVE = False
# -----------------------------------------------------------------------------  
def Survive(screen):
    global INSURVIVAL

    INSURVIVAL = True
    for i in range(SURVIVALTRAIL):
        MachineMoveOneStep(screen,False)
        if not InDangerZone(PLAYERTWO):
            INSURVIVAL = False
            return
        time.sleep(SURVIVALSPEED)
    INSURVIVAL = False
# -----------------------------------------------------------------------------         
#程序终止
def terminate():
    # delay
    # sound effect
    try:
        die_sound = pygame.mixer.Sound('die.wav')
        die_sound.play()
    except:
        pass
    time.sleep(10) # 让炸弹炸出来
    try:
        pygame.display.quit()
        pygame.quit()
        sys.exit()
    except SystemExit:
        pygame.display.quit()
        pygame.quit()
        #sys.exit()
# -----------------------------------------------------------------------------
game()
