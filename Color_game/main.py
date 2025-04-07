import random, sys, time, pygame
from pygame.locals import K_q, K_w, K_e, K_a, K_s, K_d, QUIT, KEYDOWN, KEYUP, MOUSEBUTTONUP, K_ESCAPE
import pyttsx3
import threading  # Import threading
import queue  # To handle queued voiceover tasks

# Initialize the pyttsx3 engine
engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 25)

# Queue to store voiceover tasks
voiceover_queue = queue.Queue()

# Thread to process voiceover tasks
def processVoiceOvers():
    while True:
        key = voiceover_queue.get()  # Get the next voiceover task
        if key is None:  # None is used as a signal to stop the thread
            break
        
        if key == YELLOW:
            engine.say("Q")
        elif key == BLUE:
            engine.say("W")
        elif key == RED:
            engine.say("A")
        elif key == GREEN:
            engine.say("S")
        elif key == ORANGE:
            engine.say("E")
        elif key == PURPLE:
            engine.say("D")
        
        engine.runAndWait()

# Start the voiceover processing thread once at the beginning
voiceover_thread = threading.Thread(target=processVoiceOvers, daemon=True)
voiceover_thread.start()

FPS = 30
WINDOWWIDTH = 700
WINDOWHEIGHT = 550
FLASHSPEED = 500  # in milliseconds
FLASHDELAY = 200  # in milliseconds
BUTTONSIZE = 200
BUTTONGAPSIZE = 20

#                R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BRIGHTRED = (255, 0, 0)
RED = (155, 0, 0)
BRIGHTGREEN = (0, 255, 0)
GREEN = (0, 155, 0)
BRIGHTBLUE = (0, 0, 255)
BLUE = (0, 0, 155)
BRIGHTYELLOW = (255, 255, 0)
YELLOW = (155, 155, 0)
BRIGHTORANGE = (255, 140, 0)
ORANGE = (175, 60, 0)
DARKGRAY = (40, 40, 40)
PURPLE = (68, 0 , 68)
BRIGHTPURPLE = (128, 0, 128)

bgColor = BLACK

XMARGIN = int((WINDOWWIDTH - (3 * BUTTONSIZE) - 2 * BUTTONGAPSIZE) / 2)
TOPMARGIN = 50
YMARGIN = TOPMARGIN

# Rect objects for each of the five buttons
YELLOWRECT = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
BLUERECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
REDRECT = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
GREENRECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
ORANGERECT = pygame.Rect(XMARGIN + 2 * (BUTTONSIZE + BUTTONGAPSIZE), YMARGIN, BUTTONSIZE, BUTTONSIZE)
PURPLERECT = pygame.Rect(XMARGIN + 2 * (BUTTONSIZE + BUTTONGAPSIZE), YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)

def getButtonClicked(x, y):
    if YELLOWRECT.collidepoint( (x, y) ):
        return YELLOW
    elif BLUERECT.collidepoint( (x, y) ):
        return BLUE
    elif REDRECT.collidepoint( (x, y) ):
        return RED
    elif GREENRECT.collidepoint( (x, y) ):
        return GREEN
    elif ORANGERECT.collidepoint( (x, y) ):
        return ORANGE
    elif PURPLERECT.collidepoint( (x, y) ):
        return PURPLE
    return None

# Define the flashButtonAnimation function first, before main
def flashButtonAnimation(color, animationSpeed=50):
    if color == YELLOW:
        flashColor = BRIGHTYELLOW
        rectangle = YELLOWRECT
    elif color == BLUE:
        flashColor = BRIGHTBLUE
        rectangle = BLUERECT
    elif color == RED:
        flashColor = BRIGHTRED
        rectangle = REDRECT
    elif color == GREEN:
        flashColor = BRIGHTGREEN
        rectangle = GREENRECT
    elif color == ORANGE:
        flashColor = BRIGHTORANGE
        rectangle = ORANGERECT
    elif color == PURPLE:
        flashColor = BRIGHTPURPLE
        rectangle = PURPLERECT

    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface((BUTTONSIZE, BUTTONSIZE))
    flashSurf = flashSurf.convert_alpha()
    r, g, b = flashColor
    voiceover_queue.put(color)
    # Flash animation loop
    for start, end, step in ((0, 255, 1), (255, 0, -1)):  # animation loop
        for alpha in range(start, end, animationSpeed * step):
            checkForQuit()
            pygame.time.delay(75)
            DISPLAYSURF.blit(origSurf, (0, 0))
            flashSurf.fill((r, g, b, alpha))
            DISPLAYSURF.blit(flashSurf, rectangle.topleft)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    DISPLAYSURF.blit(origSurf, (0, 0))

# Define checkForQuit function before main
def checkForQuit():
    for event in pygame.event.get(QUIT):  # get all the QUIT events
        terminate()  # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP):  # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate()  # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event)  # put the other KEYUP event objects back

def drawButtons():
    pygame.draw.rect(DISPLAYSURF, YELLOW, YELLOWRECT)
    pygame.draw.rect(DISPLAYSURF, BLUE, BLUERECT)
    pygame.draw.rect(DISPLAYSURF, RED, REDRECT)
    pygame.draw.rect(DISPLAYSURF, GREEN, GREENRECT)
    pygame.draw.rect(DISPLAYSURF, ORANGE, ORANGERECT)
    pygame.draw.rect(DISPLAYSURF, PURPLE, PURPLERECT)

#animation for game over
def gameOverAnimation(color=WHITE, animationSpeed=50):
    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface(DISPLAYSURF.get_size())
    flashSurf = flashSurf.convert_alpha()
    r, g, b = color
    for i in range(3): # do the flash 3 times
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            for alpha in range(start, end, animationSpeed * step): # animation loop
                # alpha = transparency
                checkForQuit()
                flashSurf.fill((r, g, b, alpha))
                DISPLAYSURF.blit(origSurf, (0, 0))
                DISPLAYSURF.blit(flashSurf, (0, 0))
                drawButtons()
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Simulate')

    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
    infoSurf = BASICFONT.render('Match the pattern by clicking on the button or using the Q, W, E, A, S, D keys.', 1, WHITE)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINDOWHEIGHT - 25)

    pattern = []
    currentStep = 0
    lastClickTime = 0
    score = 0
    # when False, the pattern is playing. when True, waiting for the player to click a colored button:
    waitingForInput = False

    while True:  # main game loop
        clickedButton = None  # button that was clicked (set to YELLOW, RED, GREEN, BLUE, ORANGE)
        DISPLAYSURF.fill(bgColor)
        drawButtons()
        scoreSurf = BASICFONT.render('Score: ' + str(score), 1, WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 100, 10)
        DISPLAYSURF.blit(scoreSurf, scoreRect)

        DISPLAYSURF.blit(infoSurf, infoRect)

        checkForQuit()
        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey)
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    clickedButton = YELLOW
                elif event.key == K_w:
                    clickedButton = BLUE
                elif event.key == K_a:
                    clickedButton = RED
                elif event.key == K_s:
                    clickedButton = GREEN
                elif event.key == K_e:
                    clickedButton = ORANGE
                elif event.key == K_d:
                    clickedButton = PURPLE

        if not waitingForInput:
            # play the pattern
            pygame.display.update()
            pygame.time.delay(1000)  # Use delay instead of wait
            pattern.append(random.choice((YELLOW, BLUE, RED, GREEN, ORANGE)))  # Include orange
            for button in pattern:
                flashButtonAnimation(button)
                pygame.time.delay(FLASHDELAY)
            waitingForInput = True
        else:
            # wait for the player to enter buttons
            if clickedButton is not None and clickedButton == pattern[currentStep]:
                # pushed the correct button
                flashButtonAnimation(clickedButton)
                currentStep += 1
                lastClickTime = time.time()

                if currentStep == len(pattern):
                    # pushed the last button in the pattern
                    score += 1
                    waitingForInput = False
                    currentStep = 0  # reset back to first step

            elif (clickedButton is not None and clickedButton != pattern[currentStep]):
                # pushed the incorrect button
                gameOverAnimation()
                # reset the variables for a new game:
                pattern = []
                currentStep = 0
                waitingForInput = False
                score = 0
                pygame.time.delay(1000)  # Use delay instead of wait

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
