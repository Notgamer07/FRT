import pygame

__all__ = ['play','play_background_music']

pygame.mixer.init()

pygame.mixer.music.load("audio/level-up-89823.mp3")  # music is for longer tracks
eventSong = pygame.mixer.Sound("audio/game-level-complete-143022.mp3")
eventSong.set_volume(0.4)
channel = eventSong.play()
channel.stop()
def play_background_music():
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(loops=-1,start=0.0,fade_ms=50)

def play(sfx):
    if sfx in ["ScoreUp", "Score Up","scoreup"]:
        if channel.get_busy():
            channel.stop()
            channel.play(eventSong)
        else:
            channel.play(eventSong)