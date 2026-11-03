# Two-Tier Flask DevOps Project

A production-style DevOps project built for learning and portfolio purposes. A Flask + MySQL task management application, fully containerized with Docker, version-controlled on GitHub, and automatically tested and deployed via a Jenkins CI/CD pipeline.

---

## Project Status

- [x] Phase 1: Flask + MySQL application
- [x] Phase 2: Docker containerization
- [x] Phase 3: Git + GitHub
- [x] Phase 4: Jenkins CI/CD setup
- [x] Phase 5: Automated pipeline with GitHub webhook
- [ ] Phase 6: AWS EC2 deployment (planned)

---

## Tech Stack

| Technology              | Role                                |
| ----------------------- | ----------------------------------- |
| Python 3.12 + Flask     | REST API and application logic      |
| MySQL 8.0               | Persistent data storage             |
| Docker + Docker Compose | Containerization and orchestration  |
| Jenkins                 | CI/CD automation server             |
| GitHub                  | Version control and webhook trigger |
| ngrok                   | Local webhook tunnel (development)  |
| AWS EC2                 | Cloud deployment (planned)          |

---

## Architecture

### Two-Tier Application

```
Client (browser / curl / Postman)
        │
        ▼
┌───────────────┐
│   Flask App   │  ← Tier 1: Application (port 5000)
│   REST API    │
└───────┬───────┘
        │ Docker internal network
        ▼
┌───────────────┐
│     MySQL     │  ← Tier 2: Data (port 3306)
│   Database    │
└───────────────┘
```

### CI/CD Workflow

```
Developer
    │
    │ git push
    ▼
 GitHub
    │
    │ webhook (automatic trigger)
    ▼
 Jenkins
    ├── Fix Docker Socket
    ├── Checkout code
    ├── Install dependencies
    ├── Run automated tests (6 tests)
    ├── Build Docker image
    ├── Deploy via Docker Compose
    └── Verify app is running (/health)
```

### Container Layout

```
Docker Desktop
│
├── taskmanager-jenkins     Jenkins CI server        (port 8080)
├── jenkins-mysql           MySQL for CI tests only
├── taskmanager-mysql       App database             (port 3306)
└── taskmanager-flask       Flask application        (port 5000)
```

---

## Project Structure

```
two-tier-flask-devops/
├── app/
│   ├── __init__.py          Flask app factory
│   ├── config.py            Configuration from environment variables
│   ├── db.py                MySQL connection and schema init
│   ├── models.py            CRUD operations
│   └── routes.py            API endpoints (Blueprint)
├── tests/
│   └── test_app.py          Automated tests (pytest)
├── jenkins/
│   └── Dockerfile           Custom Jenkins image (Python + Docker CLI)
├── run.py                   Application entry point
├── requirements.txt         Python dependencies
├── Dockerfile               Flask app Docker image
├── docker-compose.yml       App stack (Flask + MySQL)
├── docker-compose.jenkins.yml  CI stack (Jenkins + test MySQL)
├── Jenkinsfile              CI/CD pipeline definition
├── .env.example             Environment variable template
├── .gitignore
└── README.md
```

---

## API Endpoints

| Method | Endpoint      | Description    | Status Code |
| ------ | ------------- | -------------- | ----------- |
| GET    | `/health`     | Health check   | 200         |
| GET    | `/tasks`      | List all tasks | 200         |
| GET    | `/tasks/<id>` | Get one task   | 200 / 404   |
| POST   | `/tasks`      | Create a task  | 201 / 400   |
| PUT    | `/tasks/<id>` | Update a task  | 200 / 404   |
| DELETE | `/tasks/<id>` | Delete a task  | 204 / 404   |

### Request body for POST and PUT

```json
{
  "title": "Task title (required)",
  "description": "Optional description",
  "status": "pending or done (PUT only)"
}
```

---

## Local Setup

### Prerequisites

- Windows 10/11
- Docker Desktop (with WSL2 backend)
- Python 3.12+
- Git
- VS Code (recommended)

### 1. Clone the repository

```bash
git clone https://github.com/humblebee22/two-tier-flask-devops.git
cd two-tier-flask-devops
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Edit .env and fill in your values
```

### 3. Start the application

```bash
docker compose up -d
```

App runs at `http://localhost:5000`

### 4. Start Jenkins (optional)

```bash
docker compose -f docker-compose.jenkins.yml up -d
```

Jenkins runs at `http://localhost:8080`

### 5. Run tests locally

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m pytest tests/test_app.py -v
```

---

## Environment Variables

Copy `.env.example` to `.env` and fill in your values. Never commit `.env` to Git.

| Variable           | Description          | Example                                 |
| ------------------ | -------------------- | --------------------------------------- |
| `MYSQL_HOST`       | MySQL hostname       | `localhost` (native) / `mysql` (Docker) |
| `MYSQL_PORT`       | MySQL port           | `3306`                                  |
| `MYSQL_USER`       | MySQL username       | `root`                                  |
| `MYSQL_PASSWORD`   | MySQL password       | your password                           |
| `MYSQL_DATABASE`   | Database name        | `taskdb`                                |
| `FLASK_SECRET_KEY` | Flask session secret | any random string                       |
| `FLASK_DEBUG`      | Debug mode           | `True` (dev) / `False` (Docker)         |

---

## CI/CD Pipeline

The `Jenkinsfile` defines a 7-stage declarative pipeline:

| Stage                | What it does                                              |
| -------------------- | --------------------------------------------------------- |
| Fix Docker Socket    | Grants Jenkins permission to run Docker commands          |
| Checkout             | Pulls latest code from GitHub                             |
| Install Dependencies | Creates fresh venv, installs from requirements.txt        |
| Run Tests            | Runs pytest — pipeline stops here if any test fails       |
| Build Docker Image   | Builds `taskmanager-flask:latest` image                   |
| Deploy               | Tears down old containers, brings up new ones via Compose |
| Verify               | Hits `/health` endpoint to confirm app is live            |

### Automatic triggering

A GitHub webhook triggers Jenkins automatically on every push (requires ngrok locally, permanent on EC2).

### Jenkins credentials required

Add these as Secret text in Jenkins → Manage Jenkins → Credentials:

| ID                 | Value                    |
| ------------------ | ------------------------ |
| `mysql-password`   | Your MySQL root password |
| `mysql-user`       | `root`                   |
| `mysql-database`   | `taskdb`                 |
| `flask-secret-key` | Your Flask secret key    |

---

## Daily Startup Sequence

| Step | Action                                                        |
| ---- | ------------------------------------------------------------- |
| 1    | Open Docker Desktop, wait for engine to start                 |
| 2    | `cd D:\taskmanager26`                                         |
| 3    | `docker compose up -d`                                        |
| 4    | `docker compose -f docker-compose.jenkins.yml up -d`          |
| 5    | `docker ps` — verify all 4 containers running                 |
| 6    | `Invoke-RestMethod -Uri "http://localhost:5000/health"`       |
| 7    | _(Optional)_ `ngrok http 8080` then update GitHub webhook URL |

---

## Testing the API (PowerShell)

```powershell
# Health check
Invoke-RestMethod -Uri "http://localhost:5000/health"

# List all tasks
Invoke-RestMethod -Uri "http://localhost:5000/tasks"

# Create a task
Invoke-RestMethod -Uri "http://localhost:5000/tasks" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"title": "My task", "description": "Details here"}'

# Update a task
Invoke-RestMethod -Uri "http://localhost:5000/tasks/1" `
  -Method PUT `
  -ContentType "application/json" `
  -Body '{"title": "Updated", "status": "done"}'

# Delete a task
Invoke-RestMethod -Uri "http://localhost:5000/tasks/1" -Method DELETE
```

---

## Viewing the Database

```powershell
# Open MySQL shell
docker exec -it taskmanager-mysql mysql -u root -pdevpassword taskdb

# Quick query without entering shell
docker exec taskmanager-mysql mysql -u root -pdevpassword taskdb -e "SELECT * FROM tasks;"
```

---

## Key Design Decisions

**Why JSON API over server-rendered HTML** — lighter Docker image, easier to test, decoupled from any frontend, better fit for DevOps learning goals.

**Why `python:3.12-slim`** — roughly 5x smaller than the full Python image, reducing build time, pull time, and memory usage on a resource-limited development machine.

**Why layer ordering in Dockerfile** — `COPY requirements.txt` before `COPY . .` means the dependency install layer is cached and only rebuilds when `requirements.txt` changes, not on every code change.

**Why named volumes** — container filesystems are ephemeral (destroyed with the container). Named volumes (`mysql-data`) live outside any container's lifecycle, so database data survives `docker compose down` and redeployment.

**Why `name: taskmanager` in docker-compose.yml** — locks the Compose project name so volume and network names are consistent whether the stack is started manually or by Jenkins from its own workspace directory.

**Why `depends_on` with healthcheck** — without it, Flask starts before MySQL finishes initializing and crashes. The healthcheck makes Flask wait until MySQL actually accepts connections.

**Why parameterized SQL queries** — prevents SQL injection. Never concatenate user input directly into SQL strings.

**Why pipeline as code (Jenkinsfile in Git)** — pipeline changes are versioned alongside application code, any Jenkins server can pick up and run the pipeline, no manual UI editing required.

---

## Documentation

Full learning documentation and error reference available in the `docs/` folder:

- `devops-project-documentation.md` — complete concept explanations, architecture, file reference, commands
- `devops-errors-and-fixes.md` — all 16 errors encountered, root causes, and fixes applied

---

## Author

Kartik Goswami — B.Tech Final Year, ADGIPS Delhi  
GitHub: [@humblebee22](https://github.com/humblebee22)
