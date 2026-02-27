# PythonIILabs

Python II lab exercises for IEMCSBT Term 2.

## What's Inside

**EcoMute Bike Sharing API** — a REST API built with [FastAPI](https://fastapi.tiangolo.com/) featuring:

- **Bikes** (`/bikes`) — full CRUD for bike inventory with status filtering (available / rented / maintenance)
- **Users** (`/users`) — user management with CRUD endpoints
- **Rentals** (`/rentals`) — rental processing with battery-level validation (rejects < 20%)
- **Admin** (`/admin`) — protected stats endpoint secured with API key header auth
- Pydantic schemas with field validators (battery range, password strength, email format)
- Dependency injection for data sources
- In-memory mock data store (to be replaced with SQL in later sessions)

## Project Structure

```
src/
├── main.py                      # FastAPI app entry point, router registration
├── app/
│   ├── routers/
│   │   ├── bikes.py             # GET, POST, PUT, DELETE /bikes
│   │   ├── users.py             # GET, POST, PUT, DELETE /users
│   │   ├── rentals.py           # POST /rentals
│   │   └── admin.py             # GET /admin/stats (API key required)
│   ├── schemas/
│   │   ├── bikes.py             # BikeBase, BikeCreate, BikeResponse
│   │   ├── users.py             # UserCreate, UserResponse, UserSignUp
│   │   └── rentals.py           # RentalOutcome, RentalProcessing
│   └── data/
│       ├── mocks.py             # In-memory BIKES and USERS lists
│       ├── bikes_data_source.py # BikesDataSource class (CRUD logic)
│       └── users_data_source.py # UsersDataSource class (CRUD logic)
```

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/bikes` | List all bikes (optional `?status=` filter) |
| GET | `/bikes/{bike_id}` | Get a single bike |
| POST | `/bikes` | Create a new bike |
| PUT | `/bikes/{bike_id}` | Update a bike |
| DELETE | `/bikes/{bike_id}` | Delete a bike |
| GET | `/users` | List all users |
| GET | `/users/{user_id}` | Get a single user |
| POST | `/users` | Create a new user |
| PUT | `/users/{user_id}` | Update a user |
| DELETE | `/users/{user_id}` | Delete a user |
| POST | `/rentals` | Process a rental (battery must be ≥ 20%) |
| GET | `/admin/stats` | Admin stats (requires `api-key` header) |

## Run Locally

```bash
pip install fastapi uvicorn
uvicorn src.main:app --reload
```

API docs available at `http://127.0.0.1:8000/docs`

---

## Git Commands Reference

### Initial Setup

```bash
# Configure your identity (once per machine)
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Initialize a new repo in the current folder
git init

# Clone an existing repo
git clone https://github.com/kevinleonj/PythonIILabs.git
```

### Daily Workflow

```bash
# Check which files have changed
git status

# See the actual changes line by line
git diff

# Stage specific files for commit
git add filename.py

# Stage all changed files
git add .

# Commit staged changes with a message
git commit -m "Add rental endpoint validation"

# Push commits to GitHub
git push

# Pull latest changes from GitHub
git pull
```

### Viewing History

```bash
# See commit history
git log

# Compact one-line log
git log --oneline

# See log with a graph of branches
git log --oneline --graph --all

# See what changed in a specific commit
git show <commit-hash>

# See changes between two commits
git diff <commit1> <commit2>
```

### Branching

```bash
# List all branches
git branch

# Create a new branch
git branch feature-name

# Switch to a branch
git checkout feature-name

# Create and switch in one step
git checkout -b feature-name

# Merge a branch into your current branch
git merge feature-name

# Delete a branch (after merging)
git branch -d feature-name
```

### Undoing Things

```bash
# Unstage a file (keep the changes, just remove from staging)
git restore --staged filename.py

# Discard changes in a file (revert to last commit)
git restore filename.py

# Amend the last commit message
git commit --amend -m "New message"

# Undo the last commit but keep the changes staged
git reset --soft HEAD~1

# Undo the last commit and unstage the changes
git reset HEAD~1
```

### Remote Repos

```bash
# See your remotes
git remote -v

# Add a remote
git remote add origin https://github.com/kevinleonj/PythonIILabs.git

# Push and set upstream (first push to a new branch)
git push -u origin master

# Fetch changes without merging
git fetch

# Pull (fetch + merge)
git pull origin master
```

### Stashing (save work temporarily)

```bash
# Stash your uncommitted changes
git stash

# List all stashes
git stash list

# Re-apply the most recent stash
git stash pop

# Apply a specific stash
git stash apply stash@{1}

# Drop a stash
git stash drop stash@{0}
```

### Tags (mark releases / milestones)

```bash
# Create a tag
git tag v1.0

# Create an annotated tag with a message
git tag -a v1.0 -m "First release"

# List tags
git tag

# Push tags to GitHub
git push --tags
```

### Useful Inspection Commands

```bash
# See who changed each line of a file
git blame filename.py

# Search commit messages for a keyword
git log --grep="rental"

# See a summary of changes per commit
git log --stat

# Show all files tracked by git
git ls-files
```

---

## gh CLI Commands

### Repo Setup (used to create this repo)

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
