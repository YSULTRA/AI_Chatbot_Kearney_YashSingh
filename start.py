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
    """Print startup banner"""
    banner = """
    ========================================
      🍬 Sugar Commodity AI Chatbot
    ========================================
    """
    print(banner)

def get_venv_python():
    """Get path to virtual environment Python"""
    system = platform.system()
    venv_path = Path("chatbot-backend") / "env"

    if system == "Windows":
        return venv_path / "Scripts" / "python.exe"
    else:  # Linux/Mac
        return venv_path / "bin" / "python"

def check_requirements():
    """Check if requirements are met"""
    print("🔍 Checking requirements...")

    # Check if backend venv exists
    venv_python = get_venv_python()
    if not venv_python.exists():
        print("❌ Virtual environment not found!")
        print("Please run: cd chatbot-backend && python -m venv env")
        return False

    # Check if frontend node_modules exists
    if not (Path("chatbot-frontend") / "node_modules").exists():
        print("⚠️  Installing frontend dependencies...")
        os.chdir("chatbot-frontend")
        subprocess.run(["npm", "install"], check=True)
        os.chdir("..")

    print("✅ All requirements met!")
    return True

def start_backend():
    """Start backend server"""
    print("\n🚀 Starting Backend Server...")

    system = platform.system()
    backend_dir = Path("chatbot-backend")

    if system == "Windows":
        # Windows: Use start to open new window
        cmd = [
            "cmd", "/c", "start", "cmd", "/k",
            f"cd {backend_dir} && env\\Scripts\\activate && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
        ]
        subprocess.Popen(cmd, shell=True)
    else:
        # Mac/Linux: Use gnome-terminal, xterm, or osascript
        venv_python = get_venv_python()
        cmd = [
            str(venv_python), "-m", "uvicorn",
            "app.main:app", "--reload",
            "--host", "0.0.0.0", "--port", "8000"
        ]

        # Try to open in new terminal
        try:
            if system == "Darwin":  # Mac
                terminal_cmd = f"cd {backend_dir.absolute()} && {' '.join(cmd)}"
                subprocess.Popen([
                    "osascript", "-e",
                    f'tell app "Terminal" to do script "{terminal_cmd}"'
                ])
            else:  # Linux
                subprocess.Popen(["gnome-terminal", "--", "bash", "-c",
                                f"cd {backend_dir} && {' '.join(cmd)}; exec bash"])
        except:
            # Fallback: run in background
            print("⚠️  Running backend in background (no separate window)")
            subprocess.Popen(cmd, cwd=backend_dir)

def start_frontend():
    """Start frontend server"""
    print("\n🎨 Starting Frontend Server...")

    system = platform.system()
    frontend_dir = Path("chatbot-frontend")

    if system == "Windows":
        # Windows: Use start to open new window
        cmd = [
            "cmd", "/c", "start", "cmd", "/k",
            f"cd {frontend_dir} && npm run dev"
        ]
        subprocess.Popen(cmd, shell=True)
    else:
        # Mac/Linux
        try:
            if system == "Darwin":  # Mac
                terminal_cmd = f"cd {frontend_dir.absolute()} && npm run dev"
                subprocess.Popen([
                    "osascript", "-e",
                    f'tell app "Terminal" to do script "{terminal_cmd}"'
                ])
            else:  # Linux
                subprocess.Popen(["gnome-terminal", "--", "bash", "-c",
                                f"cd {frontend_dir} && npm run dev; exec bash"])
        except:
            # Fallback: run in background
            print("⚠️  Running frontend in background (no separate window)")
            subprocess.Popen(["npm", "run", "dev"], cwd=frontend_dir)

def main():
    """Main function"""
    print_banner()

    # Check requirements
    if not check_requirements():
        input("\nPress Enter to exit...")
        sys.exit(1)

    # Start backend
    start_backend()

    # Wait for backend to initialize
    print("\n⏳ Waiting for backend to initialize (10 seconds)...")
    time.sleep(10)

    # Start frontend
    start_frontend()

    # Display info
    print("\n" + "="*50)
    print("  ✅ Both servers are starting!")
    print("="*50)
    print("\n📊 Access your application:")
    print("   Frontend: http://localhost:3000")
    print("   Backend:  http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")
    print("\n💡 Servers are running in separate windows/terminals")
    print("   Close those windows to stop the servers\n")

    input("Press Enter to exit launcher...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)
