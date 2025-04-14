# test_config.py
import pytest
from color_game import config

def test_window_constants():
    assert config.WINDOWWIDTH > 0
    assert config.WINDOWHEIGHT > 0

def test_color_key_map_integrity():
    for color, key in config.COLOR_KEY_MAP.items():
        assert isinstance(key, str)
        assert len(key) == 1

def test_margin_calculation():
    assert config.XMARGIN >= 0
    assert config.YMARGIN >= 0
