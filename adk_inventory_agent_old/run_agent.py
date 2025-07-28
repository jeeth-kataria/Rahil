#!/usr/bin/env python3
"""
Quick start script for the ADK Inventory Agent

This script provides easy commands to set up and run the agent.
"""

import sys
import subprocess
import os
from pathlib import Path

def check_virtual_env():
    """Check if we're in a virtual environment."""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def install_requirements():
    """Install required packages."""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def check_env_file():
    """Check if .env file is properly configured."""
    if not Path(".env").exists():
        print("❌ .env file not found")
        return False
    
    with open(".env", "r") as f:
        content = f.read()
        if "your-project-id" in content:
            print("⚠️  Please update .env file with your actual Google Cloud project ID")
            return False
    
    print("✅ Environment configuration looks good")
    return True

def run_agent():
    """Start the ADK web interface."""
    print("🚀 Starting ADK Inventory Agent...")
    print("💡 Open http://localhost:8000 in your browser")
    print("🛑 Press Ctrl+C to stop the agent")

    try:
        # Try to run from current directory first
        subprocess.run(["adk", "web"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start agent from current directory: {e}")
        try:
            # Fallback: try from parent directory
            print("🔄 Trying from parent directory...")
            parent_dir = Path.cwd().parent
            subprocess.run(["adk", "web"], cwd=parent_dir, check=True)
        except subprocess.CalledProcessError as e2:
            print(f"❌ Failed to start agent from parent directory: {e2}")
            print("Make sure you have installed google-adk and configured authentication")
            print("\n🔧 Alternative: Try running directly with:")
            print("   adk web")
            print("   or")
            print("   python -m google.adk.cli web")
    except KeyboardInterrupt:
        print("\n🛑 Agent stopped by user")

def main():
    """Main entry point."""
    print("🤖 ADK Inventory Agent Startup Script")
    print("=" * 40)
    
    # Check virtual environment
    if not check_virtual_env():
        print("⚠️  Warning: Not running in a virtual environment")
        print("   Recommend: python -m venv .venv && source .venv/bin/activate")
    
    # Install requirements if needed
    try:
        import google.adk
        print("✅ ADK is installed")
    except ImportError:
        print("📦 ADK not found, installing requirements...")
        if not install_requirements():
            sys.exit(1)
    
    # Check environment configuration
    if not check_env_file():
        print("\n🔧 Please configure your .env file first:")
        print("   1. Edit .env file")
        print("   2. Replace 'your-project-id' with your actual Google Cloud project ID")
        print("   3. Run this script again")
        sys.exit(1)
    
    # Start the agent
    print("\n" + "=" * 40)
    run_agent()

if __name__ == "__main__":
    main()
