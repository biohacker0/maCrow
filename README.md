# maCrow
A macro recorder for windows automation

# Mouse Recorder/Replayer

This Python script allows you to record and replay mouse movements and actions.

## Features

- **Record**: Capture mouse movements, clicks, and scrolls.
- **Replay**: Replay recorded actions to simulate mouse behavior.

## Requirements

- Python 3.x
- pynput
- pyautogui
- mouse
- ctypes
- tkinter

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

### Replay

To replay mouse actions from a recorded file:

```bash
python maCrow.py replay --file mouse_actions.json
```

### Additional Notes

Adjust the `double_click_threshold` variable in the script to suit your scenario.

Press `Ctrl + C` to stop the recording.



