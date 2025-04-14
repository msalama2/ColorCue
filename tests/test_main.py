import unittest
from unittest.mock import patch
import pygame
from color_game import main
from color_game import config

class TestMainGame(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.display = pygame.display.set_mode((config.WINDOWWIDTH, config.WINDOWHEIGHT))
        self.fpsclock = pygame.time.Clock()

    def test_get_button_clicked_valid(self):
        # Pick a point inside the first button rect
        color = main.get_button_clicked(config.RECT_MAP[config.YELLOW].centerx,
                                        config.RECT_MAP[config.YELLOW].centery)
        self.assertEqual(color, config.YELLOW)

    def test_get_button_clicked_invalid(self):
        # Point outside all buttons
        self.assertIsNone(main.get_button_clicked(0, 0))

    @patch('main.play_key_sound')
    def test_flash_button_runs(self, mock_play_key_sound):
        try:
            main.flash_button(self.display, config.YELLOW, self.fpsclock, play_sound=True, speed=255)
            self.assertTrue(mock_play_key_sound.called)
        except Exception as e:
            self.fail(f"flash_button raised exception: {e}")

    def test_display_score_does_not_crash(self):
        font = pygame.font.Font(None, 28)
        try:
            main.display_score(self.display, font, 5)
        except Exception as e:
            self.fail(f"display_score raised exception: {e}")

    def test_handle_correct_input_increments(self):
        main.current_step = 0
        main.score = 0
        main.waiting_for_input = True
        main.pattern = [config.YELLOW]
        main.handle_correct_input(self.display, self.fpsclock, config.YELLOW)
        self.assertEqual(main.current_step, 1)
        self.assertEqual(main.score, 0)  # Not yet completed pattern

    def test_handle_incorrect_input_resets(self):
        main.pattern = [config.YELLOW]
        main.current_step = 0
        main.score = 5
        main.waiting_for_input = True
        main.handle_incorrect_input(self.display, self.fpsclock)
        self.assertEqual(main.pattern, [])
        self.assertEqual(main.current_step, 0)
        self.assertEqual(main.score, 0)

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
