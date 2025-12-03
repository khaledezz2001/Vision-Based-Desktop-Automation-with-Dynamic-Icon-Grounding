# gui_automation.py

import cv2
import numpy as np
import pyautogui
import time
import os

def minimize_all_windows():
    """Minimizes all open windows to show the desktop."""
    print("Minimizing all windows...")
    pyautogui.hotkey('win', 'd')
    time.sleep(1)

def take_screenshot():
    """Captures a screenshot of the entire screen."""
    print("Taking a screenshot...")
    screenshot = pyautogui.screenshot()
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return screenshot_cv

# In gui_automation.py

def find_icon_with_edge_detection(screenshot, reference_image_path, threshold=0.7, debug_save_dir=None):
    """
    Finds the icon by matching its edges, making it robust to background changes.
    Includes an option to save debug images.
    """
    print(f"Attempting Edge Detection Matching with {reference_image_path}...")
    try:
        ref_image = cv2.imread(reference_image_path, cv2.IMREAD_GRAYSCALE)
        if ref_image is None:
            print(f"[DEBUG] Could not load reference image: {reference_image_path}")
            return None
    except Exception as e:
        print(f"Error loading reference image: {e}")
        return None

    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Apply Canny edge detection to both images
    # The thresholds (100, 200) might need slight tuning for different icons
    ref_edges = cv2.Canny(ref_image, 100, 200)
    screenshot_edges = cv2.Canny(screenshot_gray, 100, 200)

    # --- NEW DEBUGGING CODE ---
    if debug_save_dir:
        ref_edges_path = os.path.join(debug_save_dir, 'debug_ref_edges.png')
        screenshot_edges_path = os.path.join(debug_save_dir, 'debug_screenshot_edges.png')
        cv2.imwrite(ref_edges_path, ref_edges)
        cv2.imwrite(screenshot_edges_path, screenshot_edges)
        print(f"[DEBUG] Saved reference edge image to: {ref_edges_path}")
        print(f"[DEBUG] Saved screenshot edge image to: {screenshot_edges_path}")
    # --- END DEBUGGING CODE ---

    w, h = ref_edges.shape[::-1]
    result = cv2.matchTemplate(screenshot_edges, ref_edges, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    print(f"Edge Detection: Best match value: {max_val:.2f} at {max_loc}")

    if max_val >= threshold:
        print(f"Edge Detection: Icon found with confidence {max_val:.2f}.")
        x, y = max_loc
        center_x = x + w // 2
        center_y = y + h // 2
        return (int(center_x), int(center_y))
    else:
        print(f"Edge Detection: Icon not found. Best match {max_val:.2f} below threshold {threshold}.")
        return None
    
def find_icon_with_orb(screenshot, reference_image_path, min_matches=15):
    """Finds icon using ORB feature matching."""
    print(f"Attempting ORB feature matching with {reference_image_path}...")
    try:
        ref_image = cv2.imread(reference_image_path, cv2.IMREAD_GRAYSCALE)
        if ref_image is None:
            print(f"[DEBUG] Could not load reference image: {reference_image_path}")
            return None
    except Exception as e:
        print(f"Error loading reference image: {e}")
        return None

    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create(nfeatures=1000)
    kp1, des1 = orb.detectAndCompute(ref_image, None)
    kp2, des2 = orb.detectAndCompute(screenshot_gray, None)

    if des1 is None or des2 is None:
        print("Could not find descriptors in one of the images.")
        return None

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)

    if len(matches) > min_matches:
        print(f"ORB: Icon found with {len(matches)} good matches.")
        src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        if M is None:
            print("Homography could not be computed.")
            return None
        h, w = ref_image.shape
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)
        (x, y, w, h) = cv2.boundingRect(dst)
        center_x = x + w // 2
        center_y = y + h // 2
        return (int(center_x), int(center_y))
    else:
        print(f"ORB: Icon not found. Only {len(matches)} matches found (need > {min_matches}).")
        return None

def find_icon_with_template_matching(screenshot, reference_image_path, threshold=0.8):
    """Finds icon using template matching."""
    print(f"Attempting template matching with {reference_image_path}...")
    try:
        ref_image = cv2.imread(reference_image_path, cv2.IMREAD_GRAYSCALE)
        if ref_image is None:
            print(f"[DEBUG] Could not load reference image: {reference_image_path}")
            return None
    except Exception as e:
        print(f"Error loading reference image: {e}")
        return None

    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    w, h = ref_image.shape[::-1]
    result = cv2.matchTemplate(screenshot_gray, ref_image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    print(f"Template: Best match value: {max_val:.2f} at {max_loc}")

    if max_val >= threshold:
        print(f"Template: Icon found with confidence {max_val:.2f}.")
        x, y = max_loc
        center_x = x + w // 2
        center_y = y + h // 2
        return (int(center_x), int(center_y))
    else:
        print(f"Template: Icon not found. Best match {max_val:.2f} below threshold {threshold}.")
        return None

def find_icon(screenshot, reference_image_path, edge_threshold, orb_min_matches, template_threshold):
    """
    Tries to find the icon using a hierarchy of methods, from most robust to least.
    Thresholds are passed in from the main script.
    """
    # Method 1: Edge Detection (Best for background changes)
    icon_coords = find_icon_with_edge_detection(screenshot, reference_image_path, threshold=edge_threshold)
    if icon_coords:
        return icon_coords
    
    # Method 2: ORB Feature Matching (Good for size/scale changes)
    print("Edge Detection failed, trying ORB feature matching...")
    icon_coords = find_icon_with_orb(screenshot, reference_image_path, min_matches=orb_min_matches)
    if icon_coords:
        return icon_coords

    # Method 3: Template Matching (Last resort)
    print("ORB failed, trying template matching...")
    return find_icon_with_template_matching(screenshot, reference_image_path, threshold=template_threshold)

def is_notepad_running():
    """Check if Notepad is currently running."""
    try:
        notepad_window = pyautogui.getWindowsWithTitle("Notepad")
        return len(notepad_window) > 0
    except:
        return False

def wait_for_notepad_launch(timeout=10):
    """Wait for Notepad to launch and return True if successful."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_notepad_running():
            return True
        time.sleep(0.5)
    return False