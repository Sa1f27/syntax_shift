#!/usr/bin/env python3
"""
Syntax Shift Setup Script
Automated setup for the AI-Powered Code Transformation Suite
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header():
    """Print welcome header"""
    print("=" * 60)
    print("🚀 SYNTAX SHIFT - AI CODE TRANSFORMATION SUITE")
    print("=" * 60)
    print("Welcome to the automated setup process!")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8+ is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        print("   Please upgrade Python and try again.")
        sys.exit(1)
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")

def create_directory_structure():
    """Create necessary directories"""
    print("\n📁 Creating directory structure...")
    
    directories = [
        "backend",
        "frontend", 
        "samples",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   Created: {directory}/")
    
    print("✅ Directory structure created")

def create_virtual_environment():
    """Create Python virtual environment"""
    print("\n🐍 Setting up virtual environment...")
    
    venv_name = "venv"
    
    try:
        subprocess.run([sys.executable, "-m", "venv", venv_name], check=True)
        print(f"✅ Virtual environment '{venv_name}' created")
        
        # Get activation command based on OS
        if platform.system() == "Windows":
            activate_cmd = f"{venv_name}\\Scripts\\activate"
        else:
            activate_cmd = f"source {venv_name}/bin/activate"
        
        print(f"📝 To activate: {activate_cmd}")
        return venv_name
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return None

def install_dependencies(venv_name):
    """Install Python dependencies"""
    print("\n📦 Installing dependencies...")
    
    # Get pip path
    if platform.system() == "Windows":
        pip_path = f"{venv_name}\\Scripts\\pip"
    else:
        pip_path = f"{venv_name}/bin/pip"
        
    dependencies = [
        "fastapi",
        "uvicorn[standard]",
        "pydantic",
        "groq",
        "python-multipart",
        "jinja2",
        "aiofiles"
    ]
    
    try:
        for dep in dependencies:
            print(f"   Installing {dep}...")
            subprocess.run([pip_path, "install", dep], check=True, capture_output=True)
        
        print("✅ All dependencies installed")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_env_file():
    """Create .env file for configuration"""
    print("\n⚙️ Creating configuration file...")
    
    env_content = """# Syntax Shift Configuration
# Copy this file to .env and update with your settings

# Required: Get your free API key from https://console.groq.com
GROQ_API_KEY=your_groq_api_key_here

# Optional: Server configuration
PORT=8000
HOST=127.0.0.1
DEBUG=false

# Optional: Processing limits
MAX_CODE_LENGTH=50000
RATE_LIMIT=100

# Optional: Model configuration
AI_MODEL=meta-llama/llama-4-maverick-17b-128e-instruct
TEMPERATURE=0.3
MAX_TOKENS=1024
"""
    
    with open(".env.example", "w") as f:
        f.write(env_content)
    
    print("✅ Configuration template created (.env.example)")
    print("📝 Copy .env.example to .env and add your Groq API key")

def create_launch_script():
    """Create launch script for easy startup"""
    print("\n🚀 Creating launch script...")
    
    if platform.system() == "Windows":
        # Windows batch script
        script_content = '''@echo off
echo Starting Syntax Shift Server...
echo.

REM Activate virtual environment
call syntax_shift_env\\Scripts\\activate

REM Check if .env file exists
if not exist .env (
    echo ❌ Error: .env file not found
    echo Please copy .env.example to .env and add your Groq API key
    pause
    exit /b 1
)

REM Start the server
cd backend
python main.py

pause
'''
        with open("start_server.bat", "w") as f:
            f.write(script_content)
        print("✅ Windows launch script created (start_server.bat)")
        
    else:
        # Unix shell script
        script_content = '''#!/bin/bash
echo "Starting Syntax Shift Server..."
echo

# Activate virtual environment
source syntax_shift_env/bin/activate

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "Please copy .env.example to .env and add your Groq API key"
    exit 1
fi

# Start the server
cd backend
python main.py
'''
        with open("start_server.sh", "w") as f:
            f.write(script_content)
        
        # Make executable
        os.chmod("start_server.sh", 0o755)
        print("✅ Unix launch script created (start_server.sh)")

def print_next_steps():
    """Print instructions for next steps"""
    print("\n" + "=" * 60)
    print("🎉 SETUP COMPLETE!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Get a free Groq API key from: https://console.groq.com")
    print("2. Copy .env.example to .env")
    print("3. Add your API key to the .env file")
    print("4. Run the launch script:")
    
    if platform.system() == "Windows":
        print("   → Double-click start_server.bat")
    else:
        print("   → ./start_server.sh")
    
    print("5. Open http://localhost:8000 in your browser")
    print()
    print("📚 For detailed instructions, see README.md")
    print("🐛 Issues? Visit: https://github.com/yourusername/syntax-shift/issues")
    print()
    print("Happy coding! 🚀")

def main():
    """Main setup function"""
    try:
        print_header()
        check_python_version()
        create_directory_structure()
        
        venv_name = create_virtual_environment()
        if not venv_name:
            print("❌ Setup failed: Could not create virtual environment")
            sys.exit(1)
        
        if not install_dependencies(venv_name):
            print("❌ Setup failed: Could not install dependencies")
            sys.exit(1)
        
        create_env_file()
        create_launch_script()
        print_next_steps()
        
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()