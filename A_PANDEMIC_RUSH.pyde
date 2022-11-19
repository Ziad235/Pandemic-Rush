# IMPORTING MODULES AND LIBRARIES FOR GAME FLOW AND SOUNDS
import os
import random
import time
add_library("minim")
path = os.getcwd()
game_sound = Minim(this)
level_sound = Minim(this)
menu_sound = Minim(this)

# SCREEN DIMENSIONS
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# INITIALIZING IMAGES AND SOUNDS FOR GLOBAL USE
enemy_image = loadImage(path + "/enemy.png")
player_image = loadImage(path + "/player.png")
player_lose = loadImage(path + "/player_lose.png")
player_win = loadImage(path + "/player_win.png")
enemy_fire = loadImage(path + "/enemy_win.png")
start_menu = loadImage(path + "/menu.png")
rules = loadImage(path + "/rules.png")
booster1 = loadImage(path + "/booster1.png")
booster2 = loadImage(path + "/booster2.png")

PLAYER_SPEED = 7 #SPEED OF PLAYER
MAX_UP = 150 # MAXIMUM HIGH OF SCREEN PLAYER CAN REACH
MAX_SCORE = 300 # MAXIMUM SCORE PLAYER CAN EARN BEFORE WINNING

MIN_ENEMY_SIZE = 50 # MINIMUM ENEMY SIZE
MAX_ENEMY_SIZE = 70 # MAXIMUM ENEMY SIZE

NUM_MAX_ENEMIES = 8 # MAXIMUM ENEMIES DROPPED ON SCREEN PER FRAME RATE
NUM_MAX_BOOSTER1 = 1 # MAXIMUM FIRST BOOSTER DROPPED ON SCREEN PER FRAME RATE
NUM_MAX_BOOSTER2 = 1 # MAXIMUM SECOND BOOSTER DROPPED ON SCREEN PER FRAME RATE

# GLOBAL VARIABLES TO CONTROL STARTING AND ENDING OF GAME
PAUSE = False
OVER = False
WON = False

# CLASS FOR ENEMY INCLUDES RANGE OF SIZE, STARTING X AND Y POSITIONS ON SCREEN AND IMAGE DISPLAY
class Enemy():
    def __init__(self, occupied, enemies):
        self.enemy_size = random.randint(MIN_ENEMY_SIZE, MAX_ENEMY_SIZE)
        self.positionx = random.randint (0, (SCREEN_WIDTH - self.enemy_size)) 
        self.positiony = 0
        
    def display(self):
        image(enemy_image, self.positionx, self.positiony, self.enemy_size, self.enemy_size)

# CLASS FOR BOOSTER INCLUDES STARTING X AND Y POSITIONS ON SCREEN AND BOOSTERS 1&2 DISPLAY            
class Booster():
    def __init__(self, taken, booster):
        self.positionx_b = random.randint(0, (SCREEN_WIDTH - 80)) 
        self.positiony_b = 0
        
    def display_booster1(self):
        image(booster1, self.positionx_b, self.positiony_b, 80, 40)
        
    def display_booster2(self):
        image(booster2, self.positionx_b, self.positiony_b, 40, 80)
        
# CLASS FOR PLAYER INCLUDES STARTING X AND Y POSITIONS ON SCREEN AND IMAGE DISPLAY ACCORDING TO SITUATION IN GAME
class Player():
    def __init__(self):
        self.x = SCREEN_WIDTH//2.2
        self.y = SCREEN_HEIGHT - 80
        
    def display(self):
        image(player_image, self.x, self.y, 45, 45)
        
    def lose_display(self):
        image(player_lose, self.x, self.y, 45, 45)
        
    def win_display(self):
        image(player_win, 300, 450, 107, 78)

# CLASS FOR GAME INCLUDES RULES AND MECHANICS OF THE GAME
class Game():
    def __init__(self):
        self.key_handler = {UP: False, DOWN: False, RIGHT: False, LEFT:False}
        self.player = Player()
        self.stage = 1
        self.start = False
        self.score = 0
        self.highscore = 0
        self.enemies = [] # 2D LIST TO STORE ENEMIES IN ORDER TO ADD OR DELETE THEM WHEN NECESSARY
        self.booster1 = [] # 2D LIST TO STORE BOOSTER 1 IN ORDER TO ADD OR DELETE THEM WHEN NECESSARY
        self.booster2 = [] # 2D LIST TO STORE BOOSTER 2 IN ORDER TO ADD OR DELETE THEM WHEN NECESSARY
        self.speedenemy = ["",5,7,10] # 2D LIST TO STORE ENEMY SPEEDS IN ORDER TO CHANGE ACCORDING TO STAGE
        self.occupied = [] # 2D LIST TO STORE ENEMY PRESENCE IN ORDER TO ADD OR MAKE ENEMIES MOVE ACCORDINGLY 
        self.taken =[] # 2D LIST TO STORE BOOSTER PRESENCE IN ORDER TO ADD OR MAKE ENEMIES MOVE ACCORDINGLY 
        # SOUNDS USED FOR GAME CLASS ACCORDING TO GAME SITUATION
        self.next_level = level_sound.loadFile(path + "/next_level.mp3")
        self.bg_music = game_sound.loadFile(path + "/game_sound.mp3")
        self.game_over = level_sound.loadFile(path + "/game_over.mp3")
        self.win_game = level_sound.loadFile(path + "/win_game.mp3")
        self.booster_sound  = level_sound.loadFile(path + "/booster_sound.mp3")
        self.bg_music.loop()
    
    # METHOD FOR ADDING ENEMIES ON SCREEN BY APPEDNING THEM TO THE INITALIZED LIST    
    def addEnemy(self):
        if len(self.enemies)<NUM_MAX_ENEMIES:
            newenemy = Enemy(self.occupied, self.enemies)
            self.enemies.append(newenemy)
    
    # METHOD FOR ADDING BOOSTER 1 ON SCREEN BY APPEDNING IT TO THE INITALIZED LIST 
    def addbooster1(self):
        if len(self.booster1)<NUM_MAX_BOOSTER1:
            newbooster1 = Booster(self.taken, self.booster1)
            self.booster1.append(newbooster1)
    
    # METHOD FOR ADDING BOOSTER 2 ON SCREEN BY APPEDNING IT TO THE INITALIZED LIST 
    def addbooster2(self):
        if len(self.booster2)<NUM_MAX_BOOSTER2:
            newbooster2 = Booster(self.taken, self.booster2)
            self.booster2.append(newbooster2)  
            
     # METHOD FOR MOVING BOOSTERS ON SCREEN WITH SPEED AND DELETING THEM FROM INITIALIZED LIST WHEN PASSED OFF SCREEN              
    def moveBooster(self):       
        for booster in self.booster1:
            if booster.positiony_b > SCREEN_HEIGHT:
                self.booster1.remove(booster)
                self.taken.remove(booster.positionx_b)
            else:
                try:
                    booster.positiony_b += 10 
                except:
                    pass  
        for booster in self.booster2:
            if booster.positiony_b > SCREEN_HEIGHT:
                self.booster2.remove(booster)
                self.taken.remove(booster.positionx_b)
            else:
                try:
                    booster.positiony_b += 10
                except:
                    pass    
    
    # METHOD FOR MOVING ENEMIES ON SCREEN WITH SPEED ACCORDING TO STAGE AND DELETING THEM FROM INITIALIZED LIST WHEN PASSED OFF SCREEN 
    def moveEnemy(self):       
        for enemy in self.enemies:
            if enemy.positiony > SCREEN_HEIGHT:
                self.enemies.remove(enemy)
                self.occupied.remove(enemy.positionx)
            else:
                try:
                    enemy.positiony += self.speedenemy[self.stage]
                except:
                    pass
                    
    # METHOD FOR MOVING PLAYER ON SCREEN WITH SPEED WITH RESTRICTIONS        
    def movePlayer(self):
        for code in self.key_handler:
            if self.key_handler[code]:
                if code == UP and self.player.y > MAX_UP:
                    self.player.y -= PLAYER_SPEED
                if code == DOWN and self.player.y < SCREEN_HEIGHT - 90:
                    self.player.y += PLAYER_SPEED
                
                if code == RIGHT and self.player.x < SCREEN_WIDTH - 85:
                    self.player.x += PLAYER_SPEED
                if code == LEFT and self.player.x >=35:
                    self.player.x -= PLAYER_SPEED
     
    # METHOD FOR CREATING AND READING A TEXT FILE THAT STORES HIGHEST SCORE NO MATTER WHAT (UNLESS FILE IS DELETED)          
    def score_board(self):
        try:
            with open("high_score.txt", "r") as f:
                try:
                    self.highscore = int(f.read())
                except:
                    pass
        except:
            pass
            
        if self.score > self.highscore:
            with open("high_score.txt", "w") as f:
                f.write(str(int(self.score)))
        else:
            with open("high_score.txt", "w") as f:
                f.write(str(int(self.highscore)))
    
    # METHOD FOR REGISTERING COLLISION BETWEEN PLAYER AND ENEMY 
    def detectCollision(self):
        global OVER
        for enemy in self.enemies:
            if self.player.x-45<=enemy.positionx<=self.player.x+42:
                if self.player.y-45<=enemy.positiony<=self.player.y+42:
                    self.collision = enemy
                    OVER = True
                    return OVER
     
    # METHOD FOR REGISTERING COLLISION BETWEEN PLAYER AND BOOSTER 1        
    def boosterCollision1(self):
        for Booster in self.booster1:
             if self.player.x-60<=Booster.positionx_b<=self.player.x+42:
                if self.player.y-55<=Booster.positiony_b<=self.player.y+42:
                    self.booster1.remove(Booster)
                    self.collision = Booster
                    self.booster_sound.rewind()
                    self.booster_sound.play()
                    return True
    
    # METHOD FOR REGISTERING COLLISION BETWEEN PLAYER AND BOOSTER 1            
    def boosterCollision2(self):
        for Booster in self.booster2:
             if self.player.x-60<=Booster.positionx_b<=self.player.x+42:
                if self.player.y-55<=Booster.positiony_b<=self.player.y+42:
                    self.booster2.remove(Booster)
                    self.collision = Booster
                    self.booster_sound.rewind()
                    self.booster_sound.play()
                    return True
    
    # METHOD FOR ENDING GAME           
    def game_lost(self):
        if OVER == True:
            return True
        else: 
            return False            
     
    # METHOD FOR CHECKING AND CHANGING STAGES WITH DIFFICULTY   (AS LONG AS PLAYER IS NOT DEAD)      
    def checkStage(self):
        if self.score >= 50 and self.stage == 1:
            self.next_level.rewind()
            self.next_level.play()
            self.stage +=1
            NUM_MAX_ENEMIES = 12
            return True
        
        elif self.score >= 150 and self.stage == 2:
            self.next_level.rewind()
            self.next_level.play()
            self.stage +=1
            NUM_MAX_ENEMIES = 16
            return True
        
        elif self.score >= MAX_SCORE and self.stage == 3:
            fill(66, 255, 246)
            rect(30, 180, 500, 200)
            fill(69, 255, 66)
            rect(50, 170, 500,190)
            self.player.win_display()
            fill(0,0,0)
            textSize(50)
            text("WINNER!", 195, SCREEN_HEIGHT//2.3)
            textSize(30)
            text("CLICK TO RETURN TO MENU", SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2.5 + 95)
            game_sound.stop()
            self.win_game.play()
            WON = True
            return True
      
    # METHOD TO RESTART GAME
    def restart(self):
        self.__init__()
    
    # METHOD FOR DISPLAYING THE ENTIRE GAME
    def display(self):
        global PAUSE
        # DISPLAYS HOME SCREEN
        if not self.start:
            self.bg_music.rewind()
            rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)
            background(4, 51, 59)
            image(start_menu, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
            fill(255, 136, 0)
            rect(0, 420, 280, 150)
            fill(136,0,255)
            rect(10,410,280,150)
            fill(0,0,0)
            textSize(40)
            text("PRESS ENTER", 30, 475)
            textSize(35)
            text("TO PLAY", 70, 530)
            fill(255, 136, 0)
            rect(300, 420, 280, 150)
            fill(136,0,255)
            rect(310,410,280,150)
            fill(0,0,0)
            textSize(40)
            text("PRESS TAB", 350, 475)
            textSize(35)
            text("FOR RULES", 360, 530)

        else:
            # DISPLAYS AND EXECUTES THE GAME WITH RULES
            background(31, 78, 121)
            self.detectCollision()
            if not self.detectCollision():
                if self.boosterCollision1():
                    self.score += 10
                elif self.boosterCollision2():
                    self.score += 15
                if self.checkStage():
                    PAUSE = True
                if not PAUSE:
                    self.score += 0.05
                    self.movePlayer()
                    self.player.display()
                    for enemy in self.enemies:
                        enemy.display()
                        if enemy.positionx not in self.occupied:
                            self.occupied.append(enemy.positionx)
                    for b in self.booster1:
                        b.display_booster1()
                        if b.positionx_b not in self.taken:
                            self.taken.append(b.positionx_b)
                    for b in self.booster2:
                        b.display_booster2()
                        if b.positionx_b not in self.taken:
                            self.taken.append(b.positionx_b)
                            
     
                    self.addEnemy()
                    self.moveEnemy()
                    self.addbooster1()
                    self.addbooster2()
                    self.moveBooster()
                
                # DISPLAYS WHEN PLAYER REACHES NEW STAGE
                elif self.score < MAX_SCORE:
                    fill(255, 187, 0)
                    rect(30, 180, 500, 200)
                    fill(255, 174, 0)
                    rect(50, 170, 500,190)
                    fill(0,0,0)
                    self.player.display()
                    textSize(40)
                    text("NEXT STAGE", SCREEN_WIDTH//1.81 -160,SCREEN_HEIGHT//2.5)
                    textSize(30)
                    text("CLICK TO CONTINUE", SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2.5 + 70)

            # DISPLAYS WHEN PLAYER LOSES    
            elif self.detectCollision():
                fill(252, 3, 132)
                rect(30, 180, 500, 200)
                fill(177, 3, 252)
                rect(50, 170, 500,190)
                self.game_over.play()
                self.player.lose_display()
                self.collision.display()
                textSize(50)
                fill(255, 255, 255)
                text("GAME OVER",SCREEN_WIDTH//2 -150,SCREEN_HEIGHT//2.5)
                textSize(30)
                text("CLICK TO RETURN TO MENU", SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT //2.5 + 75)    
                game_sound.stop()

            # DISPLAYS AS LONG PLAYER HAS NEITHER LOST NOR WON
            if not WON:
                fill(0, 0, 0)
                rect(0, 0, 180, 60)
                rect(490, 0, 310, 60)
                fill(255, 255, 255)
                textSize(20)
                text(("STAGE: " + str(self.stage)), 500, 40)
                text(("SCORE: " + str(int(self.score))), 5, 25)
                text("HIGH SCORE: "+ str(int(self.highscore)), 5, 50)

            
game = Game() #INSTANTIATING GAME CLASS

def setup():
    size(SCREEN_WIDTH, SCREEN_HEIGHT)

def draw():
    game.display()
    game.score_board()
    # DISPLAYS RULES OF GAME WHEN KEY TAB IS PRESSED
    if key == TAB and not game.start:
        image(rules, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        
def keyPressed():
    # STARTS GAME WHEN KEY ENTER IS PRESSED (AS LONG AS GAME IS NOT RUNNING)
    if key == ENTER and not game.start:
        game.start = True
    # MOVES THE PLAYER
    if keyCode in game.key_handler:
        game.key_handler[keyCode] = True
    # CLICK SOUND WHEN PLAYER ALTERNATES BETWEEN START MENU AND RULES PAGE
    if (key == TAB or key == BACKSPACE) and not game.start:
        menu_sound.loadFile(path + "/mouse_click.mp3").rewind()
        menu_sound.loadFile(path + "/mouse_click.mp3").play()

def keyReleased():
    # STOPS PLAYER FROM MOVING FARTHER WHEN KEY IS RELEASED 
    if keyCode in game.key_handler:
        game.key_handler[keyCode] = False
        
def mouseClicked():
    global PAUSE, OVER
    if PAUSE and not WON:
        for enemy in game.enemies:
            enemy.positiony = 15
        PAUSE = False
        
    if OVER:
        game.__init__()
        OVER = False
        
    # RESTARTS THE GAME WHEN PLAYER LOSES
    if game.game_lost():
        game.restart()

    if game.checkStage() and not WON:
        level_sound.stop()
        game.restart()
    
        
    
        
              
