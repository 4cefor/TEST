#!/usr/bin/env python3
"""
Setup script for WhatsApp Bulk Messenger
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False
    return True

def create_sample_excel():
    """Create sample Excel file"""
    print("Creating sample Excel template...")
    try:
        subprocess.check_call([sys.executable, "create_sample_excel.py"])
        print("✅ Sample Excel file created!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create sample Excel: {e}")
        return False
    return True

def check_chrome():
    """Check if Chrome is installed"""
    print("Checking Chrome installation...")
    chrome_paths = [
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser", 
        "/usr/bin/chromium",
        "/opt/google/chrome/chrome"
    ]
    
    chrome_found = False
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"✅ Chrome found at: {path}")
            chrome_found = True
            break
    
    if not chrome_found:
        print("❌ Chrome/Chromium not found. Please install Google Chrome or Chromium browser.")
        print("On Ubuntu/Debian: sudo apt install google-chrome-stable")
        print("On CentOS/RHEL: sudo yum install google-chrome-stable")
        return False
    
    return True

def install_chromedriver():
    """Install ChromeDriver using webdriver-manager"""
    print("Setting up ChromeDriver...")
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        ChromeDriverManager().install()
        print("✅ ChromeDriver setup completed!")
    except Exception as e:
        print(f"❌ Failed to setup ChromeDriver: {e}")
        return False
    return True

def main():
    """Main setup function"""
    print("🚀 Setting up WhatsApp Bulk Messenger...")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Check Chrome
    if not check_chrome():
        sys.exit(1)
    
    # Install ChromeDriver
    if not install_chromedriver():
        sys.exit(1)
    
    # Create sample Excel
    if not create_sample_excel():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit 'contacts_template.xlsx' with your actual contacts")
    print("2. Run: python whatsapp_sender.py contacts_template.xlsx")
    print("3. Scan QR code when prompted")
    print("4. Watch the magic happen! ✨")

if __name__ == "__main__":
    main()