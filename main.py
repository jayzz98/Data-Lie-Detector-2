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

import httpx
from fastapi.responses import StreamingResponse

@app.get("/app")
async def proxy_streamlit_app(request: Request):
    # Proxy the main Streamlit page
    async with httpx.AsyncClient() as client:
        # We reach the internal streamlit server on localhost:8502
        resp = await client.get("http://localhost:8502/")
        return HTMLResponse(content=resp.text)

# We need to catch all Streamlit internal paths (_stcore, static, etc.)
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_all(request: Request, path: str):
    # Skip if it's our own routes or static landing files
    if path == "" or path == "app" or os.path.exists(os.path.join(landing_dir, path)):
        return None # Let the next route handle it
        
    async with httpx.AsyncClient() as client:
        url = f"http://localhost:8502/{path}"
        if request.query_params:
            url += f"?{request.query_params}"
            
        # Forward the request to internal Streamlit
        req = client.build_request(
            method=request.method,
            url=url,
            headers=request.headers.raw,
            content=await request.body()
        )
        resp = await client.send(req, stream=True)
        return StreamingResponse(
            resp.aiter_raw(),
            status_code=resp.status_code,
            headers=dict(resp.headers)
        )

# Serve the static files for the landing page
app.mount("/", StaticFiles(directory=landing_dir, html=True), name="landing")

if __name__ == "__main__":
    # Default to 8000 for local development, or use the PORT provided by the hosting platform (e.g. 8080 on Replit)
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Data Lie Detector Gateway on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

