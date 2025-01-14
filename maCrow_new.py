import time
import json
import argparse
from pynput import mouse as pynput_mouse
import pyautogui
import mouse
import keyboard
import ctypes
import tkinter as tk
from tkinter import Canvas, Label
import os

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

    if root.mode == "record":
        countdown_label.config(text="Recording has started  :3 ")
    elif root.mode == "replay":
        countdown_label.config(text="Replay has started :3 ")

    root.update()
    time.sleep(1)

    canvas.destroy()

def count_down_animation_config(mode):
    print(f"{mode.capitalize()} will start in:")
    root = tk.Tk()
    root.attributes("-transparentcolor", "white")
    root.overrideredirect(1)
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    root.attributes('-topmost', 1)
    root.mode = mode  # Set the mode attribute

    countdown_animation(root)
    root.withdraw()  # Hide the root window

def record(filename, should_continue):
    count_down_animation_config("record")
    actions = []
    start_time = time.time()  # Initialize start_time at the beginning of recording

    def on_move(x, y):
        nonlocal start_time
        current_time = time.time()
        time_diff = current_time - start_time
        start_time = current_time
        if 0 <= x < screen_width and 0 <= y < screen_height:
            actions.append({
                "action": "move",
                "position": (x, y),
                "time_diff": time_diff
            })

    def on_click(x, y, button, pressed):
        nonlocal start_time
        current_time = time.time()
        time_diff = current_time - start_time
        start_time = current_time
        if 0 <= x < screen_width and 0 <= y < screen_height:
            actions.append({
                "action": "press" if pressed else "release",
                "button": str(button),
                "position": (x, y),
                "time_diff": time_diff
            })

    def on_scroll(x, y, dx, dy):
        nonlocal start_time
        current_time = time.time()
        time_diff = current_time - start_time
        start_time = current_time
        if 0 <= x < screen_width and 0 <= y < screen_height:
            actions.append({
                "action": "scroll",
                "position": (x, y),
                "scroll": dy,
                "time_diff": time_diff
            })

    def on_key_event(event):
        nonlocal start_time
        current_time = time.time()
        time_diff = current_time - start_time
        start_time = current_time
        actions.append({
            "action": "key",
            "key": event.name,
            "event_type": event.event_type,
            "time_diff": time_diff
        })

    listener = pynput_mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    listener.start()

    keyboard.hook(on_key_event)

    print("Recording started. Move the mouse around, perform actions, and type on the keyboard. Press Ctrl + C to stop.")
    try:
        while should_continue():
            time.sleep(0.05)  # Adjusted sleep time for smoother recordings
    finally:
        print("Recording stopped.")
        listener.stop()
        keyboard.unhook_all()

        with open(filename, 'w') as file:
            json.dump(actions, file)

def replay(filename, key_delay=0.1):
    count_down_animation_config("replay")
    with open(filename, 'r') as file:
        actions = json.load(file)
    print("Replaying mouse movements and keyboard inputs...")
    # Variables for double click detection
    last_click_time = 0
    double_click_threshold = 0.3  # Adjust this threshold as needed for your scenario

    for i in range(len(actions)):
        action = actions[i]
        if action["action"] == "move":
            # Use mouse.move for smooth movement at normal speed
            mouse.move(action["position"][0], action["position"][1], absolute=True, duration=0.00001)
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

        elif action["action"] == "key":
            if action["event_type"] == "down":
                keyboard.press(action["key"])
                print(f"Key pressed: {action['key']}")
            elif action["event_type"] == "up":
                keyboard.release(action["key"])
                print(f"Key released: {action['key']}")

            # Introduce a delay between key presses
            time.sleep(key_delay)

    print("Replay complete.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mouse and Keyboard Recorder/Replayer')
    parser.add_argument('command', choices=['record', 'replay'], help='Choose command: record or replay')
    parser.add_argument('--file', default='mouse_keyboard_actions.json',
                        help='File to save mouse and keyboard actions (default: mouse_keyboard_actions.json)')
    args = parser.parse_args()

    if args.command == 'record':
        record(args.file)
    elif args.command == 'replay':
        replay(args.file)