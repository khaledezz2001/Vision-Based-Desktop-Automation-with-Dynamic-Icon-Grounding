# Vision-Based Desktop Automation with Dynamic Icon Grounding

A Python application that uses computer vision to dynamically locate and interact with desktop icons on Windows (1920×1080). The system robustly identifies and clicks the Notepad icon regardless of its position on the desktop, enabling automation workflows even when icon layouts change.

## 📋 Project Overview

This project implements a vision-based desktop automation system that:
- Dynamically locates the Notepad icon on a Windows desktop using computer vision
- Launches Notepad and automates content creation from API data
- Handles icon repositioning, varying desktop themes, and partial obscurations
- Implements robust error handling and retry logic for production reliability

## 🎯 Features

- **Dynamic Icon Grounding**: Locates desktop icons without hardcoded positions or pre-trained templates
- **Automated Workflow**:
  - Captures desktop screenshots
  - Grounds and clicks the Notepad icon
  - Fetches posts from JSONPlaceholder API
  - Types and saves content in Notepad
- **Robust Error Handling**:
  - Retry logic (up to 3 attempts)
  - Window launch validation
  - API failure graceful degradation
  - Existing file handling
- **Adaptive Detection**:
  - Handles different icon positions (top-left, bottom-right, center)
  - Manages partial obscuration by other windows
  - Accommodates varying desktop backgrounds

## 🛠️ Tech Stack

- **Python 3.9+**
- **Computer Vision**: OpenCV, Pillow
- **Desktop Automation**: pyautogui, pygetwindow
- **API Interaction**: requests
- **Dependency Management**: uv
- **OS**: Windows 10/11 (1920×1080 resolution)

## 📁 Project Structure
