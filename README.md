# Vision-Based-Desktop-Automation-with-Dynamic-Icon-Grounding

A Python application that uses computer vision to dynamically locate and interact with desktop icons on Windows (1920×1080). The system robustly identifies and clicks the Notepad icon regardless of its position on the desktop, enabling automation workflows even when icon layouts change.

🎯 Key Features
Dynamic Icon Detection: Uses computer vision to locate desktop icons without hardcoded positions

Automated Workflow: Fetches blog posts from JSONPlaceholder API and saves them via Notepad

Robust & Adaptive: Handles icon repositioning, partial obscuration, and varying desktop themes

Error Handling: Retry logic, window validation, and graceful degradation for API failures

🛠️ Tech Stack
Python with uv for dependency management

OpenCV / pyautogui for screenshot and mouse control

Requests for API interaction

Pillow for image processing

📁 Deliverables
Fully documented source code

uv configuration for reproducible setup

Annotated screenshots demonstrating detection across desktop regions

Ready for live interview testing with movable icons

🧠 Discussion Ready
Detection methodology and trade-offs

Failure case analysis and improvements

Performance metrics and optimization strategies

Scalability to other icons, resolutions, and themes
