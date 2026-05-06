import uvicorn
import subprocess
import sys
import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI(title="Data Lie Detector Unified Server")

# Get absolute path to the project root
project_root = os.path.dirname(os.path.abspath(__file__))
landing_dir = os.path.join(project_root, "landing")

# Start Streamlit in the background
@app.on_event("startup")
async def startup_event():
    print("Starting Streamlit background engine...")
    subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", 
         "--server.port", "8502", 
         "--server.address", "0.0.0.0",
         "--server.headless", "true"],
        cwd=project_root
    )

@app.get("/", response_class=HTMLResponse)
async def get_landing():
    with open(os.path.join(landing_dir, "index.html"), "r", encoding="utf-8") as f:
        return f.read()

@app.get("/app")
async def get_app(request: Request):
    host = request.url.hostname or "localhost"
    # Use the active tunnel for the dashboard
    public_app_url = "https://recorders-path-investments-logos.trycloudflare.com"
    return RedirectResponse(url=public_app_url)

# Serve the static files for the landing page
app.mount("/", StaticFiles(directory=landing_dir, html=True), name="landing")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
