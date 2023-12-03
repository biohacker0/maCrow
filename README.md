# maCrow
A macro recorder for windows automation

# Mouse Recorder/Replayer

This Python script allows you to record and replay mouse movements, clicks, and keyboard inputs. It uses the pynput library for mouse events and the keyboard library for keyboard events. The recorded actions are saved in a JSON file, which can be later replayed to simulate the recorded input.

## Features

- **Record**: Capture mouse movements, left or right clicks, scrolls , hold & drag , double clicks, and keyboard inputs with multiple key press combo(hotkeys).
- **Replay**: Replay recorded actions to simulate mouse and keyboard behavior.

## Requirements

- Python 3.x
- pynput    - Library to monitor and control input devices.
- pyautogui - Library to programmatically control the mouse and keyboard.
- mouse     - Cross-platform library to control and monitor mouse events.
- keyboard  - Cross-platform library to control and monitor keyboard events.
- tkinter   - Library for creating GUI applications.
- ctypes

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com//biohacker0/maCrow.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Record

To record mouse actions and save them to a file:

```bash
python maCrow.py record --file mouse_actions.json
```

-- While recording, move the mouse, perform actions, and type on the keyboard. Press Ctrl + C to stop recording.

To stop the recording and save them to file:

```bash
Ctrl + C
```

### Replay

To replay mouse actions from a recorded file:

```bash
python maCrow.py replay --file mouse_actions.json
```

-- This will simulate the recorded mouse and keyboard inputs.


### Additional Notes

Adjust the key_delay parameter in the replay function to control the delay between key presses during replay.
Customize the double_click_threshold in the replay function to adjust the threshold for detecting double clicks.

Press `Ctrl + C` to stop the recording.



