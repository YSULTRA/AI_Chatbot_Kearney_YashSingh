#!/usr/bin/env python3
"""
Sugar Commodity AI Chatbot - Universal Launcher
Works on Windows, Mac, and Linux - Zero Config Required
"""

import subprocess
import sys
import os
import time
import platform
from pathlib import Path

def print_banner():
    banner = """
    ========================================
      🍬 Sugar Commodity AI Chatbot
    ========================================
    """
    print(banner)

def print_section(title):
    print(f"\n{'='*50}")
    print(f"  {title}")
    print('='*50)

def run_command(cmd, cwd=None, shell=False):
    """Run command with proper error handling"""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300  # 5 minute timeout
        )
        return result.returncode == 0
    except Exception as e:
        print(f"   Warning: {e}")
        return False

def setup_backend():
    """Setup backend environment"""
    print_section("🔧 Backend Setup")

    backend_dir = Path("chatbot-backend")
    venv_path = backend_dir / "env"

    # Create virtual environment
    if not venv_path.exists():
        print("📦 Creating virtual environment...")
        if run_command([sys.executable, "-m", "venv", str(venv_path)]):
            print("✅ Virtual environment created")
        else:
            print("❌ Failed to create virtual environment")
            return False
    else:
        print("✅ Virtual environment exists")

    # Get pip path
    system = platform.system()
    if system == "Windows":
        pip_exe = venv_path / "Scripts" / "pip.exe"
    else:
        pip_exe = venv_path / "bin" / "pip"

    # Install dependencies
    print("📥 Installing backend dependencies (1-2 minutes)...")
    print("   Installing packages silently...")

    # Upgrade pip first
    run_command([str(pip_exe), "install", "--upgrade", "pip", "--quiet"])

    # Install requirements
    if run_command([str(pip_exe), "install", "-r", "requirements.txt", "--quiet"], cwd=backend_dir):
        print("✅ Backend dependencies installed")
    else:
        print("❌ Failed to install dependencies")
        return False

    # Check .env file
    env_file = backend_dir / ".env"
    if not env_file.exists():
        print("\n⚠️  API Key Required!")
        print("\n   Get your FREE Gemini API key:")
        print("   👉 https://aistudio.google.com/apikey")

        api_key = input("\n   Paste your API key: ").strip()

        if api_key:
            with open(env_file, 'w') as f:
                f.write(f"GEMINI_API_KEY={api_key}\n")
            print("✅ API key saved!")
        else:
            print("\n❌ Cannot start without API key")
            return False
    else:
        print("✅ API key configured")

    return True

def setup_frontend():
    """Setup frontend environment"""
    print_section("🎨 Frontend Setup")

    frontend_dir = Path("chatbot-frontend")
    node_modules = frontend_dir / "node_modules"

    if not node_modules.exists():
        print("📥 Installing frontend dependencies (1-2 minutes)...")
        print("   Installing packages silently...")

        if run_command(["npm", "install", "--silent"], cwd=frontend_dir, shell=True):
            print("✅ Frontend dependencies installed")
            return True
        else:
            print("\n⚠️  Could not install frontend dependencies")
            print("\n   Please install Node.js from: https://nodejs.org/")
            print("   Then restart terminal and run: python start.py")
            return False
    else:
        print("✅ Frontend dependencies exist")
        return True

def start_servers(start_frontend=True):
    """Start servers"""
    print_section("🚀 Starting Servers")

    system = platform.system()
    backend_dir = Path("chatbot-backend").absolute()
    frontend_dir = Path("chatbot-frontend").absolute()

    # Get Python executable path
    if system == "Windows":
        venv_python = backend_dir / "env" / "Scripts" / "python.exe"
    else:
        venv_python = backend_dir / "env" / "bin" / "python"

    # Start backend
    print("🔧 Starting backend server...")
    if system == "Windows":
        batch_content = f'''@echo off
title Backend - Sugar Commodity AI Chatbot
cd /d "{backend_dir}"
"{venv_python}" -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause'''
        batch_file = Path("_start_backend.bat")
        batch_file.write_text(batch_content, encoding='utf-8')
        subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", str(batch_file)], shell=True)
    else:
        cmd = f'cd "{backend_dir}" && "{venv_python}" -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000'
        if system == "Darwin":
            subprocess.Popen(["osascript", "-e", f'tell app "Terminal" to do script "{cmd}"'])
        else:
            subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"{cmd}; exec bash"])

    print("✅ Backend server starting (port 8000)")

    # Wait for backend
    if start_frontend:
        print("\n⏳ Initializing backend (10 seconds)...")
        for i in range(10):
            print(f"   {'▓' * (i+1)}{'░' * (9-i)} {(i+1)*10}%", end='\r')
            time.sleep(1)
        print("\n")

    # Start frontend
    if start_frontend:
        print("🎨 Starting frontend server...")
        if system == "Windows":
            batch_content = f'''@echo off
title Frontend - Sugar Commodity AI Chatbot
cd /d "{frontend_dir}"
npm run dev
pause'''
            batch_file = Path("_start_frontend.bat")
            batch_file.write_text(batch_content, encoding='utf-8')
            subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", str(batch_file)], shell=True)
        else:
            cmd = f'cd "{frontend_dir}" && npm run dev'
            if system == "Darwin":
                subprocess.Popen(["osascript", "-e", f'tell app "Terminal" to do script "{cmd}"'])
            else:
                subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"{cmd}; exec bash"])

        print("✅ Frontend server starting (port 3000)")

def main():
    """Main function"""
    try:
        print_banner()

        # Check Python version
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 9):
            print("❌ Python 3.9+ required")
            print(f"   You have: Python {version.major}.{version.minor}.{version.micro}")
            input("\nPress Enter to exit...")
            return

        # Setup backend
        backend_ok = setup_backend()
        if not backend_ok:
            print("\n❌ Backend setup failed")
            input("\nPress Enter to exit...")
            return

        # Setup frontend
        frontend_ok = setup_frontend()

        # Start servers
        start_servers(start_frontend=frontend_ok)

        # Success message
        print_section("✅ Success!")
        print("\n   📱 Open your browser:")
        if frontend_ok:
            print("   🌐 Frontend:  http://localhost:3000")
        print("   🔧 Backend:   http://localhost:8000")
        print("   📚 API Docs:  http://localhost:8000/docs")
        print("\n   💡 Servers running in separate windows")
        print("   💡 Close those windows to stop servers")

        if not frontend_ok:
            print("\n   ⚠️  Start frontend manually:")
            print("       cd chatbot-frontend")
            print("       npm install")
            print("       npm run dev")
        else:
            print("\n   🎯 Try: 'Which supplier has cheapest sugar?'")

        input("\n\nPress Enter to close launcher...")

    except KeyboardInterrupt:
        print("\n\n👋 Cancelled")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        print("\nTry manual setup - see README.md")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
