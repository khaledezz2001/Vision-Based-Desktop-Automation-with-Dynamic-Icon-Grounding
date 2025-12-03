# config.py

import os

# --- Path Configuration ---
# IMPORTANT: Make sure this filename matches your reference image exactly!
ICON_REFERENCE_IMAGE = 'notepad_icon.png'

# Directory to save the files on the desktop
DESKTOP_PATH = os.path.join(os.path.expanduser('~'), 'Desktop')
SAVE_DIRECTORY = os.path.join(DESKTOP_PATH, 'tjm-project')

# --- API Configuration ---
API_URL = 'https://jsonplaceholder.typicode.com/posts'

# --- Automation Settings ---
# How many posts to process
POSTS_TO_PROCESS = 10
# Confidence threshold for template matching (0.0 to 1.0)
TEMPLATE_MATCH_THRESHOLD = 0.8
# Maximum number of retries for finding and clicking the icon
MAX_RETRIES = 3
# Timeout in seconds for waiting for Notepad to launch
NOTEPAD_LAUNCH_TIMEOUT = 10

# --- Icon Detection Settings ---
# Minimum number of matches required for ORB feature matching
MIN_ORB_MATCHES = 15
# Number of features to detect with ORB
ORB_NFEATURES = 1000
# ===================================================================
# === THIS IS THE NEW LINE. PLEASE MAKE SURE IT IS PRESENT ===
# Threshold for the edge detection method
EDGE_DETECTION_THRESHOLD = 0.66
# ===================================================================