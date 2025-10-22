#!/usr/bin/env python3
"""
Sugar Commodity AI Chatbot - Universal Launcher
Works on Windows, Mac, and Linux
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

def check_python():
    """Check Python version"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9+ required. You have Python {}.{}.{}".format(
            version.major, version.minor, version.micro))
        print("   Download from: https://www.python.org/downloads/")
        return False
    return True

def get_venv_python():
    """Get path to virtual environment Python"""
    system = platform.system()
    venv_path = Path("chatbot-backend") / "env"

    if system == "Windows":
        return venv_path / "Scripts" / "python.exe"
    else:
        return venv_path / "bin" / "python"

def setup_backend():
    """Setup backend environment"""
    print_section("🔧 Backend Setup")

    backend_dir = Path("chatbot-backend")
    venv_path = backend_dir / "env"
    venv_python = get_venv_python()

    # Create virtual environment
    if not venv_path.exists():
        print("📦 Creating virtual environment...")
        subprocess.run(
            [sys.executable, "-m", "venv", str(venv_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        print("✅ Virtual environment created")
    else:
        print("✅ Virtual environment exists")

    # Install dependencies (silent)
    print("📥 Installing backend dependencies...")
    print("   (This runs silently, please wait 1-2 minutes)")

    subprocess.run(
        [str(venv_python), "-m", "pip", "install", "--upgrade", "pip", "--quiet"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    subprocess.run(
        [str(venv_python), "-m", "pip", "install", "-r",
         str(backend_dir / "requirements.txt"), "--quiet"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )

    print("✅ Backend dependencies installed")

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
            input("\nPress Enter to exit...")
            sys.exit(1)
    else:
        print("✅ API key configured")

def setup_frontend():
    """Setup frontend environment - with better error handling"""
    print_section("🎨 Frontend Setup")

    frontend_dir = Path("chatbot-frontend")
    node_modules = frontend_dir / "node_modules"

    # Try to install frontend dependencies
    if not node_modules.exists():
        print("📥 Installing frontend dependencies...")
        print("   (This runs silently, please wait 1-2 minutes)")

        try:
            # Try with npm
            subprocess.run(
                ["npm", "install", "--silent"],
                cwd=frontend_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
                shell=True  # Important for Windows
            )
            print("✅ Frontend dependencies installed")
        except Exception as e:
            # If npm fails, give helpful message
            print("\n⚠️  Could not install frontend dependencies")
            print("\n   This usually means Node.js is not in your PATH")
            print("\n   Quick fix:")
            print("   1. Open NEW terminal/PowerShell")
            print("   2. Run: cd chatbot-frontend")
            print("   3. Run: npm install")
            print("   4. Then run: python start.py again")
            print("\n   OR just start frontend manually:")
            print("   1. Open terminal in chatbot-frontend folder")
            print("   2. Run: npm run dev")

            # Ask if user wants to continue with just backend
            choice = input("\n   Continue with BACKEND only? (y/n): ").lower()
            if choice != 'y':
                input("\nPress Enter to exit...")
                sys.exit(1)
            return False  # Signal that frontend setup failed
    else:
        print("✅ Frontend dependencies exist")

    return True  # Frontend setup succeeded

def start_servers(start_frontend=True):
    """Start servers"""
    print_section("🚀 Starting Servers")

    system = platform.system()
    backend_dir = Path("chatbot-backend").absolute()
    frontend_dir = Path("chatbot-frontend").absolute()
    venv_python = get_venv_python().absolute()

    # Start backend
    print("🔧 Starting backend server...")
    if system == "Windows":
        batch_content = f'''@echo off
title Backend - Sugar Commodity AI Chatbot
cd /d "{backend_dir}"
"{venv_python}" -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause'''
        batch_file = Path("_start_backend.bat")
        batch_file.write_text(batch_content)
        subprocess.Popen(["start", "cmd", "/c", str(batch_file)], shell=True)
    else:
        cmd = f'cd "{backend_dir}" && "{venv_python}" -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000'
        if system == "Darwin":
            subprocess.Popen(["osascript", "-e", f'tell app "Terminal" to do script "{cmd}"'])
        else:
            subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"{cmd}; exec bash"])

    print("✅ Backend starting (port 8000)")

    # Wait for backend
    if start_frontend:
        print("\n⏳ Waiting for backend to initialize...")
        for i in range(10):
            print(f"   {'▓' * (i+1)}{'░' * (9-i)} {(i+1)*10}%", end='\r')
            time.sleep(1)
        print("\n")

    # Start frontend if setup succeeded
    if start_frontend:
        print("🎨 Starting frontend server...")
        if system == "Windows":
            batch_content = f'''@echo off
title Frontend - Sugar Commodity AI Chatbot
cd /d "{frontend_dir}"
npm run dev
pause'''
            batch_file = Path("_start_frontend.bat")
            batch_file.write_text(batch_content)
            subprocess.Popen(["start", "cmd", "/c", str(batch_file)], shell=True)
        else:
            cmd = f'cd "{frontend_dir}" && npm run dev'
            if system == "Darwin":
                subprocess.Popen(["osascript", "-e", f'tell app "Terminal" to do script "{cmd}"'])
            else:
                subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"{cmd}; exec bash"])

        print("✅ Frontend starting (port 3000)")

def main():
    """Main function"""
    try:
        print_banner()

        # Check Python version
        if not check_python():
            input("\nPress Enter to exit...")
            sys.exit(1)

        # Setup backend
        setup_backend()

        # Setup frontend (returns True if successful)
        frontend_ok = setup_frontend()

        # Start servers
        start_servers(start_frontend=frontend_ok)

        # Success
        print_section("✅ Success!")
        print("\n   📱 Open your browser and visit:")
        if frontend_ok:
            print("   🌐 Frontend:  http://localhost:3000")
        print("   🔧 Backend:   http://localhost:8000")
        print("   📚 API Docs:  http://localhost:8000/docs")
        print("\n   💡 Servers are running in separate windows")
        print("   💡 Close those windows to stop servers")

        if not frontend_ok:
            print("\n   ⚠️  Frontend not started - install Node.js and run:")
            print("       cd chatbot-frontend && npm install && npm run dev")
        else:
            print("\n   🎯 Try: 'Which supplier has cheapest sugar?'")

        input("\n\nPress Enter to close launcher...")

    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print("\nCheck README.md for manual setup")
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
