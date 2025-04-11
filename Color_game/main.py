import random
import sys
import pygame
from pygame.locals import *
import pyttsx3


# Initialize the TTS engine and set a slightly slower speech rate for clarity
engine = pyttsx3.init()
engine.setProperty('rate', engine.getProperty('rate') - 25)

# Initialize pygame mixer for sound effects
pygame.mixer.init()

# Load background music and sound effects
welcome_sound = pygame.mixer.Sound("assets/tutorial/welcome_to_colorcue.mp3")  # Welcome sound
listen_tutorial = pygame.mixer.Sound("assets/tutorial/listen_tutorial_sound.mp3")  # Listen tutorial sound
startgame_sound = pygame.mixer.Sound("assets/tutorial/start_game_sound.mp3")  # Start game sound

pygame.mixer.music.load("assets/music/Moog City.mp3")  # Background music
tutorial = pygame.mixer.Sound("assets/tutorial/tutorial.mp3")  # Tutorial sound

correct_chime = pygame.mixer.Sound("assets/sounds/correct_sound.wav")  # Correct sound
incorrect_chime = pygame.mixer.Sound("assets/sounds/incorrect_sound.mp3")  # Incorrect sound
a_sound = pygame.mixer.Sound("assets/sounds/a_sound.mp3")  # A sound
d_sound = pygame.mixer.Sound("assets/sounds/d_sound.mp3")  # D sound
e_sound = pygame.mixer.Sound("assets/sounds/e_sound.mp3")  # E sound
s_sound = pygame.mixer.Sound("assets/sounds/s_sound.mp3")  # S sound
q_sound = pygame.mixer.Sound("assets/sounds/q_sound.mp3")  # Q sound
w_sound = pygame.mixer.Sound("assets/sounds/w_sound.mp3")  # W sound

gameover_sound = pygame.mixer.Sound("assets/sounds/gameover_sound.mp3")  # Game over sound

# Keep this for now. We might need to use it later to say the score 
def speak(text):
    engine.say(text)
    engine.runAndWait() 

# Constants
FPS = 30
WINDOWWIDTH = 700
WINDOWHEIGHT = 550
FLASHSPEED = 500  # milliseconds for button flash animation
FLASHDELAY = 200  # delay between flashes in milliseconds
BUTTONSIZE = 200
BUTTONGAPSIZE = 20

# Define RGB color constants
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
BRIGHTPURPLE = (128, 0, 128)
PURPLE = (68, 0, 68)

bgColor = BLACK
XMARGIN = int((WINDOWWIDTH - (3 * BUTTONSIZE) - 2 * BUTTONGAPSIZE) / 2)
YMARGIN = 50

# COLOR Mappings
COLOR_KEY_MAP = {
    YELLOW: 'Q', 
    BLUE: 'W', 
    RED: 'E', 
    GREEN: 'A', 
    ORANGE: 'S', 
    PURPLE: 'D'
}
# Bright color mappings for flashing
COLOR_BRIGHT_MAP = {
    YELLOW: BRIGHTYELLOW, 
    BLUE: BRIGHTBLUE, 
    RED: BRIGHTRED,
    GREEN: BRIGHTGREEN, 
    ORANGE: BRIGHTORANGE, 
    PURPLE: BRIGHTPURPLE
}
# Rectangles for each button
RECT_MAP = {
    YELLOW: pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE),
    BLUE: pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE),
    RED: pygame.Rect(XMARGIN + 2 * (BUTTONSIZE + BUTTONGAPSIZE), YMARGIN, BUTTONSIZE, BUTTONSIZE),
    GREEN: pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE),
    ORANGE: pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE),
    PURPLE: pygame.Rect(XMARGIN + 2 * (BUTTONSIZE + BUTTONGAPSIZE), YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
}

# Utility Functions 
def draw_buttons(surface):
    for color, rect in RECT_MAP.items():
        pygame.draw.rect(surface, color, rect)

# Function to get the color of the clicked button
def get_button_clicked(x, y):
    for color, rect in RECT_MAP.items():
        if rect.collidepoint((x, y)):
            return color
    return None

# Function to animate the button flash
def flash_button(surface, color, fpsclock, play_sound = True, speed=50):
    flash_color = COLOR_BRIGHT_MAP[color]
    rect = RECT_MAP[color]
    key = COLOR_KEY_MAP[color]

    if play_sound :
        play_key_sound(key) # Play the sound associated with the key
    
    # Create a surface for the flash effect
    orig_surf = surface.copy()
    flash_surf = pygame.Surface((BUTTONSIZE, BUTTONSIZE)).convert_alpha()
    r, g, b = flash_color

    # Flash animation
    for start, end, step in ((0, 255, 1), (255, 0, -1)):
        for alpha in range(start, end, speed * step):
            flash_surf.fill((r, g, b, alpha))
            surface.blit(orig_surf, (0, 0))
            surface.blit(flash_surf, rect.topleft)
            pygame.display.update()
            fpsclock.tick(FPS)

# Function to animate game over
def game_over_animation(surface, fpsclock, color=WHITE, speed=50):
    orig_surf = surface.copy()
    flash_surf = pygame.Surface(surface.get_size()).convert_alpha()
    r, g, b = color
    for _ in range(3):
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            for alpha in range(start, end, speed * step):
                flash_surf.fill((r, g, b, alpha))
                surface.blit(orig_surf, (0, 0))
                surface.blit(flash_surf, (0, 0))
                draw_buttons(surface)
                pygame.display.update()
                fpsclock.tick(FPS)

# Function to play the sound associated with a key
def play_key_sound(key):
    key = key.upper()
    if key == 'A':
        a_sound.play()
    elif key == 'D':
        d_sound.play()
    elif key == 'E':
        e_sound.play()
    elif key == 'S':
        s_sound.play()
    elif key == 'Q':
        q_sound.play()
    elif key == 'W':
        w_sound.play()

# Main Game Function
def main():
    # Initialize game state variables
    global score, pattern, current_step, waiting_for_input, game_started, tutorial_playing
    score = 0
    pattern = []
    current_step = 0
    waiting_for_input = False
    game_started = False
    tutorial_playing = False

    # Initialize pygame
    pygame.init()
    fpsclock = pygame.time.Clock()
    display = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Accessible Pattern Game')
    font = pygame.font.Font(None, 28)
    initialize_game()
    
    # Main game loop
    while True:
        clicked = handle_events()
        display.fill(bgColor)
        draw_buttons(display)
        display_score(display, font, score)

        if game_started:
            run_game_logic(display, fpsclock, clicked)

        pygame.display.update()
        fpsclock.tick(FPS)

# Function to initialize the game
def initialize_game():
    welcome_sound.play()
    pygame.time.wait(int(welcome_sound.get_length() * 1000))
    listen_tutorial.play()
    pygame.time.wait(int(listen_tutorial.get_length() * 1000))
    startgame_sound.play()
    pygame.time.wait(int(startgame_sound.get_length() * 1000))

# Function to handle events
def handle_events():
    global tutorial_playing, game_started, pattern, current_step, score, waiting_for_input
    clicked = None
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONUP:
            clicked = get_button_clicked(*event.pos)
        elif event.type == KEYDOWN:
            clicked = handle_keydown(event)
    return clicked

# Function to handle keydown events
def handle_keydown(event):
    global tutorial_playing, game_started, pattern, current_step, score, waiting_for_input
    if event.key == K_t:
        tutorial.play()
        tutorial_playing = True
    elif event.key == K_SPACE:
        start_game()
    elif game_started:
        for col, key in COLOR_KEY_MAP.items():
            if event.key == ord(key.lower()):
                return col
    return None

# Function to start the game
def start_game():
    global tutorial_playing, game_started, pattern, current_step, score, waiting_for_input
    if tutorial_playing:
        tutorial.stop()
        tutorial_playing = False
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1, 0.0)
    game_started = True
    waiting_for_input = False
    pattern = []
    current_step = 0
    score = 0

# Function to display the score
def display_score(display, font, score):
    score_surf = font.render(f"Score: {score}", True, WHITE)
    display.blit(score_surf, (WINDOWWIDTH - 120, 10))

# Function to run the game logic
def run_game_logic(display, fpsclock, clicked):
    global pattern, current_step, score, waiting_for_input
    if not waiting_for_input:
        generate_pattern(display, fpsclock)
    else:
        process_input(display, fpsclock, clicked)

# Function to generate the pattern
def generate_pattern(display, fpsclock):
    global pattern, waiting_for_input
    pygame.display.update()
    pygame.time.wait(1000)
    pattern.append(random.choice(list(COLOR_KEY_MAP.keys())))
    for btn in pattern:
        flash_button(display, btn, fpsclock, play_sound=True)
        pygame.time.wait(FLASHDELAY)
    waiting_for_input = True

# Function to process user input
def process_input(display, fpsclock, clicked):
    global pattern, current_step, score, waiting_for_input
    if clicked:
        if clicked == pattern[current_step]:
            handle_correct_input(display, fpsclock, clicked)
        else:
            handle_incorrect_input(display, fpsclock)

# Function to handle correct user input
def handle_correct_input(display, fpsclock, clicked):
    global current_step, score, waiting_for_input
    flash_button(display, clicked, fpsclock, play_sound=False)
    correct_chime.play()
    current_step += 1
    if current_step == len(pattern):
        score += 1
        waiting_for_input = False
        current_step = 0

# Function to handle incorrect user input
def handle_incorrect_input(display, fpsclock):
    global pattern, current_step, score, waiting_for_input
    incorrect_chime.play()
    gameover_sound.play()
    game_over_animation(display, fpsclock)
    pattern = []
    current_step = 0
    waiting_for_input = False
    score = 0
    pygame.time.wait(2000)

if __name__ == '__main__':
    main()