#!/usr/bin/env python3
"""
Quick Start Script for AI Dungeon Master
This script helps users set up the project quickly and safely.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_banner():
    """Print the project banner"""
    print("🎲 AI Dungeon Master - Quick Start")
    print("=" * 50)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        sys.exit(1)
    print("✅ Python version:", sys.version.split()[0])

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        "flask",
        "google-cloud-firestore", 
        "google-auth",
        "python-dotenv"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} (missing)")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def check_config_files():
    """Check if configuration files exist"""
    print("\n⚙️  Checking configuration...")
    
    # Check if adk.yaml exists
    if Path("adk.yaml").exists():
        print("✅ adk.yaml found")
    else:
        print("❌ adk.yaml not found")
        return False
    
    # Check service account key
    service_account_path = Path("config/service-account-key.json")
    if service_account_path.exists():
        try:
            with open(service_account_path, 'r') as f:
                data = json.load(f)
            
            # Check if it's the template or real credentials
            if data.get("project_id") == "YOUR_PROJECT_ID":
                print("⚠️  service-account-key.json contains template values")
                print("   Please replace with your actual Firebase credentials")
                return False
            else:
                print("✅ service-account-key.json configured")
        except json.JSONDecodeError:
            print("❌ service-account-key.json is not valid JSON")
            return False
    else:
        print("❌ service-account-key.json not found")
        return False
    
    return True

def setup_environment():
    """Set up environment variables"""
    print("\n🔧 Setting up environment...")
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        with open(env_file, 'w') as f:
            f.write("# Environment variables for AI Dungeon Master\n")
            f.write("# Add your configuration here\n\n")
            f.write("# Debug mode (optional)\n")
            f.write("# DEBUG=1\n\n")
            f.write("# Custom port (optional)\n")
            f.write("# FLASK_PORT=5001\n")
        print("✅ Created .env file")
    else:
        print("✅ .env file exists")

def run_tests():
    """Run basic tests to verify setup"""
    print("\n🧪 Running basic tests...")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_config_loading.py", "-v"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Basic tests passed")
            return True
        else:
            print("❌ Basic tests failed")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎉 Setup complete!")
    print("=" * 50)
    print("\n📋 Next steps:")
    print("1. Start the application:")
    print("   python start_app.py")
    print()
    print("2. Open your browser to: http://localhost:5001")
    print()
    print("3. Create a new campaign and start playing!")
    print()
    print("📚 Documentation:")
    print("- README.md - Main documentation")
    print("- DEVELOPMENT.md - Technical details")
    print("- SECURITY.md - Security guidelines")
    print()
    print("🔧 Development:")
    print("- Run tests: pytest")
    print("- Format code: black .")
    print("- Lint code: flake8 .")
    print()
    print("⚠️  Important:")
    print("- Never commit real credentials to version control")
    print("- Keep your Firebase credentials secure")
    print("- Update .env file for production deployment")

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    check_python_version()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies and try again.")
        sys.exit(1)
    
    # Check configuration
    if not check_config_files():
        print("\n❌ Please configure your Firebase credentials and try again.")
        print("See README.md for setup instructions.")
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Run tests
    if not run_tests():
        print("\n⚠️  Tests failed, but you can still try running the application.")
        print("Check the error messages above for issues.")
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main() 