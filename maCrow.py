import time
import json
import argparse
from pynput import mouse as pynput_mouse
import pyautogui
import mouse
import ctypes
import tkinter as tk
from tkinter import Canvas, Label


# Get screen resolution
screen_width, screen_height = pyautogui.size()

# Function to set the cursor position using the Windows API
def set_cursor_pos(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)
    
# Function to display a countdown animation
def countdown_animation(root):
    canvas = Canvas(root, width=screen_width, height=screen_height, bg="white", highlightthickness=0)
    canvas.pack()

    countdown_label = Label(canvas, text="", font=("Helvetica", 50))
    countdown_label.place(relx=0.5, rely=0.5, anchor="center")

    for i in range(3, 0, -1):
        countdown_label.config(text=str(i))
        root.update()
        time.sleep(1)

    countdown_label.config(text="Recording has started OwO :3 !")
    root.update()
    time.sleep(1)

    canvas.destroy()
    
def count_down_animation_config():
    print("Recording will start in:")
    root = tk.Tk()
    root.attributes("-transparentcolor", "white")
    root.overrideredirect(1)
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    root.attributes('-topmost', 1)

    countdown_animation(root)
    root.withdraw()  # Hide the root window
    

def record(filename):
    count_down_animation_config()
    print("Recording started. Move the mouse around and perform actions. Press Ctrl + C to stop.")
    actions = []
    previous_time = time.time()  # Initialize previous_time

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

    listener = pynput_mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    listener.start()

    try:
        while True:
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
