# Two-Tier Task Management App

A Flask + MySQL task management application built as a hands-on DevOps learning project.

## Tech Stack

- **App:** Python, Flask
- **Database:** MySQL
- **Containerization:** Docker, Docker Compose
- **CI/CD:** Jenkins (in progress)
- **Cloud:** AWS EC2 (planned)

## Architecture

Developer → GitHub → Jenkins CI/CD → Docker Image → Deployment
Flask Container ↔ MySQL Container

## Running Locally

### Prerequisites

- Docker Desktop
- Python 3.12+ (for running tests locally)

### Start the application

```bash
cp .env.example .env
# Fill in your values in .env
docker compose up --build
```

App runs at `http://localhost:5000`

### API Endpoints

| Method | Endpoint    | Description    |
| ------ | ----------- | -------------- |
| GET    | /health     | Health check   |
| GET    | /tasks      | List all tasks |
| GET    | /tasks/<id> | Get one task   |
| POST   | /tasks      | Create a task  |
| PUT    | /tasks/<id> | Update a task  |
| DELETE | /tasks/<id> | Delete a task  |

### Run Tests

```bash
python -m pytest tests/test_app.py -v
```

## Project Status

- [x] Phase 1: Flask + MySQL application
- [x] Phase 2: Docker containerization
- [x] Phase 3: Git + GitHub
- [ ] Phase 4: Jenkins setup
- [ ] Phase 5: CI/CD pipeline
- [ ] Phase 6: AWS EC2 deployment
