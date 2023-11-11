import argparse
import time
import json
import ctypes
from ctypes import wintypes

# Required Windows API Functions
# Function to set cursor position
def set_cursor_pos(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)

# Function to get cursor position
def get_cursor_pos():
    point = ctypes.wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
    return point.x, point.y

def record(filename):
    print("Recording started. Move the mouse around. Press Ctrl + C to stop.")
    positions = []
    try:
        while True:
            x, y = get_cursor_pos()
            positions.append((x, y))
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Recording stopped.")
        with open(filename, 'w') as file:
            json.dump(positions, file)

def replay(filename):
    with open(filename, 'r') as file:
        positions = json.load(file)
        print("Replaying mouse movements...")
        for pos in positions:
            set_cursor_pos(pos[0], pos[1])
            time.sleep(0.1)
        print("Replay complete.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mouse Recorder/Replayer')
    parser.add_argument('command', choices=['record', 'replay'], help='Choose command: record or replay')
    parser.add_argument('--file', default='mouse_actions.json', help='File to save mouse actions (default: mouse_actions.json)')
    args = parser.parse_args()

    if args.command == 'record':
        record(args.file)
    elif args.command == 'replay':
        replay(args.file)
