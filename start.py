import subprocess
import sys
import os
import time
import webbrowser

def start_servers():
    print("Starting Data Lie Detector Gateway and App Engine...")
    
    # Get absolute path to the project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Kill any existing processes (Windows)
    if os.name == 'nt':
        subprocess.run("taskkill /F /IM python.exe /T", shell=True, capture_output=True)
    
    # 2. Start the FastAPI Gateway (Port 8000)
    # This serves the landing page and proxies the app
    print("Launching Gateway on http://localhost:8000")
    gateway_proc = subprocess.Popen(
        [sys.executable, "main.py"],
        cwd=project_root
    )
    
    # Wait for the gateway to start
    time.sleep(3)
    
    # Open the browser to the gateway
    webbrowser.open("http://localhost:8000")
    
    print("\nSystem is LIVE at http://localhost:8000")
    print("Press Ctrl+C to stop the servers.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping servers...")
        gateway_proc.terminate()

if __name__ == "__main__":
    start_servers()
