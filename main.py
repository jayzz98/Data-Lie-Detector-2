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
    # Render provides the port in the PORT environment variable
    port = os.environ.get("PORT", "8000")
    # We will run Streamlit on a separate internal port
    subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", 
         "--server.port", "8502", 
         "--server.address", "0.0.0.0",
         "--server.headless", "true",
         "--server.enableXsrfProtection", "false",
         "--server.enableCORS", "false"],
        cwd=project_root
    )

@app.get("/", response_class=HTMLResponse)
async def get_landing():
    with open(os.path.join(landing_dir, "index.html"), "r", encoding="utf-8") as f:
        return f.read()

@app.get("/app")
async def get_app(request: Request):
    # On Render, we'll use a direct internal proxy for the app
    # This ensures the user stays on the same domain
    return HTMLResponse(content="""
        <style>body, html { margin: 0; padding: 0; height: 100%; overflow: hidden; }</style>
        <iframe src="/_st" style="border:none; width:100%; height:100%;"></iframe>
    """)

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all_proxy(request: Request, path: str):
    # If it's a known static file or route, let it pass
    if path == "" or path == "app" or os.path.exists(os.path.join(landing_dir, path)):
        # Re-serve landing if root
        if path == "":
             with open(os.path.join(landing_dir, "index.html"), "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())
        return None 

    # Otherwise, proxy to Streamlit
    async with httpx.AsyncClient() as client:
        url = f"http://localhost:8502/{path}"
        if request.query_params:
            url += f"?{request.query_params}"
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
