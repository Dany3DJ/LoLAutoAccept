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

    scales = np.linspace(0.5, 1.2, 6)  # Try various scales
    best_val = 0
    best_loc = None
    best_scale = 1

    for scale in scales:
        resized_template = cv2.resize(template, (0, 0), fx=scale, fy=scale)
        if gray_screenshot.shape[0] < resized_template.shape[0] or gray_screenshot.shape[1] < resized_template.shape[1]:
            continue  # Skip if template is bigger than screenshot

        res = cv2.matchTemplate(gray_screenshot, resized_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if max_val > best_val:
            best_val = max_val
            best_loc = max_loc
            best_scale = scale
            best_size = resized_template.shape[::-1]  # (w, h)

    if best_val >= threshold:
        top_left = best_loc
        w, h = best_size
        center_x = top_left[0] + w // 2
        center_y = top_left[1] + h // 2

        #print(f"🎯 Accept button found at ({center_x}, {center_y}) with scale {best_scale:.2f}, clicking...")
        print("🎯 Accept button found!")
        time.sleep(0.2)
        click(center_x, center_y)
        quit()
        return True
    else:
        print("🔍 Accept button not found")
        return False

print("🕹️ League Auto-Accept Bot Running...")

try:
    while True:
        find_and_click_accept()
        time.sleep(2)  # Avoid CPU overload
except KeyboardInterrupt:
    print("🛑 Bot stopped.")
