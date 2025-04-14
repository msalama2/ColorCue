# test_audio.py
import pytest
from unittest.mock import patch
from color_game import sound as audio

def test_speak_function():
    with patch.object(audio.engine, 'say') as mock_say, \
         patch.object(audio.engine, 'runAndWait') as mock_run:
        audio.speak("Hello")
        mock_say.assert_called_once_with("Hello")
        mock_run.assert_called_once()

def test_play_key_sound_valid_key():
    with patch.object(audio.sounds['a'], 'play') as mock_play:
        audio.play_key_sound('a')
        mock_play.assert_called_once()

def test_play_key_sound_invalid_key():
    assert audio.play_key_sound('z') is None
