#!/usr/bin/env python3
"""
Setup script for Phishing Detection System
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def setup_backend():
    """Setup the backend API"""
    print("\n🔧 Setting up Backend API...")
    
    # Change to ml-api directory
    os.chdir("ml-api")
    
    # Create virtual environment
    if not run_command("python -m venv venv", "Creating virtual environment"):
        return False
    
    # Activate virtual environment and install dependencies
    if platform.system() == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    # Install dependencies
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies"):
        return False
    
    # Train model if needed
    if not os.path.exists("phishing_model.pkl"):
        if not run_command(f"{activate_cmd} && python train_model.py", "Training ML model"):
            return False
    
    print("✅ Backend setup completed!")
    return True

def create_startup_scripts():
    """Create startup scripts for easy launching"""
    
    # Windows batch file
    if platform.system() == "Windows":
        with open("start_api.bat", "w") as f:
            f.write("@echo off\n")
            f.write("cd ml-api\n")
            f.write("venv\\Scripts\\activate\n")
            f.write("python app.py\n")
            f.write("pause\n")
        print("✅ Created start_api.bat")
    
    # Unix shell script
    else:
        with open("start_api.sh", "w") as f:
            f.write("#!/bin/bash\n")
            f.write("cd ml-api\n")
            f.write("source venv/bin/activate\n")
            f.write("python app.py\n")
        os.chmod("start_api.sh", 0o755)
        print("✅ Created start_api.sh")

def main():
    """Main setup function"""
    print("🛡️ Phishing Detection System Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Setup backend
    if not setup_backend():
        print("❌ Backend setup failed")
        return
    
    # Create startup scripts
    create_startup_scripts()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start the API server:")
    if platform.system() == "Windows":
        print("   - Double-click start_api.bat")
        print("   - Or run: cd ml-api && venv\\Scripts\\activate && python app.py")
    else:
        print("   - Run: ./start_api.sh")
        print("   - Or run: cd ml-api && source venv/bin/activate && python app.py")
    
    print("2. Load the browser extension:")
    print("   - Open Chrome and go to chrome://extensions/")
    print("   - Enable Developer mode")
    print("   - Click 'Load unpacked' and select the phishing-extension folder")
    
    print("3. Test the system:")
    print("   - Run: cd ml-api && python test_api.py")
    
    print("\n🚀 Your phishing detection system is ready!")

if __name__ == "__main__":
    main() 