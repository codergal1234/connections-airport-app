#!/usr/bin/env python3
"""
Deployment helper for Connections Airport App
"""

import os
import subprocess
import sys

def check_git():
    """Check if git is installed and initialized"""
    try:
        subprocess.run(['git', '--version'], check=True, capture_output=True)
        print("✅ Git is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git is not installed. Please install Git first.")
        return False

def init_git():
    """Initialize git repository if not already done"""
    if not os.path.exists('.git'):
        subprocess.run(['git', 'init'])
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', 'Initial commit: Connections Airport App'])
        print("✅ Git repository initialized")
    else:
        print("✅ Git repository already exists")

def create_github_repo():
    """Instructions for creating GitHub repository"""
    print("\n📝 To deploy your app:")
    print("1. Go to https://github.com/new")
    print("2. Create a new repository named 'connections-airport-app'")
    print("3. Don't initialize with README (we already have one)")
    print("4. Copy the repository URL")
    print("5. Run these commands:")
    print("   git remote add origin YOUR_REPO_URL")
    print("   git push -u origin main")

def deploy_to_railway():
    """Instructions for Railway deployment"""
    print("\n🚀 To deploy to Railway:")
    print("1. Go to https://railway.app")
    print("2. Sign up with your GitHub account")
    print("3. Click 'New Project'")
    print("4. Select 'Deploy from GitHub repo'")
    print("5. Choose your 'connections-airport-app' repository")
    print("6. Railway will automatically deploy your app")
    print("7. Get your public URL from the Railway dashboard")

def main():
    print("🛫 Connections Airport App - Deployment Helper")
    print("=" * 50)
    
    if not check_git():
        sys.exit(1)
    
    init_git()
    create_github_repo()
    deploy_to_railway()
    
    print("\n🎉 Once deployed, share your Railway URL with friends!")
    print("Example: https://connections-airport-app.railway.app")

if __name__ == "__main__":
    main() 