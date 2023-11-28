# import time
# import json
# import argparse
# from pynput import mouse as pynput_mouse, keyboard as pynput_keyboard
# import pyautogui
# import mouse
# import ctypes

# # Get screen resolution
# screen_width, screen_height = pyautogui.size()

# # Function to set the cursor position using the Windows API
# def set_cursor_pos(x, y):
#     ctypes.windll.user32.SetCursorPos(x, y)

# # Mapping for special keys
# SPECIAL_KEYS_MAPPING = {
#     pynput_keyboard.Key.alt: 'alt',
#     pynput_keyboard.Key.alt_gr: 'alt_gr',
#     pynput_keyboard.Key.alt_l: 'alt_l',
#     pynput_keyboard.Key.alt_r: 'alt_r',
#     pynput_keyboard.Key.backspace: 'backspace',
#     pynput_keyboard.Key.caps_lock: 'caps_lock',
#     pynput_keyboard.Key.cmd: 'cmd',
#     pynput_keyboard.Key.cmd_l: 'cmd_l',
#     pynput_keyboard.Key.cmd_r: 'cmd_r',
#     pynput_keyboard.Key.ctrl: 'ctrl',
#     pynput_keyboard.Key.ctrl_l: 'ctrl_l',
#     pynput_keyboard.Key.ctrl_r: 'ctrl_r',
#     pynput_keyboard.Key.delete: 'delete',
#     pynput_keyboard.Key.down: 'down',
#     pynput_keyboard.Key.end: 'end',
#     pynput_keyboard.Key.enter: 'enter',
#     pynput_keyboard.Key.esc: 'esc',
#     pynput_keyboard.Key.f1: 'f1',
#     pynput_keyboard.Key.home: 'home',
#     pynput_keyboard.Key.insert: 'insert',
#     pynput_keyboard.Key.left: 'left',
#     pynput_keyboard.Key.media_next: 'media_next',
#     pynput_keyboard.Key.media_play_pause: 'media_play_pause',
#     pynput_keyboard.Key.media_previous: 'media_previous',
#     pynput_keyboard.Key.media_volume_down: 'media_volume_down',
#     pynput_keyboard.Key.media_volume_mute: 'media_volume_mute',
#     pynput_keyboard.Key.media_volume_up: 'media_volume_up',
#     pynput_keyboard.Key.menu: 'menu',
#     pynput_keyboard.Key.num_lock: 'num_lock',
#     pynput_keyboard.Key.page_down: 'page_down',
#     pynput_keyboard.Key.page_up: 'page_up',
#     pynput_keyboard.Key.pause: 'pause',
#     pynput_keyboard.Key.print_screen: 'print_screen',
#     pynput_keyboard.Key.right: 'right',
#     pynput_keyboard.Key.scroll_lock: 'scroll_lock',
#     pynput_keyboard.Key.shift: 'shift',
#     pynput_keyboard.Key.shift_l: 'shift_l',
#     pynput_keyboard.Key.shift_r: 'shift_r',
#     pynput_keyboard.Key.space: 'space',
#     pynput_keyboard.Key.tab: 'tab',
#     pynput_keyboard.Key.up: 'up'
# }

# def record(filename):
#     print("Recording started. Move the mouse around and perform actions. Press Ctrl + C to stop.")
#     actions = []
#     previous_time = time.time()  # Initialize previous_time

#     # Initialize the mouse listener for scroll and press events
#     def on_move(x, y):
#         if 0 <= x < screen_width and 0 <= y < screen_height:
#             actions.append({
#                 "action": "move",
#                 "position": (x, y),
#                 "time_diff": time_diff
#             })

#     def on_click(x, y, button, pressed):
#         if 0 <= x < screen_width and 0 <= y < screen_height:
#             actions.append({
#                 "action": "press" if pressed else "release",
#                 "button": str(button),
#                 "position": (x, y),
#                 "time_diff": time_diff
#             })

#     def on_scroll(x, y, dx, dy):
#         if 0 <= x < screen_width and 0 <= y < screen_height:
#             actions.append({
#                 "action": "scroll",
#                 "position": (x, y),
#                 "scroll": dy,
#                 "time_diff": time_diff
#             })

#     def on_key_release(key):
#         action = {
#             "action": "key_release",
#             "key": None
#         }

#         # Try to get the character of the key
#         try:
#             action["key"] = key.char
#         except AttributeError:
#             # If it's not a character key, use the predefined values from pynput.keyboard.Key
#             if key in SPECIAL_KEYS_MAPPING:
#                 action["key"] = SPECIAL_KEYS_MAPPING[key]
#             else:
#                 action["key"] = str(key)

#         actions.append(action)

#     mouse_listener = pynput_mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
#     mouse_listener.start()

#     keyboard_listener = pynput_keyboard.Listener(on_release=on_key_release)
#     keyboard_listener.start()

#     try:
#         while True:
#             current_time = time.time()
#             time_diff = current_time - previous_time

#             # Get the current mouse position
#             x, y = mouse.get_position()

#             # Keep the mouse within the screen boundaries
#             x = max(0, min(x, screen_width - 1))
#             y = max(0, min(y, screen_height - 1))
            
#             set_cursor_pos(x, y)

#             time.sleep(0.05)  # Adjusted sleep time for smoother recordings

#     except KeyboardInterrupt:
#         print("Recording stopped.")
#         mouse_listener.stop()
#         keyboard_listener.stop()
#         with open(filename, 'w') as file:
#             json.dump(actions, file)

# # Function to replay mouse and keyboard actions
# def replay(filename):
#     with open(filename, 'r') as file:
#         actions = json.load(file)
#         print("Replaying mouse and keyboard movements...")

#         # Variables for double click detection
#         last_click_time = 0
#         double_click_threshold = 0.3  # Adjust this threshold as needed for your scenario

#         for i in range(len(actions)):
#             action = actions[i]
#             if action["action"] == "move":
#                 # Use mouse.move for smooth movement at normal speed
#                 mouse.move(action["position"][0], action["position"][1], absolute=True, duration=0.01)
#             elif action["action"] == "press":
#                 current_time = action["time_diff"]

#                 # Check for double click
#                 if current_time - last_click_time <= double_click_threshold:
#                     if action["button"] == "Button.left":
#                         pyautogui.mouseDown(button='left')
#                         print("double click")
#                     elif action["button"] == "Button.right":
#                         pyautogui.mouseDown(button='right')
#                         print("double right click")
#                 else:
#                     if action["button"] == "Button.left":
#                         pyautogui.mouseDown(button='left')
#                         print("holding mode")
#                     elif action["button"] == "Button.right":
#                         pyautogui.mouseDown(button='right')
#                         print("holding right mode")

#                 last_click_time = current_time

#             elif action["action"] == "release":
#                 if action["button"] == "Button.left":
#                     pyautogui.mouseUp(button='left')
#                     print("normal click")
#                 elif action["button"] == "Button.right":
#                     pyautogui.mouseUp(button='right')
#                     print("normal right click")

#             elif action["action"] == "scroll":
#                 # Adjust the sleep time based on the duration of the scroll action
#                 time.sleep(0.01)
#                 mouse.wheel(delta=action["scroll"])

#             elif action["action"] == "key_release":
#                 # Perform keyboard action using pyautogui
#                     time.sleep(0.01)
#                     pyautogui.press(action["key"])

#                     print(f"Key released: {action['key']}")

#         print("Replay complete.")

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Mouse and Keyboard Recorder/Replayer')
#     parser.add_argument('command', choices=['record', 'replay'], help='Choose command: record or replay')
#     parser.add_argument('--file', default='actions.json', help='File to save or load mouse and keyboard actions (default: actions.json)')
#     args = parser.parse_args()

#     if args.command == 'record':
#         record(args.file)
#     elif args.command == 'replay':
#         replay(args.file)








# import time
# import json
# import argparse
# from pynput import mouse as pynput_mouse, keyboard as pynput_keyboard
# import pyautogui
# import mouse
# import ctypes

# # Get screen resolution
# screen_width, screen_height = pyautogui.size()

# # Function to set the cursor position using the Windows API
# def set_cursor_pos(x, y):
#     ctypes.windll.user32.SetCursorPos(x, y)

# SPECIAL_KEYS_MAPPING = {
#     pynput_keyboard.Key.alt: 'alt',
#     pynput_keyboard.Key.alt_l: 'altleft',
#     pynput_keyboard.Key.alt_r: 'altright',
#     pynput_keyboard.Key.alt_gr: 'altright',
#     pynput_keyboard.Key.backspace: 'backspace',
#     pynput_keyboard.Key.caps_lock: 'capslock',
#     pynput_keyboard.Key.cmd: 'winleft',
#     pynput_keyboard.Key.cmd_l: 'winleft',
#     pynput_keyboard.Key.cmd_r: 'winright',
#     pynput_keyboard.Key.ctrl: 'ctrlleft',
#     pynput_keyboard.Key.ctrl_l: 'ctrlleft',
#     pynput_keyboard.Key.ctrl_r: 'ctrlright',
#     pynput_keyboard.Key.delete: 'delete',
#     pynput_keyboard.Key.down: 'down',
#     pynput_keyboard.Key.end: 'end',
#     pynput_keyboard.Key.enter: 'enter',
#     pynput_keyboard.Key.esc: 'esc',
#     pynput_keyboard.Key.f1: 'f1',
#     pynput_keyboard.Key.f2: 'f2',
#     pynput_keyboard.Key.f3: 'f3',
#     pynput_keyboard.Key.f4: 'f4',
#     pynput_keyboard.Key.f5: 'f5',
#     pynput_keyboard.Key.f6: 'f6',
#     pynput_keyboard.Key.f7: 'f7',
#     pynput_keyboard.Key.f8: 'f8',
#     pynput_keyboard.Key.f9: 'f9',
#     pynput_keyboard.Key.f10: 'f10',
#     pynput_keyboard.Key.f11: 'f11',
#     pynput_keyboard.Key.f12: 'f12',
#     pynput_keyboard.Key.home: 'home',
#     pynput_keyboard.Key.left: 'left',
#     pynput_keyboard.Key.page_down: 'pagedown',
#     pynput_keyboard.Key.page_up: 'pageup',
#     pynput_keyboard.Key.right: 'right',
#     pynput_keyboard.Key.shift: 'shift_left',
#     pynput_keyboard.Key.shift_l: 'shift_left',
#     pynput_keyboard.Key.shift_r: 'shiftright',
#     pynput_keyboard.Key.space: 'space',
#     pynput_keyboard.Key.tab: 'tab',
#     pynput_keyboard.Key.up: 'up',
#     pynput_keyboard.Key.media_play_pause: 'playpause',
#     pynput_keyboard.Key.insert: 'insert',
#     pynput_keyboard.Key.num_lock: 'num_lock',
#     pynput_keyboard.Key.pause: 'pause',
#     pynput_keyboard.Key.print_screen: 'print_screen',
#     pynput_keyboard.Key.scroll_lock: 'scroll_lock',
# }

# def record(filename):
#     print("Recording started. Move the mouse around and perform actions. Press Ctrl + C to stop.") 
#     actions = []
#     previous_time = time.time()  # Initialize previous_time

#     # Initialize the mouse listener for scroll and press events
#     def on_move(x, y):
#         if 0 <= x < screen_width and 0 <= y < screen_height:
#             actions.append({
#                 "action": "move",
#                 "position": (x, y),
#                 "time_diff": time_diff
#             })

#     def on_click(x, y, button, pressed):
#         if 0 <= x < screen_width and 0 <= y < screen_height:
#             actions.append({
#                 "action": "press" if pressed else "release",
#                 "button": str(button),
#                 "position": (x, y),
#                 "time_diff": time_diff
#             })

#     def on_scroll(x, y, dx, dy):
#         if 0 <= x < screen_width and 0 <= y < screen_height:
#             actions.append({
#                 "action": "scroll",
#                 "position": (x, y),
#                 "scroll": dy,
#                 "time_diff": time_diff
#             })

#     def on_key_release(key):
#         action = {
#             "action": "key_release",
#             "key": None
#         }

#         # Try to get the character of the key
#         try:
#             action["key"] = key.char
#         except AttributeError:
#             if key in SPECIAL_KEYS_MAPPING: 
#                 action["key"] = SPECIAL_KEYS_MAPPING[key]
#             else:
#                 action["key"] = str(key)
#         print(action["key"])
#         actions.append(action)

#     mouse_listener = pynput_mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
#     mouse_listener.start()

#     keyboard_listener = pynput_keyboard.Listener(on_release=on_key_release)
#     keyboard_listener.start()

#     try:
#         while True:
#             current_time = time.time()
#             time_diff = current_time - previous_time

#             # Get the current mouse position
#             x, y = mouse.get_position()

#             # Keep the mouse within the screen boundaries
#             x = max(0, min(x, screen_width - 1))
#             y = max(0, min(y, screen_height - 1))
            
#             set_cursor_pos(x, y)

#             time.sleep(0.05)  # Adjusted sleep time for smoother recordings

#     except KeyboardInterrupt:
#         print("Recording stopped.")
#         mouse_listener.stop()
#         keyboard_listener.stop()
#         with open(filename, 'w') as file:
#             json.dump(actions, file)

# # Function to replay mouse and keyboard actions
# def replay(filename):
#     with open(filename, 'r') as file:
#         actions = json.load(file)
#         print("Replaying mouse and keyboard movements...")

#         # Variables for double click detection
#         last_click_time = 0
#         double_click_threshold = 0.3  # Adjust this threshold as needed for your scenario

#         for i in range(len(actions)):
#             action = actions[i]
#             if action["action"] == "move":
#                 # Use mouse.move for smooth movement at normal speed
#                 mouse.move(action["position"][0], action["position"][1], absolute=True, duration=0.01)
#             elif action["action"] == "press":
#                 current_time = action["time_diff"]

#                 # Check for double click
#                 if current_time - last_click_time <= double_click_threshold:
#                     if action["button"] == "Button.left":
#                         pyautogui.mouseDown(button='left')
#                         print("double click")
#                     elif action["button"] == "Button.right":
#                         pyautogui.mouseDown(button='right')
#                         print("double right click")
#                 else:
#                     if action["button"] == "Button.left":
#                         pyautogui.mouseDown(button='left')
#                         print("holding mode")
#                     elif action["button"] == "Button.right":
#                         pyautogui.mouseDown(button='right')
#                         print("holding right mode")

#                 last_click_time = current_time

#             elif action["action"] == "release":
#                 if action["button"] == "Button.left":
#                     pyautogui.mouseUp(button='left')
#                     print("normal click")
#                 elif action["button"] == "Button.right":
#                     pyautogui.mouseUp(button='right')
#                     print("normal right click")

#             elif action["action"] == "scroll":
#                 # Adjust the sleep time based on the duration of the scroll action
#                 time.sleep(0.01)
#                 mouse.wheel(delta=action["scroll"])

#             elif action["action"] == "key_release":
#                 # Perform keyboard action using pyautogui
#                     time.sleep(0.01)
#                     pyautogui.press(action["key"])

#                     print(f"Key released: {action['key']}")

#         print("Replay complete.")

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Mouse and Keyboard Recorder/Replayer')
#     parser.add_argument('command', choices=['record', 'replay'], help='Choose command: record or replay')
#     parser.add_argument('--file', default='actions.json', help='File to save or load mouse and keyboard actions (default: actions.json)')
#     args = parser.parse_args()

#     if args.command == 'record':
#         record(args.file)
#     elif args.command == 'replay':
#         replay(args.file)




import time
import json
import argparse
from pynput import mouse as pynput_mouse, keyboard as pynput_keyboard
import pyautogui
import mouse
import ctypes

# Get screen resolution
screen_width, screen_height = pyautogui.size()

# Function to set the cursor position using the Windows API
def set_cursor_pos(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)

SPECIAL_KEYS_MAPPING = {
    pynput_keyboard.Key.alt: 'alt',
    pynput_keyboard.Key.alt_l: 'altleft',
    pynput_keyboard.Key.alt_r: 'altright',
    pynput_keyboard.Key.alt_gr: 'altright',
    pynput_keyboard.Key.backspace: 'backspace',
    pynput_keyboard.Key.caps_lock: 'capslock',
    pynput_keyboard.Key.cmd: 'winleft',
    pynput_keyboard.Key.cmd_l: 'winleft',
    pynput_keyboard.Key.cmd_r: 'winright',
    pynput_keyboard.Key.ctrl: 'ctrlleft',
    pynput_keyboard.Key.ctrl_l: 'ctrlleft',
    pynput_keyboard.Key.ctrl_r: 'ctrlright',
    pynput_keyboard.Key.delete: 'delete',
    pynput_keyboard.Key.down: 'down',
    pynput_keyboard.Key.end: 'end',
    pynput_keyboard.Key.enter: 'enter',
    pynput_keyboard.Key.esc: 'esc',
    pynput_keyboard.Key.f1: 'f1',
    pynput_keyboard.Key.f2: 'f2',
    pynput_keyboard.Key.f3: 'f3',
    pynput_keyboard.Key.f4: 'f4',
    pynput_keyboard.Key.f5: 'f5',
    pynput_keyboard.Key.f6: 'f6',
    pynput_keyboard.Key.f7: 'f7',
    pynput_keyboard.Key.f8: 'f8',
    pynput_keyboard.Key.f9: 'f9',
    pynput_keyboard.Key.f10: 'f10',
    pynput_keyboard.Key.f11: 'f11',
    pynput_keyboard.Key.f12: 'f12',
    pynput_keyboard.Key.home: 'home',
    pynput_keyboard.Key.left: 'left',
    pynput_keyboard.Key.page_down: 'pagedown',
    pynput_keyboard.Key.page_up: 'pageup',
    pynput_keyboard.Key.right: 'right',
    pynput_keyboard.Key.shift: 'shift_left',
    pynput_keyboard.Key.shift_l: 'shift_left',
    pynput_keyboard.Key.shift_r: 'shiftright',
    pynput_keyboard.Key.space: 'space',
    pynput_keyboard.Key.tab: 'tab',
    pynput_keyboard.Key.up: 'up',
    pynput_keyboard.Key.media_play_pause: 'playpause',
    pynput_keyboard.Key.insert: 'insert',
    pynput_keyboard.Key.num_lock: 'num_lock',
    pynput_keyboard.Key.pause: 'pause',
    pynput_keyboard.Key.print_screen: 'print_screen',
    pynput_keyboard.Key.scroll_lock: 'scroll_lock',
}

def record(filename):
    print("Recording started. Move the mouse around and perform actions. Press Ctrl + C to stop.") 
    actions = []
    previous_time = time.time()  # Initialize previous_time

    # Dictionary to store the state of pressed keys
    pressed_keys = {}

    # Initialize the mouse listener for scroll and press events
    def on_move(x, y):
        if 0 <= x < screen_width and 0 <= y < screen_height:
            actions.append({
                "action": "move",
                "position": (x, y),
                "time_diff": time_diff
            })

    def on_click(x, y, button, pressed):
        if 0 <= x < screen_width and 0 <= y < screen_height:
            actions.append({
                "action": "press" if pressed else "release",
                "button": str(button),
                "position": (x, y),
                "time_diff": time_diff
            })

    def on_scroll(x, y, dx, dy):
        if 0 <= x < screen_width and 0 <= y < screen_height:
            actions.append({
                "action": "scroll",
                "position": (x, y),
                "scroll": dy,
                "time_diff": time_diff
            })

    def on_key_press(key):
        action = {
            "action": "key_press",
            "key": None,
            "time_diff": time_diff
        }

        # Try to get the character of the key
        try:
            action["key"] = key.char
        except AttributeError:
            if key in SPECIAL_KEYS_MAPPING: 
                action["key"] = SPECIAL_KEYS_MAPPING[key]
            else:
                action["key"] = str(key)

        # Update the pressed keys dictionary
        pressed_keys[action["key"]] = time_diff

        actions.append(action)

    def on_key_release(key):
        action = {
            "action": "key_release",
            "key": None,
            "time_diff": time_diff
        }

        # Try to get the character of the key
        try:
            action["key"] = key.char
        except AttributeError:
            if key in SPECIAL_KEYS_MAPPING: 
                action["key"] = SPECIAL_KEYS_MAPPING[key]
            else:
                action["key"] = str(key)

        # Remove the key from the pressed keys dictionary a a a dsadsa 
        if action["key"] in pressed_keys:
            del pressed_keys[action["key"]]

        actions.append(action)

    mouse_listener = pynput_mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    mouse_listener.start()

    # Register the key press and release listeners
    key_listener = pynput_keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
    key_listener.start()

    
    try:
        while True:
            
            keys_pressed = list(pressed_keys)
            if keys_pressed: 
                actions.append({
                    "action": "keys_pressed",
                    "keys": keys_pressed,
                    "time_diff": time_diff
                })            


            time.sleep(0.05)  # Adjusted sleep time for smoother recordings
            
            current_time = time.time()
            time_diff = current_time - previous_time

            # Get the current mouse position
            x, y = mouse.get_position()

            # Keep the mouse within the screen boundaries
            x = max(0, min(x, screen_width - 1))
            y = max(0, min(y, screen_height - 1))
            
            set_cursor_pos(x, y)

            time.sleep(0.05)  # Adjusted sleep time for smoother recordings

    except KeyboardInterrupt:
        print("Recording stopped.")
        mouse_listener.stop()
        with open(filename, 'w') as file:
            json.dump(actions, file)

# Function to replay mouse and keyboard actions
def replay(filename):
    with open(filename, 'r') as file:
        actions = json.load(file)
        print("Replaying mouse and keyboard movements...")

        # Variables for double click detection
        last_click_time = 0
        double_click_threshold = 0.3  # Adjust this threshold as needed for your scenario

        # Dictionary to store the state of pressed keys
        pressed_keys = {}

        for i in range(len(actions)):
            action = actions[i]
            if action["action"] == "move":
                # Use mouse.move for smooth movement at normal speed
                mouse.move(action["position"][0], action["position"][1], absolute=True, duration=0.01)
            elif action["action"] == "press":
                current_time = action["time_diff"]

                # Check for double click
                if current_time - last_click_time <= double_click_threshold:
                    if action["button"] == "Button.left":
                        pyautogui.mouseDown(button='left')
                        print("double click")
                    elif action["button"] == "Button.right":
                        pyautogui.mouseDown(button='right')
                        print("double right click")
                else:
                    if action["button"] == "Button.left":
                        pyautogui.mouseDown(button='left')
                        print("holding mode")
                    elif action["button"] == "Button.right":
                        pyautogui.mouseDown(button='right')
                        print("holding right mode")

                last_click_time = current_time

            elif action["action"] == "release":
                if action["button"] == "Button.left":
                    pyautogui.mouseUp(button='left')
                    print("normal click")
                elif action["button"] == "Button.right":
                    pyautogui.mouseUp(button='right')
                    print("normal right click")

            elif action["action"] == "scroll":
                # Adjust the sleep time based on the duration of the scroll action
                time.sleep(0.01)
                mouse.wheel(delta=action["scroll"])

            elif action["action"] == "key_press":
                key = action["key"]
                current_time = action["time_diff"]

                # Check for special keys or key combinations
                if '+' in key:
                    # Split and simulate key combination
                    keys = key.split('+')
                    for k in keys:
                        if k not in pressed_keys or current_time - pressed_keys[k] <= 0.1:
                            # Press the key if not already pressed or pressed within a time frame
                            pyautogui.keyDown(k)
                            pressed_keys[k] = current_time
                else:
                    # Simulate normal key press
                    pyautogui.keyDown(key)
                    pressed_keys[key] = current_time

                print(f"Key pressed: {key}")

            elif action["action"] == "key_release":
                key = action["key"]
                current_time = action["time_diff"]

                # Check for special keys or key combinations
                if '+' in key:
                    # Split and simulate key combination
                    keys = key.split('+')
                    for k in keys:
                        if k in pressed_keys:
                            # Release the key if it was pressed
                            pyautogui.keyUp(k)
                            del pressed_keys[k]
                else:
                    # Simulate normal key release
                    pyautogui.keyUp(key)
                    del pressed_keys[key]

                print(f"Key released: {key}")

        # Release any remaining pressed keys
        for key in pressed_keys:
            pyautogui.keyUp(key)
            print(f"Key released: {key}")

        print("Replay complete.")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mouse and Keyboard Recorder/Replayer')
    parser.add_argument('command', choices=['record', 'replay'], help='Choose command: record or replay')
    parser.add_argument('--file', default='actions.json', help='File to save or load mouse and keyboard actions (default: actions.json)')
    args = parser.parse_args()

    if args.command == 'record':
        record(args.file)
    elif args.command == 'replay':
        replay(args.file)

