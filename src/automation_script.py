# automation_script.py

import os
import time
import pyautogui
import pyperclip
import sys

# Import our custom modules and configuration
import config
from api_client import fetch_posts
from gui_automation import (
    minimize_all_windows, 
    take_screenshot, 
    find_icon,
    wait_for_notepad_launch
)

def process_post(post, save_directory, icon_path, max_retries=3):
    
    """Handles the entire process for a single post with retry logic."""
    print(f"\n--- Processing Post ID: {post['id']} ---")

    
    # Check if file already exists
    file_name = f"post_{post['id']}.txt"
    file_path = os.path.join(save_directory, file_name)
    
    if os.path.exists(file_path):
        print(f"File {file_name} already exists. Skipping this post.")
        return True
    
    # Retry logic for finding and clicking the icon
    for attempt in range(max_retries):
        print(f"Attempt {attempt + 1}/{max_retries}")
        
        # 1. Find the Notepad icon
        minimize_all_windows()

        time.sleep(0.5)
        screen_width, screen_height = pyautogui.size()
        x = screen_width // 2
        y = screen_height // 2
        pyautogui.moveTo(x, y, duration=0.5)
        pyautogui.click() # Extra wait for desktop to settle
        screenshot = take_screenshot()
        
        icon_coords = find_icon(
            screenshot, 
            icon_path,
            edge_threshold=config.EDGE_DETECTION_THRESHOLD,
            orb_min_matches=config.MIN_ORB_MATCHES,
            template_threshold=config.TEMPLATE_MATCH_THRESHOLD
        )

        if not icon_coords:
            print(f"Could not find the Notepad icon on attempt {attempt + 1}.")
            if attempt < max_retries - 1:
                print(f"Retrying in 1 second...")
                time.sleep(1)
                continue
            else:
                print("Max retries reached. Skipping this post.")
                return False

        x, y = icon_coords
        print(f"Icon located at: ({x}, {y})")

        # 2. Launch Notepad
        pyautogui.moveTo(x, y, duration=0.5)
        pyautogui.doubleClick()
        print("Launched Notepad.")
        
        # 3. Wait for Notepad to launch
        if wait_for_notepad_launch(timeout=config.NOTEPAD_LAUNCH_TIMEOUT):
            print("Notepad launched successfully.")
            time.sleep(1)
            break
        else:
            print(f"Notepad did not launch within timeout on attempt {attempt + 1}.")
            if attempt < max_retries - 1:
                print(f"Retrying in 1 second...")
                time.sleep(1)
                continue
            else:
                print("Max retries reached. Skipping this post.")
                return False
    
    # 4. Paste content using the clipboard
    content_to_type = f"Title: {post['title']}\n\n{post['body']}"
    pyperclip.copy(content_to_type)
    pyautogui.hotkey('ctrl', 'v')
    print("Pasted post content into Notepad.")
    time.sleep(1)

    # 5. Save the file
    try:
        pyautogui.hotkey('ctrl', 's')
        time.sleep(1.5)
        
        # Type the file path (corrected the replace method)
        # This should type the actual file path
        pyautogui.typewrite(file_path, interval=0.02)
        time.sleep(0.5)
        
        pyautogui.press('enter')
        print(f"Saved file as: {file_path}")
        time.sleep(1)
        
        # Wait for save to complete and check if file exists
        time.sleep(1)
        if os.path.exists(file_path):
            print("File saved successfully.")
        else:
            print("Warning: File may not have been saved correctly.")
            # Don't return False yet, continue to close Notepad
            
    except Exception as e:
        print(f"Error saving file: {e}")
        pyautogui.press('escape')
        time.sleep(0.5)
        pyautogui.hotkey('alt', 'f4')
        return False
    
    # 6. Close Notepad (only after saving)
    time.sleep(1)  # Wait a bit more after saving
    pyautogui.hotkey('alt', 'f4')
    print("Closed Notepad.")
    time.sleep(1)
    
    
    
    return True  # Return True at the very end

def main():
    """Main function to run the automation workflow."""
    print("Starting Vision-Based Desktop Automation...")
    
    if not os.path.exists(config.SAVE_DIRECTORY):
        os.makedirs(config.SAVE_DIRECTORY)
        print(f"Created directory: {config.SAVE_DIRECTORY}")

    # Check if reference image exists
    if not os.path.exists(config.ICON_REFERENCE_IMAGE):
        print(f"[FATAL ERROR] Reference image not found: {config.ICON_REFERENCE_IMAGE}")
        print("Please make sure the icon image is in the same directory as the script.")
        return

    posts = fetch_posts(config.API_URL)
    if not posts:
        print("Failed to fetch posts from API. Exiting.")
        return
    
    print(f"Successfully fetched {len(posts)} posts from API.")
    
    processed_count = 0
    failed_count = 0
    for post in posts[:config.POSTS_TO_PROCESS]:
        try:
            if process_post(post, config.SAVE_DIRECTORY, config.ICON_REFERENCE_IMAGE, config.MAX_RETRIES):
                
                processed_count += 1
            else:
                failed_count += 1
                
        except Exception as e:
            print(f"Error processing post {post['id']}: {e}")
            failed_count += 1
    
    print(f"\n--- Automation Complete ---")
    print(f"Successfully processed: {processed_count} posts")
    print(f"Failed to process: {failed_count} posts")

if __name__ == "__main__":
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.5
    
    try:
        main()
    except KeyboardInterrupt:
        print("\nAutomation interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)