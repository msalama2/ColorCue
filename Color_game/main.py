import sys
import pygame
from pygame.locals import *
import random
from sound import *
from config import *

def draw_buttons(surface):
    for color, rect in RECT_MAP.items():
        pygame.draw.rect(surface, color, rect)

def get_button_clicked(x, y):
    for color, rect in RECT_MAP.items():
        if rect.collidepoint((x, y)):
            return color
    return None

def flash_button(surface, color, fpsclock, play_sound=True, speed=50):
    flash_color = COLOR_BRIGHT_MAP[color]
    rect = RECT_MAP[color]
    key = COLOR_KEY_MAP[color]

    if play_sound:
        play_key_sound(key)

    orig_surf = surface.copy()
    flash_surf = pygame.Surface((BUTTONSIZE, BUTTONSIZE)).convert_alpha()
    r, g, b = flash_color

    for start, end, step in ((0, 255, 1), (255, 0, -1)):
        for alpha in range(start, end, speed * step):
            flash_surf.fill((r, g, b, alpha))
            surface.blit(orig_surf, (0, 0))
            surface.blit(flash_surf, rect.topleft)
            pygame.display.update()
            fpsclock.tick(FPS)

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

def main():
    global score, pattern, current_step, waiting_for_input, game_started, tutorial_playing
    score = 0
    pattern = []
    current_step = 0
    waiting_for_input = False
    game_started = False
    tutorial_playing = False

    pygame.init()
    fpsclock = pygame.time.Clock()
    display = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Accessible Pattern Game')
    font = pygame.font.Font(None, 28)
    initialize_game()

    while True:
        clicked = handle_events()
        display.fill(bgColor)
        draw_buttons(display)
        display_score(display, font, score)

        if game_started:
            run_game_logic(display, fpsclock, clicked)

        pygame.display.update()
        fpsclock.tick(FPS)

def initialize_game():
    welcome_sound.play()
    pygame.time.wait(int(welcome_sound.get_length() * 1000))
    listen_tutorial.play()
    pygame.time.wait(int(listen_tutorial.get_length() * 1000))
    startgame_sound.play()
    pygame.time.wait(int(startgame_sound.get_length() * 1000))

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

def handle_keydown(event):
    global tutorial_playing, game_started, pattern, current_step, score, waiting_for_input
    if event.key == K_t:
        tutorial.stop() # Stop the tutorial sound so it doesn't overlap
        tutorial.play() 
        tutorial_playing = True
    elif event.key == K_ESCAPE: # Exit the game if escape is pressed
        pygame.quit()
        sys.exit()
    elif event.key == K_SPACE:
        start_game()
    elif game_started:
        for col, key in COLOR_KEY_MAP.items():
            if event.key == ord(key.lower()):
                return col
    return None

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

def run_game_logic(display, fpsclock, clicked):
    global pattern, current_step, score, waiting_for_input
    if not waiting_for_input:
        generate_pattern(display, fpsclock)
    else:
        process_input(display, fpsclock, clicked)

def generate_pattern(display, fpsclock):
    global pattern, waiting_for_input # Use global variables so we can modify them
    pygame.display.update() 
    pygame.time.wait(1000) # Wait for 1 second
    pattern.append(random.choice(list(COLOR_KEY_MAP.keys()))) # Add a new color to the pattern
    for btn in pattern: # Flash each color in the pattern
        flash_button(display, btn, fpsclock, play_sound=True) # Play sound, flash button
        pygame.time.wait(FLASHDELAY)
    waiting_for_input = True

def process_input(display, fpsclock, clicked):
    global pattern, current_step, score, waiting_for_input
    if clicked:
        if clicked == pattern[current_step]:
            handle_correct_input(display, fpsclock, clicked)
        else:
            handle_incorrect_input(display, fpsclock)

def handle_correct_input(display, fpsclock, clicked):
    global current_step, score, waiting_for_input
    flash_button(display, clicked, fpsclock, play_sound=False)
    correct_chime.play()
    current_step += 1
    if current_step == len(pattern):
        score += 1
        waiting_for_input = False
        current_step = 0

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
