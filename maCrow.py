# import argparse
# import time
# import json
# import ctypes
# from ctypes import wintypes

# # Required Windows API Functions
# # Function to set cursor position
# def set_cursor_pos(x, y):
#     ctypes.windll.user32.SetCursorPos(x, y)

# # Function to get cursor position
# def get_cursor_pos():
#     point = ctypes.wintypes.POINT()
#     ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
#     return point.x, point.y

# def record(filename):
#     print("Recording started. Move the mouse around. Press Ctrl + C to stop.")
#     positions = []
#     try:
#         while True:
#             x, y = get_cursor_pos()
#             positions.append((x, y))
#             time.sleep(0.1)
#     except KeyboardInterrupt:
#         print("Recording stopped.")
#         with open(filename, 'w') as file:
#             json.dump(positions, file)

# def replay(filename):
#     with open(filename, 'r') as file:
#         positions = json.load(file)
#         print("Replaying mouse movements...")
#         for pos in positions:
#             set_cursor_pos(pos[0], pos[1])
#             time.sleep(0.1)
#         print("Replay complete.")

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Mouse Recorder/Replayer')
#     parser.add_argument('command', choices=['record', 'replay'], help='Choose command: record or replay')
#     parser.add_argument('--file', default='mouse_actions.json', help='File to save mouse actions (default: mouse_actions.json)')
#     args = parser.parse_args()

#     if args.command == 'record':
#         record(args.file)
#     elif args.command == 'replay':
#         replay(args.file)


# import argparse
# import time
# import json
# import win32api
# import win32con
# import win32gui

# def record(filename):
#     print("Recording started. Move the mouse around and perform actions. Press Ctrl + C to stop.")
#     actions = []
#     try:
#         while True:
#             x, y = win32api.GetCursorPos()
#             left_click = win32api.GetKeyState(win32con.VK_LBUTTON) & 0x80 != 0
#             right_click = win32api.GetKeyState(win32con.VK_RBUTTON) & 0x80 != 0
#             double_click = win32api.GetKeyState(0x06) & 0x1 != 0
#             wheel = win32api.GetKeyState(win32con.VK_XBUTTON1) & 0x80 != 0
#             actions.append({"position": (x, y), "left_click": left_click, "right_click": right_click, "double_click": double_click, "wheel": wheel})
#             time.sleep(0.1)
#     except KeyboardInterrupt:
#         print("Recording stopped.")
#         with open(filename, 'w') as file:
#             json.dump(actions, file)

# def replay(filename):
#     with open(filename, 'r') as file:
#         actions = json.load(file)
#         print("Replaying mouse movements...")
#         for action in actions:
#             win32api.SetCursorPos(action["position"])
#             if action["left_click"]:
#                 win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
#                 win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
#             if action["right_click"]:
#                 win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
#                 win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
#             if action["double_click"]:
#                 win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
#                 win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
#                 time.sleep(0.05)
#                 win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
#                 win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
#             if action["wheel"]:
#                 win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, win32con.WHEEL_DELTA * 2, 0)
#             time.sleep(0.1)
#         print("Replay complete.")

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Mouse Recorder/Replayer')
#     parser.add_argument('command', choices=['record', 'replay'], help='Choose command: record or replay')
#     parser.add_argument('--file', default='mouse_actions.json', help='File to save mouse actions (default: mouse_actions.json)')
#     args = parser.parse_args()

#     if args.command == 'record':
#         record(args.file)
#     elif args.command == 'replay':
#         replay(args.file)


import argparse
import time
import json
import win32api
import win32con

def record(filename):
    print("Recording started. Move the mouse around and perform actions. Press Ctrl + C to stop.")
    actions = []
    try:
        while True:
            x, y = win32api.GetCursorPos()
            left_click = win32api.GetKeyState(win32con.VK_LBUTTON) < 0
            right_click = win32api.GetKeyState(win32con.VK_RBUTTON) < 0
            wheel = win32api.GetKeyState(win32con.VK_MBUTTON) < 0
            
            scroll_up = win32api.GetKeyState(win32con.VK_XBUTTON1) < 0
            scroll_down = win32api.GetKeyState(win32con.VK_XBUTTON2) < 0

            actions.append({
                "time": time.time(),
                "position": (x, y),
                "left_click": left_click,
                "right_click": right_click,
                "wheel": wheel,
                "scroll_up": scroll_up,
                "scroll_down": scroll_down
            })
            time.sleep(0.05)  # Decreased sleep time for more frequent captures
    except KeyboardInterrupt:
        print("Recording stopped.")
        with open(filename, 'w') as file:
            json.dump(actions, file)


def replay(filename):
    with open(filename, 'r') as file:
        actions = json.load(file)
        print("Replaying mouse movements...")
        start_time = actions[0]["time"]
        for action in actions:
            time.sleep(action["time"] - start_time)  # Adjust sleep based on time difference for a more accurate replay
            start_time = action["time"]
            win32api.SetCursorPos(action["position"])
            if action["left_click"]:
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            if action["right_click"]:
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
            if action["scroll_up"]:
                # Perform some action to simulate scroll up
                pass
            if action["scroll_down"]:
                # Perform some action to simulate scroll down
                pass
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