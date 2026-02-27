# PythonIILabs

Python II lab exercises for IEMCSBT Term 2.

## What's Inside

**EcoMute Bike Sharing API** — a REST API built with [FastAPI](https://fastapi.tiangolo.com/) featuring:

- **Bikes** — CRUD operations for bike inventory
- **Users** — user management endpoints
- **Rentals** — bike rental workflows
- Pydantic schemas for request/response validation
- Mock data sources for development

## Run Locally

```bash
pip install fastapi uvicorn
uvicorn src.main:app --reload
```

API docs available at `http://127.0.0.1:8000/docs`

---

## gh CLI Commands Used to Create & Push This Repo

```bash
# 1. Create the repo on GitHub (public, with description)
gh repo create PythonIILabs --public --description "Python II lab exercises"

# 2. Add the new repo as a remote
git remote add origin https://github.com/kevinleonj/PythonIILabs.git

# 3. Push local commits to GitHub
git push -u origin master
```

### Other Useful gh Commands

```bash
# Check your auth status
gh auth status

# List your repos
gh repo list

# View this repo in the browser
gh repo view --web

# Clone a repo
gh repo clone kevinleonj/PythonIILabs
```
