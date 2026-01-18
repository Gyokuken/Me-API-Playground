from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from db import get_db

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

import time
from fastapi import Request, HTTPException

RATE_LIMIT = {}
MAX_REQUESTS = 20
WINDOW = 60  # seconds



import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


security = HTTPBasic()

USERNAME = "admin"
PASSWORD = "changeme"

def check_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    client = request.client
    ip = client.host if client else "unknown"

    now = time.time()
    window_start = now - WINDOW

    requests = RATE_LIMIT.get(ip, [])
    requests = [t for t in requests if t > window_start]

    if len(requests) >= MAX_REQUESTS:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    requests.append(now)
    RATE_LIMIT[ip] = requests

    return await call_next(request)


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/profile")
def get_profile():
    logger.info("GET /profile called")
    db = get_db()
    profile = db.execute("SELECT * FROM profile").fetchone()
    db.close()
    return dict(profile) if profile else {}


@app.get("/projects")
def get_projects(skill: str | None = None):
    db = get_db()

    if skill:
        rows = db.execute("""
        SELECT p.*
        FROM projects p
        JOIN project_skills ps ON p.id = ps.project_id
        JOIN skills s ON s.id = ps.skill_id
        WHERE s.name LIKE ?
        """, (f"%{skill}%",)).fetchall()
    else:
        rows = db.execute("SELECT * FROM projects").fetchall()

    db.close()
    return [dict(r) for r in rows]

@app.get("/skills/top")
def top_skills():
    db = get_db()
    rows = db.execute("""
    SELECT s.name, COUNT(*) as count
    FROM skills s
    JOIN project_skills ps ON s.id = ps.skill_id
    GROUP BY s.id
    ORDER BY count DESC
    """).fetchall()
    db.close()
    return [dict(r) for r in rows]

@app.get("/search")
def search(q: str = Query(...)):
    db = get_db()
    rows = db.execute("""
    SELECT DISTINCT p.*
    FROM projects p
    LEFT JOIN project_skills ps ON p.id = ps.project_id
    LEFT JOIN skills s ON s.id = ps.skill_id
    WHERE p.title LIKE ?
       OR p.description LIKE ?
       OR s.name LIKE ?
    """, (f"%{q}%", f"%{q}%", f"%{q}%")).fetchall()
    db.close()
    return [dict(r) for r in rows]


@app.put("/profile")
def update_profile(payload: dict, _: None = Depends(check_auth)):

    db = get_db()
    db.execute("""
        UPDATE profile
        SET name = ?, email = ?, education = ?, github = ?, linkedin = ?, portfolio = ?
        WHERE id = 1
    """, (
        payload["name"],
        payload["email"],
        payload["education"],
        payload["github"],
        payload["linkedin"],
        payload["portfolio"]
    ))
    db.commit()
    db.close()
    return {"status": "updated"}
