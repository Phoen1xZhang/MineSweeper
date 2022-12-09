import pygame
import sys
import elements
import random
import pygame.freetype
import time

global screen
global font
DARK_BROWN=139,69,19
GRAY=216,223,232
BLACK=0,0,0
LIGHTGREY=190,190,190
BLUE=63,81,186
global safeBlocks


def initGame():
    global screen
    pygame.init()
    windowSize=450,500
    screen=pygame.display.set_mode(windowSize)
    screen.fill(GRAY)
    pygame.display.set_caption("扫雷")


def drawBlocks():
    for i in range(0,10):
        for j in range(0,10):
            block=elements.Block((i,j))
            block.draw(screen)


def createMine():
    mineList=[]
    while len(mineList)!=10:
        x=random.randint(0,9)
        y=random.randint(0,9)
        if (x,y) not in mineList:
            mineList.append((x,y))
    return mineList


def startTheGame():
    global font
    initGame()
    font = pygame.freetype.Font('/System/Library/Fonts/Supplemental/Comic Sans MS.ttf', 20)

    global safeBlocks
    safeBlocks=[]

    #记录时间
    startTime=time.time()

    #记录剩余雷的数量
    numOfMines=10

    #笑脸图片
    laughImg=pygame.image.load('笑脸.jpg')
    laughImg=pygame.transform.scale(laughImg,(40,40))
    laughRect=laughImg.get_rect()
    laughRect.left=205
    laughRect.top=20

    #哭脸图片
    cryImg=pygame.image.load('哭脸.jpg')
    cryImg=pygame.transform.scale(cryImg,(40,40))
    cryRect=cryImg.get_rect()
    cryRect.left=205
    cryRect.top=20

    #判断游戏是否在进行中
    isInGame=True
    screen.blit(laughImg,laughRect)

    #画格子
    drawBlocks()

    #随机生成雷
    mineList=createMine()

    #雷图像
    mineImg=pygame.image.load('雷.png')
    mineImg=pygame.transform.scale(mineImg,(30,30))
    mineRect=mineImg.get_rect()

    #生成爆炸雷图像
    bombMine=pygame.image.load('爆炸雷.png')
    bombMine=pygame.transform.scale(bombMine,(39,39))
    bombMineRect=bombMine.get_rect()

    #生成旗子图像
    flagImg=pygame.image.load('旗子.png')
    flagImg=pygame.transform.scale(flagImg,(30,30))
    flagRect=flagImg.get_rect()
    flagList=[]

    while True:
        #显示剩余雷数
        pygame.draw.rect(screen, GRAY, (20, 20, 180, 50))
        font.render_to(screen, (20, 20), "number of mines:", BLACK)
        font.render_to(screen, (80, 50), str(numOfMines), BLACK)

        #显示时间
        if isInGame:
            pygame.draw.rect(screen,GRAY,(330,20,100,50))
            font.render_to(screen,(330,20),"time:",BLACK)
            font.render_to(screen,(340,50),str(round(time.time() - startTime, 0)),BLACK)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                mousePosition=event.pos
                blockY=int((mousePosition[0]-30)/39)
                blockX=int((mousePosition[1]-80)/39)
                if isInGame:
                    if 0<=blockX<=9 and 0<=blockY<=9 and mousePosition[0]>=30 and mousePosition[1]>=80:
                        if event.button==1:
                            if (blockX,blockY) not in mineList:
                                mineAround=countMineAround((blockX,blockY),mineList)
                                if mineAround==0:
                                    blocksHandled=[]
                                    dealWithEmptyBlock((blockX,blockY),mineList,blocksHandled)
                                else:
                                    pygame.draw.rect(screen, LIGHTGREY, (30 + 39 * blockY, 80 + 39 * blockX, 39, 39))
                                    pygame.draw.rect(screen, BLACK, (30 + 39 * blockY, 80 + 39 * blockX, 39, 39), 1)
                                    font.render_to(screen, (30+39*blockY+15,80+39*blockX+15), str(mineAround), BLACK)
                                    safeBlocks.append((blockX,blockY))
                            else:
                                bombMineRect.left=30+blockY*39
                                bombMineRect.top=80+blockX*39
                                screen.blit(bombMine,bombMineRect)
                                pygame.draw.rect(screen, BLACK, (30 + 39 * blockY, 80 + 39 * blockX, 39, 39), 1)
                                for mine in mineList:
                                    if mine!=(blockX,blockY):
                                        pygame.draw.rect(screen, BLUE, (30 + 39 * mine[1], 80 + 39 * mine[0], 39, 39))
                                        pygame.draw.rect(screen, BLACK, (30 + 39 * mine[1], 80 + 39 * mine[0], 39, 39), 1)
                                        mineRect.left=30+mine[1]*39+5
                                        mineRect.top=80+mine[0]*39+5
                                        screen.blit(mineImg,mineRect)
                                screen.blit(cryImg,cryRect)
                                isInGame=False

                        if event.button==3:
                            if (blockX,blockY) not in flagList:
                                flagRect.left=30+blockY*39+5
                                flagRect.top=80+blockX*39+5
                                screen.blit(flagImg,flagRect)
                                flagList.append((blockX,blockY))
                                numOfMines-=1
                            else:
                                flagList.remove((blockX,blockY))
                                pygame.draw.rect(screen,BLUE,(30+39*blockY,80+39*blockX,39,39))
                                pygame.draw.rect(screen, BLACK, (30 + 39 * blockY, 80 + 39 * blockX, 39, 39), 1)
                                numOfMines+=1
                            pass

                    else:
                        if 205 <= mousePosition[0] <= 245 and 20 <= mousePosition[1] <= 60:
                            drawBlocks()
                            mineList=createMine()
                            safeBlocks.clear()
                            numOfMines=10
                            startTime=time.time()
                            flagList.clear()

                if not isInGame:
                    if 205<=mousePosition[0]<=245 and 20<=mousePosition[1]<=60:
                        screen.blit(laughImg,laughRect)
                        isInGame=True
                        drawBlocks()
                        mineList=createMine()
                        safeBlocks.clear()
                        numOfMines=10
                        startTime=time.time()
                        flagList.clear()

        if len(safeBlocks)==90:
            for mine in mineList:
                pygame.draw.rect(screen,BLUE,(30+39*mine[1],80+39*mine[0],39,39))
                pygame.draw.rect(screen,BLACK,(30+39*mine[1],80+39*mine[0],39,39),1)
                mineRect.left = 30 + mine[1] * 39 + 5
                mineRect.top = 80 + mine[0] * 39 + 5
                screen.blit(mineImg, mineRect)
            isInGame=False

        pygame.display.update()


def dealWithEmptyBlock(block,mineList,blocksHandled):
    global safeBlocks
    if block not in safeBlocks:
        safeBlocks.append(block)

    pygame.draw.rect(screen, LIGHTGREY, (30 + 39 * block[1], 80 + 39 * block[0], 39, 39))
    pygame.draw.rect(screen, BLACK, (30 + 39 * block[1], 80 + 39 * block[0], 39, 39), 1)
    blocksHandled.append(block)
    mineAround=countMineAround(block,mineList)
    if mineAround!=0:
        font.render_to(screen, (30 + 39 * block[1] + 15, 80 + 39 * block[0] + 15), str(mineAround),BLACK)
        print("Handled block positioned at ",block," with ",mineAround," mines around.")
    else:
        aroundBlocks=getAroundBlocks(block)
        print("The program is going to handle the blocks around the block positioned at ",block)
        for block in aroundBlocks:
            if block not in blocksHandled and block not in mineList:
                dealWithEmptyBlock(block,mineList,blocksHandled)


def getAroundBlocks(blockPos):
    res=[]

    if blockPos[0]==0 and blockPos[1]!=0 and blockPos[1]!=9:
        for i in range(-1,2):
            res.append((blockPos[0]+1,blockPos[1]+i))
        res.append((blockPos[0], blockPos[1] - 1))
        res.append((blockPos[0], blockPos[1] + 1))
    elif blockPos[0]==9 and blockPos[1]!=0 and blockPos[1]!=9:
        for i in range(-1,2):
            res.append((blockPos[0]-1,blockPos[1]+i))
        res.append((blockPos[0], blockPos[1] - 1))
        res.append((blockPos[0], blockPos[1] + 1))
    elif blockPos[1]==0 and blockPos[0]!=0 and blockPos[0]!=9:
        for i in range(-1,2):
            res.append((blockPos[0]+i,1))
        res.append((blockPos[0]-1,blockPos[1]))
        res.append((blockPos[0]+1,blockPos[1]))
    elif blockPos[1]==9 and blockPos[0]!=0 and blockPos[0]!=9:
        for i in range(-1,2):
            res.append((blockPos[0]+i,8))
        res.append((blockPos[0]-1,blockPos[1]))
        res.append((blockPos[0]+1,blockPos[1]))
    elif blockPos==(0,0):
        res.append((0,1))
        res.append((1,0))
        res.append((1,1))
    elif blockPos==(0,9):
        res.append((0,8))
        res.append((1,9))
        res.append((1,8))
    elif blockPos==(9,0):
        res.append((8,0))
        res.append((9,1))
        res.append((8,1))
    elif blockPos==(9,9):
        res.append((9,8))
        res.append((8,9))
        res.append((8,8))
    else:
        for i in range(-1,2):
            res.append((blockPos[0]-1,blockPos[1]+i))
            res.append((blockPos[0]+1,blockPos[1]+i))
        res.append((blockPos[0],blockPos[1]-1))
        res.append((blockPos[0],blockPos[1]+1))

    return res


def countMineAround(pos,mineList):
    count=0
    for i in range(-1,2):
        if (pos[0]-1,pos[1]+i) in mineList:
            count+=1
        if (pos[0]+1,pos[1]+i) in mineList:
            count+=1
    if (pos[0],pos[1]-1) in mineList:
        count+=1
    if (pos[0],pos[1]+1) in mineList:
        count+=1
    return count


if __name__=='__main__':
    startTheGame()