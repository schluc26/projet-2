import pgzrun
from random import randint
import math
DIFFICULTY = 1
DIFFICULTY = 1
player = Actor("beyond", (400, 550)) # Load in the player Actor image

def draw(): # Pygame Zero draw function
    screen.blit('background', (0, 0))
    player.image = player.images[math.floor(player.status/6)]
    player.draw()
    #drawbatarangs()
    drawjokerface()
    drawBases()
    screen.draw.text(str(score) , topright=(780, 10), owidth=0.5, ocolor=(255,255,255), color=(0,64,255) , fontsize=60)
    if player.status >= 30:
        screen.draw.text("GAME OVER\nPress Enter to play again" , center=(400, 300), owidth=0.5, ocolor=(255,255,255), color=(255,64,0) , fontsize=60)
    if len(jokers) == 0 :
        screen.draw.text("YOU WON!\nPress Enter to play again" , center=(400, 300), owidth=0.5, ocolor=(255,255,255), color=(255,64,0) , fontsize=60)
        
def update(): # Pygame Zero update function
    global moveCounter,player
    if player.status < 30 and len(jokers) > 0:
        checkKeys()
        updatebatarangs()
        moveCounter += 1
    if moveCounter == moveDelay:
        moveCounter = 0
        updatejokerface() 
    if player.status > 0: player.status += 1
    else:
      if keyboard.RETURN: init()

def drawjokers():
    for a in range(len(jokers)): jokers[a].draw()

def drawBases():
    for b in range(len(bases)): bases[b].drawClipped()

def drawbatarang():
    for l in range(len(batarangs)): batarangs[l].draw()

def checkKeys():
    global player, batarangs
    if keyboard.left:
        if player.x > 40: player.x -= 5
    if keyboard.right:
        if player.x < 760: player.x += 5
    if keyboard.space:
        if player.laserActive == 1:
            player.laserActive = 0
            clock.schedule(makeLaserActive, 1.0)
            l = len(batarangs)
            batarangs.append(Actor("batarangs", (player.x,player.y-32)))
            batarangs[l].status = 0
            batarangs[l].type = 1

def makeLaserActive():
    global player
    player.laserActive = 1
            
def checkBases():
    for b in range(len(bases)):
        if l < len(bases):
            if bases[b].height < 5:
                del bases[b]

def updatebatarangs():
    global batarangs, jokers
    for l in range(len(batarangs)):
        if batarangs[l].type == 0:
            batarangs[l].y += (2*DIFFICULTY)
            checkLaserHit(l)
            if batarangs[l].y > 600: batarangs[l].status = 1
        if batarangs[l].type == 1:
            batarangs[l].y -= 5
            checkPlayerLaserHit(l)
            if batarangs[l].y < 10: batarangs[l].status = 1
    batarangs = listCleanup(batarangs)
    jokers = listCleanup(jokers)

def listCleanup(l):
    newList = []
    for i in range(len(l)):
        if l[i].status == 0: newList.append(l[i])
    return newList
    
def checkLaserHit(l):
    global player
    if player.collidepoint((batarangs[l].x, batarangs[l].y)):
        player.status = 1
        batarangs[l].status = 1
    for b in range(len(bases)):
        if bases[b].collideLaser(batarangs[l]):
            bases[b].height -= 10
            batarangs[l].status = 1

def checkPlayerLaserHit(l):
    global score
    for b in range(len(bases)):
        if bases[b].collideLaser(batarangs[l]): batarangs[l].status = 1
    for a in range(len(jokers)):
        if jokers[a].collidepoint((batarangs[l].x, batarangs[l].y)):
            batarangs[l].status = 1
            jokers[a].status = 1
            score += 1000
            
def updateJokers():
    global moveSequence, batarangs, moveDelay
    movex = movey = 0
    if moveSequence < 10 or moveSequence > 30: movex = -15
    if moveSequence == 10 or moveSequence == 30:
        movey = 50 + (10 * DIFFICULTY)
        moveDelay -= 1
    if moveSequence >10 and moveSequence < 30: movex = 15
    for a in range(len(jokers)):
        animate(jokers[a], pos=(jokers[a].x + movex, jokers[a].y + movey), duration=0.5, tween='linear')
        if randint(0, 1) == 0:
            jokers[a].image = "jokerface"
            if randint(0, 5) == 0:
                batarangs.append(Actor("laser1", (jokers[a].x,jokers[a].y)))
                batarangs[len(batarangs)-1].status = 0
                batarangs[len(batarangs)-1].type = 0
        if jokers[a].y > player.y and player.status == 0:
            player.status = 1
    moveSequence +=1
    if moveSequence == 40: moveSequence = 0

def init():
    global batarangs, score, player, moveSequence, moveCounter, moveDelay
    initjokers()
    initBases()
    moveCounter = moveSequence = player.status = score = player.laserCountdown = 0
    batarangs = []
    moveDelay = 30
    player.images = ["beyond","explosion1","explosion2","explosion3","explosion4","explosion5"]
    player.laserActive = 1

def initjokers():
    global jokers
    jokers = []
    for a in range(18):
        jokers.append(Actor("jokerface", (210+(a % 6)*80,100+(int(a/6)*64))))
        jokers[a].status = 0

def drawClipped(self):
    screen.surface.blit(self._surf, (self.x-32, self.y-self.height+30),(0,0,64,self.height))

def collideLaser(self, other):
    return (
        self.x-20 < other.x+5 and
        self.y-self.height+30 < other.y and
        self.x+32 > other.x+5 and
        self.y-self.height+30 + self.height > other.y
    )

def initBases():
    global bases
    bases = []
    bc = 0
    for b in range(3):
        for p in range(3):
            bases.append(Actor("base1", midbottom=(150+(b*200)+(p*40),520)))
            bases[bc].drawClipped = drawClipped.__get__(bases[bc])
            bases[bc].collideLaser = collideLaser.__get__(bases[bc])
            bases[bc].height = 60
            bc +=1
    
init()
