import unittest
from unittest.mock import patch
from io import StringIO
import os
import json

from maCrow import record, replay, count_down_animation_config


class TestMouseKeyboardRecorder(unittest.TestCase):

    def test_record_and_replay(self):
        test_file = 'test_actions.json'

        # Record actions
        with patch('builtins.input', return_value='record'):
            with patch('sys.argv', ['script_name.py', 'record', '--file', test_file]):
                count_down_animation_config('record')
                record(test_file)

        # Replay actions
        with patch('builtins.input', return_value='replay'):
            with patch('sys.argv', ['script_name.py', 'replay', '--file', test_file]):
                count_down_animation_config('replay')
                replay(test_file)

        # Assert that the test file is created and not empty
        self.assertTrue(os.path.exists(test_file))
        self.assertGreater(os.path.getsize(test_file), 0)

        # Clean up the test file
        os.remove(test_file)

    def test_record_invalid_file(self):
        # Attempt to record with an invalid file name
        with patch('builtins.input', return_value='record'):
            with patch('sys.argv', ['script_name.py', 'record', '--file', 'invalid file name']):
                with self.assertRaises(SystemExit):
                    count_down_animation_config('record')
                    record('invalid file name')

    def test_replay_invalid_file(self):
        # Attempt to replay with an invalid file name
        with patch('builtins.input', return_value='replay'):
            with patch('sys.argv', ['script_name.py', 'replay', '--file', 'invalid file name']):
                with self.assertRaises(SystemExit):
                    count_down_animation_config('replay')
                    replay('invalid file name')


if __name__ == '__main__':
    unittest.main()
