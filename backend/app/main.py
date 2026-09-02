from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import os
import secrets

from app.core.config import STORAGE_DIR, UPLOADS_DIR, EVIDENCE_DIR, REPORTS_DIR
from app.core.database import init_db
from app.api.routes import router

# Ensure storage directories exist
os.makedirs(STORAGE_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(EVIDENCE_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# Initialize database
init_db()

app = FastAPI(
    title="Nirikshan \u2014 Packaged Commodity Compliance Auditor",
    description="Automated compliance auditor for Legal Metrology Rules",
    version="1.0.0"
)

security = HTTPBasic()

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "nirikshan2024")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Paths relative to main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "..", "..", "web", "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "..", "..", "web", "templates")

# Mount directories
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/storage", StaticFiles(directory=STORAGE_DIR), name="storage")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Include API router
app.include_router(router)

@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    """Serves the Scanner UI at the root path."""
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/dashboard", response_class=HTMLResponse)
async def serve_dashboard(request: Request, username: str = Depends(authenticate_user)):
    """Serves the Dashboard UI."""
    return templates.TemplateResponse(request=request, name="dashboard.html")
