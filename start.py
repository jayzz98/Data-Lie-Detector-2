import subprocess
import sys
import os
import time
import webbrowser

def start_unified_app():
    print("🚀 Starting Data Lie Detector (Unified One-Link Version)...")
    
    # 1. Kill any existing processes on port 8000
    if os.name == 'nt': # Windows
        subprocess.run("taskkill /F /IM python.exe /T", shell=True, capture_output=True)
    
    # 2. Start Streamlit on the primary port (8000)
    # This serves both the landing page and the app natively
    print("📦 Launching App Engine on http://localhost:8000")
    streamlit_proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", 
         "--server.port", "8000", 
         "--server.address", "0.0.0.0",
         "--server.headless", "true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # Wait for the server to start
    print("⏳ Waiting for server to initialize...")
    time.sleep(5)
    
    # Open the browser
    webbrowser.open("http://localhost:8000")
    
    print("\n✅ System is LIVE at http://localhost:8000")
    print("Press Ctrl+C to stop the servers.")
    
    try:
        while True:
            line = streamlit_proc.stdout.readline()
            if line:
                print(f"[App] {line.strip()}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        streamlit_proc.terminate()

if __name__ == "__main__":
    start_unified_app()
