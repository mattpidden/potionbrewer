import pygame
import Object_Detection
import time
import random
from pygame import mixer

#SETTING UP PYGAME WINDOW
print("Sounds from ZapSplat.com")
print("Please ensure your volume is turned on for a better experience")
pygame.init()
buttonSoundAffect = pygame.mixer.Sound("axe.mp3")
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
colour1 = (2,37,69) #DARK BLUE
colour2 = (151,107,147) #PINKY PURPLE
colour3 = (255,215,167) #CREAM
colour4 = (98,119,58) #GREEN
colour5 = (255, 255, 255) #WHITE

state = "menu"
startTime = 0
#Meaning the potion will... // the potion was supposed to...
purposes = ["give you the ability to fly.", "allow you to mind read.", "give you infinite luck.", "grant you 3 wishes.", "allow you to turn invisible.", "allow you to breath underwater.", "allow you to talk to animals.", "halt you ageing process immediately."]
#it may have a side effect of...
sideEffects = ["shrinking your head.", "turning you into a frog.", "turning you into a cow.", "making your hair turn pink.", "making you smell like an onion.", "turning you into a tree.", "giving you infinite bad luck.", "shrinking you to the size of a coin.", "turning you into a witch."]

instructionBoxWidth = 560
instructionBoxHeight = 400
instructionBoxX = (width // 2) - (instructionBoxWidth // 2)
instructionBoxY = 90
instructionBoxFontSize = 25
instructionBoxFont = pygame.font.SysFont("Arial", instructionBoxFontSize)

startW, startH, startX, startY = 560, 70, (width // 2) - (560 // 2), 510
quitW, quitH, quitX, quitY = 50, 50, width-50-20, 20

def drawBox(W, H, X, Y, fSize, text, boxColour, textColour):
    font = pygame.font.SysFont("Arial", fSize)
    box = pygame.draw.rect(screen, boxColour, (X, Y, W, H))
    boxTextSurface = font.render(text, True, textColour)
    boxTextRect = boxTextSurface.get_rect()
    boxTextRect.center = (X + W // 2, Y + H // 2)
    screen.blit(boxTextSurface, boxTextRect)

def checkMouseInsideRect(W, H, X, Y):
    mouse = pygame.mouse.get_pos()
    if X <= mouse[0] <= X+W and Y <= mouse[1] <= Y+H:
        return True

def QuitGame():
    buttonSoundAffect.play()
    state = "quit"
    pygame.quit()
    Object_Detection.EndObjectDetection(cap)

#SETTING UP OBJECT DETECTION
net, classes, colours, cap = Object_Detection.SetUpDetector()
objectsFound = []
objectsToFind = []

pygame.mixer.music.load("atmosphere.mp3")
pygame.mixer.music.play(-1)
        
#PYGAME WINDOW
while True:
    if state == "menu":
        #INTERACITIVTY
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QuitGame()
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if checkMouseInsideRect(startW, startH, startX, startY):
                    pygame.display.quit()
                    objectsToFind = Object_Detection.GetRandomListToFind()
                    net, classes, colours, cap = Object_Detection.SetUpDetector()
                    objectsFound = []
                    net, classes, colours, cap, objectsToFind, objectsFound = Object_Detection.AnalyseFrame(net, classes, colours, cap, objectsToFind, objectsFound)
                    startTime = time.time()
                    state = "playing"
                    buttonSoundAffect.play()
                    mixer.music.load("song.mp3")
                    mixer.music.play()
                    screen = pygame.display.set_mode((width, height))
                if checkMouseInsideRect(quitW, quitH, quitX, quitY):
                    QuitGame()
                    break
                
        #DRAWING
        screen.fill(colour1)

        #TITLE BOX AND QUIT BUTTON
        drawBox(560, 50, (width // 2) - (560 // 2), 20, 50, "Potion Brewer", colour2, colour1)
        if checkMouseInsideRect(quitW, quitH, quitX, quitY):
            boxColour = (255,230,180)
        else: 
            boxColour = (255,215,167)
        drawBox(quitW, quitH, quitX, quitY, 50, "X", boxColour, colour2)

        #INSTRUCTIONS
        instructionBoxText = ["INSTRUCTIONS: ",
                      "Once you click start, a list of 7",
                      "different objects will appear.",
                      "The aim of the game is to find and",
                      "show as many of those objects as you",
                      "can in 2 minutes. Each time you show",
                      "an object it is added to the brewing",
                      "potion, for which you will find",
                      "out its affect upon completion."]
        instructionBox = pygame.draw.rect(screen, colour2, (instructionBoxX, instructionBoxY, instructionBoxWidth, instructionBoxHeight))
        instructionBoxTextSurface = []
        for line in instructionBoxText: 
            instructionBoxTextSurface.append(instructionBoxFont.render(line, True, colour5))
        for line in range(len(instructionBoxTextSurface)):
            screen.blit(instructionBoxTextSurface[line], (instructionBoxX + 25, instructionBoxY+20+(line*instructionBoxFontSize)+(15*line)))

        #START BUTTON
        if checkMouseInsideRect(startW, startH, startX, startY): 
            boxColour = (255,230,180)
        else: 
            boxColour = (255,215,167)
        drawBox(startW, startH, startX, startY, 65, "START BREWING", boxColour, colour1)

        pygame.display.update()
        
    elif state == "playing":
        #INTERACITIVTY
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QuitGame()
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if checkMouseInsideRect(quitW, quitH, quitX, quitY):
                    QuitGame()
                    break
        #BACKGROUND TITLE AND QUIT BUTTON
        screen.fill(colour2)
        drawBox(560, 50, (width // 2) - (560 // 2), 20, 50, "Potion Brewer", colour1, colour2)
        if checkMouseInsideRect(quitW, quitH, quitX, quitY):
            boxColour = (255,230,180)
        else: 
            boxColour = (255,215,167)
        drawBox(quitW, quitH, quitX, quitY, 50, "X", boxColour, colour2)

        instructionBoxText = ["You have 2 minutes to find as many",
                              "ingredients as you can. GOOOOO!"]
        for toFind in objectsToFind:
            instructionBoxText.append(toFind)
        for found in objectsFound:
            instructionBoxText.append(found)
        instructionBox = pygame.draw.rect(screen, colour2, (instructionBoxX, instructionBoxY, instructionBoxWidth, instructionBoxHeight))
        instructionBoxTextSurface = []
        for lineNo in range(2+len(objectsToFind)+len(objectsFound)):
            if lineNo < 2+len(objectsToFind):
                instructionBoxTextSurface.append(instructionBoxFont.render(instructionBoxText[lineNo], True, colour5))
            else:
                instructionBoxTextSurface.append(instructionBoxFont.render(instructionBoxText[lineNo], True, colour3))
        for line in range(len(instructionBoxTextSurface)):
            screen.blit(instructionBoxTextSurface[line], (instructionBoxX + 25, instructionBoxY+20+(line*instructionBoxFontSize)+(15*line)))
        
        net, classes, colours, cap, objectsToFind, objectsFound = Object_Detection.AnalyseFrame(net, classes, colours, cap, objectsToFind, objectsFound)

        timeInSecs = int(time.time() - startTime)
        drawBox(75, 40, width-75-20, height-40-20, 20, str(120-timeInSecs), colour3, colour2)
        #CHECKING IF ALL OBJECTS HAVE BEEN FOUND
        if len(objectsToFind) == 0:
            timeString = str(int(timeInSecs/60)) + "m " + str(int(timeInSecs % 60)) + "s"
            purpose = random.choice(purposes)
            instructionBoxText = ["It took you " + timeString,
                                  "to brew the full potion.",
                                  "This potion is of the highest possible,",
                                  "quality meaning it will",
                                  purpose]
            state = "roundup"
            pygame.mixer.music.stop()
            buttonSoundAffect.play()
            pygame.mixer.music.load("bubbling.mp3")
            pygame.mixer.music.play(-1)
        #CHECKING FOR TIME UPS
        if timeInSecs >= 120:
            quality = "average"
            purpose = random.choice(purposes)
            sideEffect = random.choice(sideEffects)
            if len(objectsFound) > 5:
                quality = "good"
            elif len(objectsFound) > 4:
                quality = "decent"
            elif len(objectsFound) > 3:
                quality = "average"
            elif len(objectsFound) > 2:
                quality = "poor"
            elif len(objectsFound) > 1:
                quality = "terrible"
            elif len(objectsFound) > 0:
                quality = "horrific"
            else:
                quality = "non-existent"
                sideEffect = "not doing anything."
                
            instructionBoxText = ["You had 2 minutes to brew your potion.",
                                  "You managed to add " + str(len(objectsFound)) + " ingredients",
                                  "to your potion, resulting in a " + quality,
                                  "potion. This potion was supposed to",
                                  purpose,
                                  "However due to its quality it may",
                                  "have a side effect of",
                                  sideEffect]
            state = "roundup"
            pygame.mixer.music.stop()
            buttonSoundAffect.play()
            pygame.mixer.music.load("bubbling.mp3")
            pygame.mixer.music.play(-1)
            
        pygame.display.update()
        
    elif state == "roundup":
        Object_Detection.EndObjectDetection(cap)
        #INTERACTIVITY
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QuitGame()
                break
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if checkMouseInsideRect(quitW, quitH, quitX, quitY):
                    QuitGame()
                    break
                if checkMouseInsideRect(startW, startH, startX, startY): 
                    state = "menu"
                    buttonSoundAffect.play()
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("atmosphere.mp3")
                    pygame.mixer.music.play(-1)
                           
        screen.fill(colour4)
        drawBox(560, 50, (width // 2) - (560 // 2), 20, 50, "Potion Brewer", colour2, colour4)
        if checkMouseInsideRect(quitW, quitH, quitX, quitY):
            boxColour = (255,230,180)
        else: 
            boxColour = (255,215,167)
        drawBox(quitW, quitH, quitX, quitY, 50, "X", boxColour, colour2)

        #START BUTTON
        if checkMouseInsideRect(startW, startH, startX, startY): 
            boxColour = (255,230,180)
        else: 
            boxColour = (255,215,167)
        drawBox(startW, startH, startX, startY, 65, "BACK TO MENU", boxColour, colour1)

        instructionBox = pygame.draw.rect(screen, colour2, (instructionBoxX, instructionBoxY, instructionBoxWidth, instructionBoxHeight))
        instructionBoxTextSurface = []
        for line in instructionBoxText: 
            instructionBoxTextSurface.append(instructionBoxFont.render(line, True, colour5))
        for line in range(len(instructionBoxTextSurface)):
            screen.blit(instructionBoxTextSurface[line], (instructionBoxX + 25, instructionBoxY+20+(line*instructionBoxFontSize)+(15*line)))

        pygame.display.update()
        
    elif state == "quit":
        QuitGame()
        break
