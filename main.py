import uvicorn
import subprocess
import sys
import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI(title="Data Lie Detector Unified Server")

# Get absolute path to the project root
project_root = os.path.dirname(os.path.abspath(__file__))
landing_dir = os.path.join(project_root, "landing")

# Start Streamlit in the background
@app.on_event("startup")
async def startup_event():
    print("Starting Streamlit background engine...")
    # We run Streamlit on 8502, and Replit will automatically make it public
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

from fastapi.responses import RedirectResponse

@app.get("/app")
async def get_app(request: Request):
    # Determine the public URL for the Streamlit engine
    host = request.url.hostname or "localhost"
    
    if "REPL_SLUG" in os.environ:
        slug = os.environ.get("REPL_SLUG")
        owner = os.environ.get("REPL_OWNER", "user")
        public_app_url = f"https://8502.{slug}.{owner}.replit.dev"
    elif "trycloudflare.com" in host:
        # Seamlessly redirect to the analysis engine tunnel
        public_app_url = f"https://productions-translated-workshops-elliott.trycloudflare.com"
    elif not host == "localhost":
        public_app_url = f"https://{host}"
    else:
        public_app_url = f"http://{host}:8502"
    
    return RedirectResponse(url=public_app_url)

# Serve the static files for the landing page
app.mount("/", StaticFiles(directory=landing_dir, html=True), name="landing")

if __name__ == "__main__":
    # Default to 8000 for local development, or use the PORT provided by the hosting platform (e.g. 8080 on Replit)
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Data Lie Detector Gateway on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

