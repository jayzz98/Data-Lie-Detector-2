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

@app.get("/app")
async def get_app(request: Request):
    # Detect the public URL from Replit environment or use local host
    if "REPL_SLUG" in os.environ:
        slug = os.environ.get("REPL_SLUG")
        owner = os.environ.get("REPL_OWNER", "user")
        public_app_url = f"https://8502.{slug}.{owner}.replit.dev"
    else:
        host = request.url.hostname or "localhost"
        public_app_url = f"http://{host}:8502"
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Data Lie Detector - Dashboard</title>
        <link rel="icon" href="/favicon.ico">
        <style>
            body, html {{ margin: 0; padding: 0; height: 100%; overflow: hidden; background: #0a0a1a; }}
            iframe {{ width: 100%; height: 100%; border: none; }}
        </style>
    </head>
    <body>
        <iframe src="{public_app_url}/?embedded=true"></iframe>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Serve the static files for the landing page
app.mount("/", StaticFiles(directory=landing_dir, html=True), name="landing")

if __name__ == "__main__":
    # Default to 8000 for local development, or use the PORT provided by the hosting platform (e.g. 8080 on Replit)
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Data Lie Detector Gateway on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

