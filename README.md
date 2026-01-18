# Profile Playground API & UI

A minimal full-stack playground application that stores my personal candidate profile in a database, exposes it via a small REST API, and provides a lightweight frontend to query and visualize the data.

This project is intentionally simple in UI and focuses on **API design, data modeling, querying, and deployment** rather than visual presentation.

---

## Live URLs

- **Frontend (Netlify)**  
  https://dazzling-tarsier-2add30.netlify.app

- **Backend API (Railway)**  
  https://me-api-playground-production-a75e.up.railway.app

- **Health Check**  
  https://me-api-playground-production-a75e.up.railway.app/health

---

## Architecture Overview

The project follows a straightforward client–server architecture:

- **Backend**
  - FastAPI application
  - SQLite database
  - REST endpoints for profile, projects, skills, and search
  - Hosted on Railway

- **Frontend**
  - Plain HTML + vanilla JavaScript
  - Fetches data from the hosted API
  - Hosted as a static site on Netlify

The frontend is deliberately minimal and exists only to demonstrate that the backend endpoints work correctly and return meaningful data.

---

## Backend Details

### Tech Stack
- Python
- FastAPI
- SQLite
- Uvicorn

### Database Schema

The database is seeded with real personal data and consists of the following tables:

- **profile**
  - Stores basic profile information (name, email, education, links)

- **projects**
  - Stores project title, description, and external link

- **skills**
  - Stores unique skill names

- **project_skills**
  - Join table representing the many-to-many relationship between projects and skills

Schema is defined in `schema.sql`, and data is populated via `seed.py`.

---

### API Endpoints

#### Health
GET /health
Returns 200 OK if the service is live.

---

#### Profile
GET /proflie
- Fetches or updates the stored profile information.

---

#### Projects
GET /projects
GET /projects?skill=Python
- Lists all projects.
- Supports filtering projects by skill.

---

#### Skills
GET /skills/top
- Returns skills ordered by frequency of usage across projects.

---

#### Search
GET /search?q=vision
- Searches across project titles, descriptions, and associated skills.

---

### Rate Limiting

A simple in-memory rate limiter is implemented for write operations.  
Read-only GET requests are intentionally excluded to ensure smooth frontend usage.

---

## Frontend Details

### Tech Stack
- HTML
- Vanilla JavaScript (Fetch API)

### Functionality
- Displays profile information fetched from the backend
- Lists all projects on page load
- Allows:
  - Searching projects by keyword
  - Filtering projects by skill
- Links redirect to external GitHub / project pages

The frontend does not use any framework by design, keeping it transparent and easy to reason about.

---

## Local Setup

### Backend (Local)

```bash
cd backend
pip install -r requirements.txt
python seed.py
uvicorn main:app --reload
```

Backend will be available at:
```sh
http://127.0.0.1:8000
```
Frontend (Local)
Open the following file directly in a browser:
```sh
frontend/index.html
```

To use the local backend, update the API base URL in index.html:
```sh
const API = "http://127.0.0.1:8000";
```

Deployment Notes

-- Backend

-- Deployed on Railway

-- Root directory set to backend

-- Public domain explicitly enabled

Frontend
-- Deployed on Netlify
-- Base directory set to frontend
-- No build step required (static site)

Known Limitations
-- Authentication is minimal and not production-grade.
-- Rate limiting is in-memory and resets on service restart.
-- UI is intentionally basic and unstyled.

These tradeoffs were made to keep the project focused on core backend and deployment fundamentals.

Resume & Links
-- GitHub: https://github.com/Gyokuken
-- LinkedIn: https://www.linkedin.com/in/amitanshu-lal-611248244/
-- Portfolio: https://portfolio-website-lime-two-16.vercel.app/

Summary
This project demonstrates the ability to:
-- Design clean REST APIs
-- Model relational data
-- Implement filtering and search
-- Deploy and expose services publicly
-- Integrate a frontend with a live backend

The scope is intentionally small, readable, and focused on correctness rather than complexity.
