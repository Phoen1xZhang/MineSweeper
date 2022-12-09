import pygame
import pygame.freetype


class Block:
    def __init__(self,position):
        self.size=39
        self.position=position
        self.boarderColor=0,0,0
        self.insideColor=63,81,186
        self.boarderWidth=1
        self.hasMine=False
        self.realPos=(30+self.position[1]*self.size,80+self.position[0]*self.size)

    def draw(self,screen):
        pygame.draw.rect(screen,self.insideColor,(30+self.position[1]*self.size,80+self.position[0]*self.size,self.size,self.size))
        pygame.draw.rect(screen,self.boarderColor,(30+self.position[1]*self.size,80+self.position[0]*self.size,self.size,self.size),self.boarderWidth)

    def getPosition(self):
        return self.position

    def getRealPos(self):
        return self.realPos

    def showNum(self,screen,num):
        font=pygame.freetype.Font('/System/Library/Fonts/Supplemental/Comic Sans MS.ttf',20)
        GRAY = 216, 223, 232
        font.render_to(screen,self.realPos,str(num),GRAY)