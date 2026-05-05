import subprocess
import sys
import os
import time

def main():
    print("Starting Data Lie Detector unified server...")
    
    # Get absolute path to the project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    landing_dir = os.path.join(project_root, "landing")
    
    # 1. Start the unified FastAPI server on port 8000
    print(f"Starting unified FastAPI server on http://localhost:8000...")
    landing_server = subprocess.Popen(
        [sys.executable, "main.py"],
        cwd=project_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    # 2. Start the Streamlit app on port 8502
    print(f"Starting Streamlit app on http://localhost:8502...")
    app_server = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8502", "--server.address", "localhost"],
        cwd=project_root
    )
    
    print("\n" + "="*50)
    print("Servers are running!")
    print("Website: http://localhost:8000")
    print("App:     http://localhost:8502")
    print("="*50 + "\n")
    print("Press Ctrl+C to stop both servers.")
    
    try:
        # Keep the main process alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping servers...")
        landing_server.terminate()
        app_server.terminate()
        print("Goodbye!")

if __name__ == "__main__":
    main()
