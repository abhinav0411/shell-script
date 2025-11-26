#!/usr/bin/env python3
"""
Screenshot to Gemini AI - GNOME/Wayland Script
Captures screenshot, sends to Gemini, copies response to clipboard
"""

import subprocess
import tempfile
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import base64
load_dotenv()

try:
    import google.generativeai as genai
except ImportError:
    print("Error: google-generativeai package not installed")
    print("Install with: pip install google-generativeai")
    sys.exit(1)

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY environment variable not set")
    print("Set it with: export GEMINI_API_KEY='your-api-key'")
    sys.exit(1)

def take_screenshot():
    """Take screenshot using GNOME Screenshot on Wayland"""
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        screenshot_path = tmp.name
    
    # Use gnome-screenshot with area selection
    result = subprocess.run(
            ['grim', '-g', subprocess.check_output(['slurp']).decode().strip(), screenshot_path],
            check=True
    )
    
    if result.returncode != 0:
        print("Screenshot cancelled or failed")
        if os.path.exists(screenshot_path):
            os.unlink(screenshot_path)
        sys.exit(1)
    
    return screenshot_path
def send_to_gemini(image_path, prompt="Analyze this image and give me the exact answer for the mcq do not give more explanation just give the option"""):
    genai.configure(api_key=GEMINI_API_KEY)

    # Try newer model first; fallback if unavailable
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
    except Exception:
        model = genai.GenerativeModel("gemini-pro-vision")

    with open(image_path, "rb") as img_file:
        image_data = img_file.read()

    # Proper structured request
    response = model.generate_content([
        {"role": "user", "parts": [
            {"text": prompt},
            {"mime_type": "image/png", "data": image_data}
        ]}
    ])

    # Check for valid text output
    if not hasattr(response, "text") or not response.text:
        print("⚠️ No text output received from Gemini. Response details:")
        print(response)
        return "(No response text from Gemini)"

    return response.text

def copy_to_clipboard(text):
    """Copy text to clipboard using wl-copy (Wayland)"""
    try:
        subprocess.run(
            ['wl-copy'],
            input=text.encode(),
            check=True
        )
        subprocess.run(
            [f'notify-send {text}'],
            shell=True
        )
        print("✓ Response copied to clipboard")
    except FileNotFoundError:
        print("Error: wl-copy not found. Install wl-clipboard package:")
        print("sudo dnf install wl-clipboard")
        sys.exit(1)

def main():
    print("📸 Take a screenshot by selecting an area...")
    screenshot_path = take_screenshot()
    
    try:
        print("🤖 Sending to Gemini AI...")
        response = send_to_gemini(screenshot_path)
        
        print("\n" + "="*60)
        print("GEMINI RESPONSE:")
        print("="*60)
        print(response)
        print("="*60 + "\n")
        
        copy_to_clipboard(response)
        
    finally:
        # Cleanup
        if os.path.exists(screenshot_path):
            os.unlink(screenshot_path)

if __name__ == '__main__':
    main()
