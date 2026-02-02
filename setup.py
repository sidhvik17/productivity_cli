#!/usr/bin/env python3
"""
Setup script and demo for Productivity CLI
"""
import subprocess
import sys
import os
from pathlib import Path


def check_python_version():
    """Ensure Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")


def install_dependencies():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"
        ])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)


def create_data_directory():
    """Ensure data directory exists"""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    print("✓ Data directory created")


def run_demo():
    """Run a demo of the CLI"""
    print("\n" + "=" * 60)
    print("🚀 PRODUCTIVITY CLI DEMO")
    print("=" * 60)
    
    commands = [
        ("Adding a high-priority task", 
         'python main.py task add "Complete project proposal" -p High -d 2026-02-15'),
        
        ("Adding a medium-priority task",
         'python main.py task add "Review pull requests" -p Medium'),
        
        ("Adding a low-priority task",
         'python main.py task add "Update documentation" -p Low -d 2026-02-20'),
        
        ("Listing all tasks",
         'python main.py task list'),
        
        ("Adding food expense",
         'python main.py expense add 25.50 Food -d "Lunch at cafe"'),
        
        ("Adding tech expense",
         'python main.py expense add 89.99 Tech -d "Wireless mouse"'),
        
        ("Adding rent expense",
         'python main.py expense add 1200.00 Rent -d "Monthly rent"'),
        
        ("Listing all expenses",
         'python main.py expense list'),
        
        ("Showing expense breakdown",
         'python main.py expense breakdown'),
        
        ("Checking upcoming deadlines",
         'python main.py reminder check'),
        
        ("Showing dashboard",
         'python main.py dashboard'),
        
        ("Showing weekly analytics",
         'python main.py analytics weekly'),
    ]
    
    for description, command in commands:
        print(f"\n{'─' * 60}")
        print(f"📌 {description}")
        print(f"💻 Command: {command}")
        print(f"{'─' * 60}\n")
        
        os.system(command)
        
        input("\nPress Enter to continue...")
    
    print("\n" + "=" * 60)
    print("✨ Demo completed!")
    print("=" * 60)
    print("\nTry these commands yourself:")
    print("  python main.py --help")
    print("  python main.py task --help")
    print("  python main.py expense --help")
    print("  python main.py analytics --help")
    print("\nEnjoy your productivity CLI! 🚀")


def main():
    """Main setup function"""
    print("=" * 60)
    print("PRODUCTIVITY CLI - SETUP & DEMO")
    print("=" * 60)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Create data directory
    create_data_directory()
    
    print("\n✓ Setup completed successfully!")
    
    # Ask if user wants to run demo
    response = input("\nWould you like to run a demo? (y/n): ").lower().strip()
    
    if response == 'y':
        run_demo()
    else:
        print("\n✨ Setup complete! Run 'python main.py --help' to get started.")


if __name__ == "__main__":
    main()
