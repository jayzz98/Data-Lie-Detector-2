import uvicorn
import subprocess
import sys
import os
from fastapi import FastAPI
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

@app.get("/app")
async def get_app():
    # Detect the public URL from Replit environment or use a placeholder
    # Replit provides the public URL in REPL_SLUG and REPL_OWNER
    slug = os.environ.get("REPL_SLUG", "data-lie-detector")
    owner = os.environ.get("REPL_OWNER", "user")
    
    # Replit's multi-port URL pattern: port-number.slug.owner.repl.co
    public_app_url = f"https://8502.{slug}.{owner}.replit.dev"
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Data Lie Detector - Dashboard</title>
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
    # Replit's main port is usually 8080
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting Data Lie Detector Gateway on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
