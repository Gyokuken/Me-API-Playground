import sqlite3

conn = sqlite3.connect("data.db")
cur = conn.cursor()

# -------------------------
# CREATE SCHEMA
# -------------------------
with open("schema.sql", "r") as f:
    cur.executescript(f.read())

# -------------------------
# PROFILE (single row)
# -------------------------
cur.execute("""
INSERT INTO profile VALUES (
    1,
    'Amitanshu Lal',
    'amitanshu.lal@nitdelhi.ac.in',
    'B.Tech Computer Science and Engineering, NIT Delhi',
    'https://github.com/Gyokuken',
    'https://www.linkedin.com/in/amitanshu-lal-611248244/',
    'https://portfolio-website-lime-two-16.vercel.app/'
)
""")

# -------------------------
# SKILLS (technical only)
# -------------------------
skills = [
    "Python",
    "C++",
    "JavaScript",
    "TypeScript",
    "SQL",
    "FastAPI",
    "PyTorch",
    "TensorFlow",
    "OpenCV",
    "YOLOv5",
    "Deep Learning",
    "Machine Learning",
    "Computer Vision",
    "Next.js",
    "React",
    "Docker",
    "SQLite",
    "MySQL",
    "MongoDB"
]

for s in skills:
    cur.execute("INSERT INTO skills (name) VALUES (?)", (s,))

# Helper to fetch skill id
def sid(name):
    row = cur.execute(
        "SELECT id FROM skills WHERE name = ?",
        (name,)
    ).fetchone()
    if row is None:
        raise ValueError(f"Skill not found: {name}")
    return row[0]

# -------------------------
# PROJECTS
# -------------------------
projects = [
    (
        "Super-Resolution Enhancement of Solar Magnetograms",
        "Deep learning pipeline using MESR and SwinOIR to generate high-resolution solar magnetograms with over 50 PSNR and ~40% detail fidelity improvement.",
        "https://github.com/Gyokuken/Resolution-Enchancement-of-Solar-Magnetograms"
    ),
    (
        "Football Game Analyser",
        "Python-based football video analytics system achieving over 90% accuracy using YOLOv5 and ByteTrack with visualizations via UMAP and SigLIP embeddings.",
        "https://github.com/Gyokuken/Football-Game-Analyzer-YOLO"
    ),
    (
        "ICISA Conference Website",
        "Full-stack conference portal built with Next.js and TypeScript, achieving 99.9% uptime during peak registration for ICISA 2026.",
        "https://v0-make-homepage-functional.vercel.app/"
    ),
    (
        "Video Classification Model",
        "End-to-end video classification pipeline using VGG16 CNN for feature extraction and LSTM for sequence modeling, achieving 85% accuracy.",
        "https://github.com/Gyokuken/Video-Classification-Model"
    ),
    (
        "Patient Management System",
        "GUI-based hospital patient queue management system implementing multiple priority queue data structures with threaded ICU simulation and performance benchmarking.",
        "https://github.com/Gyokuken/hospital_patients_scheduler"
    ),
    (
        "Portfolio Website",
        "Interactive portfolio website built with Next.js 15, React 19, Three.js, and Framer Motion featuring 3D visuals, animations, and EmailJS contact integration.",
        "https://portfolio-website-lime-two-16.vercel.app/"
    )
]

for title, desc, link in projects:
    cur.execute(
        "INSERT INTO projects (title, description, link) VALUES (?, ?, ?)",
        (title, desc, link)
    )

# -------------------------
# PROJECT ↔ SKILL MAPPING
# -------------------------

# Project IDs (order matters)
SR, FOOTBALL, ICISA, VIDEO, PMS, PORTFOLIO = range(1, 7)

# Super-Resolution Magnetograms
cur.executemany(
    "INSERT INTO project_skills VALUES (?, ?)",
    [
        (SR, sid("Python")),
        (SR, sid("PyTorch")),
        (SR, sid("Deep Learning")),
        (SR, sid("Computer Vision")),
        (SR, sid("Machine Learning")),
    ]
)

# Football Game Analyser
cur.executemany(
    "INSERT INTO project_skills VALUES (?, ?)",
    [
        (FOOTBALL, sid("Python")),
        (FOOTBALL, sid("YOLOv5")),
        (FOOTBALL, sid("Computer Vision")),
        (FOOTBALL, sid("Machine Learning")),
    ]
)

# ICISA Website
cur.executemany(
    "INSERT INTO project_skills VALUES (?, ?)",
    [
        (ICISA, sid("Next.js")),
        (ICISA, sid("React")),
        (ICISA, sid("TypeScript")),
        (ICISA, sid("JavaScript")),
    ]
)

# Video Classification
cur.executemany(
    "INSERT INTO project_skills VALUES (?, ?)",
    [
        (VIDEO, sid("Python")),
        (VIDEO, sid("TensorFlow")),
        (VIDEO, sid("Deep Learning")),
        (VIDEO, sid("Computer Vision")),
    ]
)

# Patient Management System (Python only — correct and intentional)
cur.executemany(
    "INSERT INTO project_skills VALUES (?, ?)",
    [
        (PMS, sid("Python")),
    ]
)

# Portfolio Website
cur.executemany(
    "INSERT INTO project_skills VALUES (?, ?)",
    [
        (PORTFOLIO, sid("Next.js")),
        (PORTFOLIO, sid("React")),
        (PORTFOLIO, sid("TypeScript")),
        (PORTFOLIO, sid("JavaScript")),
    ]
)

conn.commit()
conn.close()
