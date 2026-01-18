CREATE TABLE profile (
  id INTEGER PRIMARY KEY,
  name TEXT,
  email TEXT,
  education TEXT,
  github TEXT,
  linkedin TEXT,
  portfolio TEXT
);

CREATE TABLE skills (
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE
);

CREATE TABLE projects (
  id INTEGER PRIMARY KEY,
  title TEXT,
  description TEXT,
  link TEXT
);

CREATE TABLE project_skills (
  project_id INTEGER,
  skill_id INTEGER
);
