# import time
# import json
# import argparse
# import mouse
# from pynput import mouse as pynput_mouse

# DOUBLE_CLICK_THRESHOLD = 0.3  # Define a threshold for double-click action (in seconds)

# def record(filename):
#     print("Recording started. Move the mouse around and perform actions. Press Ctrl + C to stop.")
#     actions = []
#     previous_y = mouse.get_position()[1]  # Initialize previous_y
#     previous_time = time.time()  # Initialize previous_time
#     previous_left_click_time = None  # Store the time of the previous left click
    
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

#                 if left_click:
#                     if previous_left_click_time is not None:
#                         time_since_last_click = current_time - previous_left_click_time
#                         if time_since_last_click <= DOUBLE_CLICK_THRESHOLD:
#                             # If within threshold, mark as a double-click
#                             actions[-1]["double_click"] = True
#                     previous_left_click_time = current_time

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
#             if action.get("double_click"):
#                 mouse.click("left")
#                 # mouse.click("left")
#             else:
#                 if action["left_click"]:
#                     mouse.click("left")
#                 if action["right_click"]:
#                     mouse.click("right")
#                 if action["scroll"] != 0:
#                     mouse.wheel(delta=action["scroll"])
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
import mouse
from pynput import mouse as pynput_mouse

def record(filename):
    print("Recording started. Move the mouse around and perform actions. Press Ctrl + C to stop.")
    actions = []
    previous_time = time.time()  # Initialize previous_time
    
    # Initialize the mouse listener for scroll events
    def on_scroll(x, y, dx, dy):
        actions.append({
            "time_diff": time_diff,
            "position": mouse.get_position(),
            "left_click": mouse.is_pressed(button="left"),
            "right_click": mouse.is_pressed(button="right"),
            "scroll": dy  # Using dy to capture the scroll details
        })

    with pynput_mouse.Listener(on_scroll=on_scroll) as listener:
        try:
            while True:
                current_time = time.time()
                time_diff = current_time - previous_time

                position = mouse.get_position()
                left_click = mouse.is_pressed(button="left")
                right_click = mouse.is_pressed(button="right")

                actions.append({
                    "time_diff": time_diff,
                    "position": position,
                    "left_click": left_click,
                    "right_click": right_click,
                    "scroll": 0  # Initialize scroll as 0
                })

                previous_time = current_time

                time.sleep(0.05)  # Adjusted sleep time for smoother recordings

        except KeyboardInterrupt:
            print("Recording stopped.")
            listener.stop()  # Stop the listener
            with open(filename, 'w') as file:
                json.dump(actions, file)

def replay(filename):
    with open(filename, 'r') as file:
        actions = json.load(file)
        print("Replaying mouse movements...")
        for i in range(len(actions)):
            action = actions[i]
            time.sleep(action["time_diff"])  # Use the recorded time differences
            mouse.move(action["position"][0], action["position"][1], absolute=True)
            if action["left_click"]:
                mouse.click("left")
            if action["right_click"]:
                mouse.click("right")
            if action["scroll"] != 0:
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






