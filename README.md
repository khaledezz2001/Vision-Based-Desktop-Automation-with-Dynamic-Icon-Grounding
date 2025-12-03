# Vision-Based Desktop Automation with Dynamic Icon Grounding

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Platform-Windows-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</p>

A robust Python application that uses computer vision to dynamically locate and interact with desktop icons on Windows. The system can find the Notepad icon regardless of its position or the desktop background, enabling reliable automation.

## 🎯 Objective

Develop a Python application that uses computer vision to dynamically locate and interact with desktop icons on Windows (1920x1080 resolution). The system must find the Notepad icon regardless of its position on the desktop, enabling robust automation even when icon positions change.

## ✨ Features

- **Dynamic Icon Grounding:** Employs a hierarchy of computer vision techniques (Edge Detection, ORB, Template Matching) for maximum robustness.
- **Background Agnostic:** Reliably finds icons even with different desktop wallpapers.
- **Error Handling & Retries:** Includes comprehensive error handling with retry logic for transient failures.
- **Modular Architecture:** Code is organized into logical modules (`api_client`, `gui_automation`, `config`) for easy maintenance.
- **API Integration:** Fetches data from an external API (JSONPlaceholder) to automate a real-world task.
- **Configuration Driven:** Easily change settings like post count, matching thresholds, and file paths via `config.py`.
- **uv Support:** Uses modern Python packaging with `pyproject.toml` for reproducible environments.

## 📋 Requirements

- **Operating System:** Windows 10 or 11
- **Screen Resolution:** 1920x1080
- **Python:** 3.8 or newer
- **Prerequisite:** A Notepad shortcut icon must be present on the desktop.

## 🚀 Installation & Setup

This project uses `uv` for modern, reproducible dependency management.

### Method 1: Using `uv` (Recommended)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    uv sync
    ```
    This command reads the `pyproject.toml` file to set up the project and install all required packages.

3.  **Run the script:**
    ```bash
    uv run python automation_script.py
    ```

### Method 2: Using `pip`

1.  **Clone the repository** (as above).
2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # On Windows
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the script:**
    ```bash
    python automation_script.py
    ```

## ⚙️ Configuration

You can customize the automation by editing the settings in `config.py`:

- `POSTS_TO_PROCESS`: Number of blog posts to process.
- `ICON_REFERENCE_IMAGE`: The filename of your reference icon image.
- `MATCH_THRESHOLD`: Sensitivity for icon matching.
- `SAVE_DIRECTORY`: Where the output `.txt` files are saved.

## 🏃 Usage

### 1. Create a Reference Icon (First-Time Setup)

Before running, you must create a reference image of the Notepad icon that matches your system's appearance (icon size, theme).

```bash
uv run python create_reference_image.py