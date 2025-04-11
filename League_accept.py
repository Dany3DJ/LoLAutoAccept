import cv2
import numpy as np
import pyautogui
import os
import ctypes
import time

# Define constants for mouse input events
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

mouse_event = ctypes.windll.user32.mouse_event

def click(x, y):
    # Move mouse to (x, y)
    ctypes.windll.user32.SetCursorPos(x, y)
    time.sleep(0.5)  # Small delay to ensure the cursor is in position
    # Simulate mouse down and up events for left-click
    mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

# Load button image
script_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(script_dir, 'accept_word.png')
template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

if template is None:
    raise FileNotFoundError(f"❌ Could not load template image at {template_path}")

w, h = template.shape[::-1]
threshold = 0.8  # Confidence threshold

def find_and_click_accept():
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)
    gray_screenshot = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        top_left = max_loc
        center_x = top_left[0] + w // 2
        center_y = top_left[1] + h // 2

        print(f"🎯 Accept button found at ({center_x}, {center_y}), clicking...")
        time.sleep(0.5)  # Delay to ensure the click is registered
        click(center_x, center_y)
        quit()
        return True
    else:
        print("🔍 Accept button not found.")
        return False

print("🕹️ League Auto-Accept Bot Running... Press Ctrl+C to stop.")

try:
    while True:
        find_and_click_accept()
        time.sleep(2)  # Avoid CPU overload
except KeyboardInterrupt:
    print("🛑 Bot stopped.")