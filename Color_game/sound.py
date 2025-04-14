import pyttsx3
import pygame

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', engine.getProperty('rate') - 25)

# Sound loading
pygame.mixer.init()
welcome_sound = pygame.mixer.Sound("assets/tutorial/welcome_to_colorcue.mp3")
listen_tutorial = pygame.mixer.Sound("assets/tutorial/listen_tutorial_sound.mp3")
startgame_sound = pygame.mixer.Sound("assets/tutorial/start_game_sound.mp3")
tutorial = pygame.mixer.Sound("assets/tutorial/tutorial.mp3")
pygame.mixer.music.load("assets/music/Moog City.mp3")

correct_chime = pygame.mixer.Sound("assets/sounds/correct_sound.wav")
incorrect_chime = pygame.mixer.Sound("assets/sounds/incorrect_sound.mp3")
a_sound = pygame.mixer.Sound("assets/sounds/a_sound.mp3")
d_sound = pygame.mixer.Sound("assets/sounds/d_sound.mp3")
e_sound = pygame.mixer.Sound("assets/sounds/e_sound.mp3")
s_sound = pygame.mixer.Sound("assets/sounds/s_sound.mp3")
q_sound = pygame.mixer.Sound("assets/sounds/q_sound.mp3")
w_sound = pygame.mixer.Sound("assets/sounds/w_sound.mp3")
gameover_sound = pygame.mixer.Sound("assets/sounds/gameover_sound.mp3")

# Functions
def speak(text):
    engine.say(text)
    engine.runAndWait()

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
