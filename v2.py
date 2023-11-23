#The version that only has basic framework with move,scroll and single click -stable version

# import time
# import json
# import argparse
# import mouse
# from pynput import mouse as pynput_mouse

# def record(filename):
#     print("Recording started. Move the mouse around and perform actions. Press Ctrl + C to stop.")
#     actions = []
#     previous_time = time.time()  # Initialize previous_time
    
#     # Initialize the mouse listener for scroll events
#     def on_scroll(x, y, dx, dy):
#         actions.append({
#             "time_diff": time_diff,
#             "position": mouse.get_position(),
#             "left_click": mouse.is_pressed(button="left"),
#             "right_click": mouse.is_pressed(button="right"),
#             "scroll": dy  # Using dy to capture the scroll details
#         })

#     with pynput_mouse.Listener(on_scroll=on_scroll) as listener:
#         try:
#             while True:
#                 current_time = time.time()
#                 time_diff = current_time - previous_time

#                 position = mouse.get_position()
#                 left_click = mouse.is_pressed(button="left")
#                 right_click = mouse.is_pressed(button="right")

#                 actions.append({
#                     "time_diff": time_diff,
#                     "position": position,
#                     "left_click": left_click,
#                     "right_click": right_click,
#                     "scroll": 0  # Initialize scroll as 0
#                 })

#                 previous_time = current_time

#                 time.sleep(0.05)  # Adjusted sleep time for smoother recordings

#         except KeyboardInterrupt:
#             print("Recording stopped.")
#             listener.stop()  # Stop the listener
#             with open(filename, 'w') as file:
#                 json.dump(actions, file)

# def replay(filename):
#     with open(filename, 'r') as file:
#         actions = json.load(file)
#         print("Replaying mouse movements...")
#         for i in range(len(actions)):
#             action = actions[i]
#             time.sleep(action["time_diff"])  # Use the recorded time differences
#             mouse.move(action["position"][0], action["position"][1], absolute=True)
#             if action["left_click"]:
#                 mouse.click("left")
#             if action["right_click"]:
#                 mouse.click("right")
#             if action["scroll"] != 0:
#                 mouse.wheel(delta=action["scroll"])
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



#This one is new one, can move, scroll, click, hold and drag , we are using this one from now on

# import time
# import json
# import argparse
# from pynput import mouse as pynput_mouse
# import pyautogui
# import mouse

# def record(filename):
#     print("Recording started. Move the mouse around and perform actions. Press Ctrl + C to stop.")
#     actions = []
#     previous_time = time.time()  # Initialize previous_time

#     # Initialize the mouse listener for scroll and press events
#     def on_move(x, y):
#         actions.append({
#             "action": "move",
#             "position": (x, y),
#             "time_diff": time_diff
#         })

#     def on_click(x, y, button, pressed):
#         actions.append({
#             "action": "press" if pressed else "release",
#             "button": str(button),
#             "position": (x, y),
#             "time_diff": time_diff
#         })

#     def on_scroll(x, y, dx, dy):
#         actions.append({
#             "action": "scroll",
#             "position": (x, y),
#             "scroll": dy,
#             "time_diff": time_diff
#         })

#     listener = pynput_mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
#     listener.start()

#     try:
#         while True:
#             current_time = time.time()
#             time_diff = current_time - previous_time
#             time.sleep(0.05)  # Adjusted sleep time for smoother recordings
#     except KeyboardInterrupt:
#         print("Recording stopped.")
#         listener.stop()
#         with open(filename, 'w') as file:
#             json.dump(actions, file)

# # Function to replay mouse actions
# def replay(filename):
#     with open(filename, 'r') as file:
#         actions = json.load(file)
#         print("Replaying mouse movements...")
#         for i in range(len(actions)):
#             action = actions[i]
#             if action["action"] == "move":
#                 # Use mouse.move for smooth movement at normal speed
#                 mouse.move(action["position"][0], action["position"][1], absolute=True, duration=0.01)
#             elif action["action"] == "press":
#                 if action["button"] == "Button.left":
#                     pyautogui.mouseDown(button='left')
#                     print("holding mode")
#             elif action["action"] == "release":
#                 if action["button"] == "Button.left":
#                     pyautogui.mouseUp(button='left')
#                     print("normal click")
#             elif action["action"] == "scroll":
#                 # Adjust the sleep time based on the duration of the scroll action
#                 time.sleep(0.01)
#                 mouse.wheel(delta=action["scroll"])

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



import time
import json
import argparse
from pynput import mouse as pynput_mouse
import pyautogui
import mouse

def record(filename):
    print("Recording started. Move the mouse around and perform actions. Press Ctrl + C to stop.")
    actions = []
    previous_time = time.time()  # Initialize previous_time

    # Initialize the mouse listener for scroll and press events
    def on_move(x, y):
        actions.append({
            "action": "move",
            "position": (x, y),
            "time_diff": time_diff
        })

    def on_click(x, y, button, pressed):
        actions.append({
            "action": "press" if pressed else "release",
            "button": str(button),
            "position": (x, y),
            "time_diff": time_diff
        })

    def on_scroll(x, y, dx, dy):
        actions.append({
            "action": "scroll",
            "position": (x, y),
            "scroll": dy,
            "time_diff": time_diff
        })

    listener = pynput_mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    listener.start()

    try:
        while True:
            current_time = time.time()
            time_diff = current_time - previous_time
            time.sleep(0.05)  # Adjusted sleep time for smoother recordings
    except KeyboardInterrupt:
        print("Recording stopped.")
        listener.stop()
        with open(filename, 'w') as file:
            json.dump(actions, file)

# Function to replay mouse actions
def replay(filename):
    with open(filename, 'r') as file:
        actions = json.load(file)
        print("Replaying mouse movements...")

        # Variables for double click detection
        last_click_time = 0
        double_click_threshold = 0.3  # Adjust this threshold as needed for your scenario

        for i in range(len(actions)):
            action = actions[i]
            if action["action"] == "move":
                # Use mouse.move for smooth movement at normal speed
                mouse.move(action["position"][0], action["position"][1], absolute=True, duration=0.01)
            elif action["action"] == "press":
                current_time = action["time_diff"]

                # Check for double click
                if current_time - last_click_time <= double_click_threshold:
                    pyautogui.mouseDown(button='left')
                    print("double click")
                else:
                    pyautogui.mouseDown(button='left')
                    print("holding mode")

                last_click_time = current_time

            elif action["action"] == "release":
                pyautogui.mouseUp(button='left')
                print("normal click")

            elif action["action"] == "scroll":
                # Adjust the sleep time based on the duration of the scroll action
                time.sleep(0.01)
                mouse.wheel(delta=action["scroll"])

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
