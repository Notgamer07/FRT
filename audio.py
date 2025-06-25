import pygame
from datahandle import get_gameState

__all__ = ['play','play_background_music','update_state']

play_sound = True
play_music = True

def update_state():
    global play_music,play_sound
    setting = get_gameState()
    if setting['Sound'] == 0:
        play_sound = False
    if setting['Music'] == 0:
        play_music = False

pygame.mixer.init()

pygame.mixer.music.load("audio/level-up-89823.mp3")  # music is for longer tracks
eventSong = pygame.mixer.Sound("audio/game-level-complete-143022.mp3")
eventSong.set_volume(0.4)
channel = eventSong.play()
channel.stop()

def play_background_music():
    if not play_music:
        return
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(loops=-1,start=0.0,fade_ms=50)

def play(sfx):
    if not play_sound:
        return
    if sfx in ["ScoreUp", "Score Up","scoreup"]:
        if channel.get_busy():
            channel.stop()
            channel.play(eventSong)
        else:
            channel.play(eventSong)