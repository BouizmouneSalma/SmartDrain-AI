# File_rouge - SmartDrain AI

SmartDrain is a full-stack AI project for cover detection from images (and soon video), with a React frontend and a FastAPI backend powered by a YOLO model.

## Overview

This repository contains:
- A web frontend to authenticate users, upload media, and view detection history.
- A FastAPI backend exposing auth, prediction, and history endpoints.
- ML artifacts and datasets used for model training/inference.
- Docker assets for containerized deployment.

## Tech Stack

- Frontend: React 18, Vite, MUI, Axios, Recharts
- Backend: FastAPI, Uvicorn, Pydantic
- AI/ML: Ultralytics YOLO, OpenCV, NumPy, Torch
- Data/Infra: PostgreSQL-related dependencies (planned), Docker, Grafana provisioning

## Project Structure

```text
.
|- backend/
|  |- app/
|  |  |- main.py
|  |  |- api/routes/
|  |     |- auth.py
|  |     |- predict.py
|  |     |- history.py
|  |- requirements.txt
|  |- Dockerfile
|- frontend/
|  |- src/
|  |- package.json
|  |- .env.example
|  |- Dockerfile
|- dataset/
|- ml/
|- docker/
|  |- docker-compose.yml
|- monitoring/
```

## Main Features

- Authentication (demo/in-memory):
  - Register user
  - Login user (returns a demo token)
- Prediction:
  - Image detection with YOLO model (`/predict/image`)
  - Video endpoint placeholder (`/predict/video`)
- History:
  - Read prediction history
  - Add new history record

## API Endpoints

Base URL (local): `http://localhost:8000`

- `GET /` -> Health message
- `POST /auth/register` -> Register user
- `POST /auth/login` -> Login user
- `POST /predict/image` -> Upload image and return detections
- `POST /predict/video` -> Placeholder response
- `GET /history/` -> Get in-memory history
- `POST /history/` -> Append in-memory history item

## Prerequisites

- Python 3.11+ (recommended)
- Node.js 18+ and npm
- (Optional) Docker + Docker Compose

## Local Development Setup

### 1. Clone and enter the project

```bash
git clone <https://github.com/BouizmouneSalma/SmartDrain-AI.git>
```

### 2. Backend setup (FastAPI)

From repository root:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

Run API:

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 3. Frontend setup (React + Vite)

Open a second terminal from repository root:

```bash
cd frontend
npm install
```

Create environment file:

```bash
cp .env
```

Windows PowerShell alternative:

```powershell
Copy-Item .env
```

Run frontend:

```bash
npm run dev
```

Frontend URL: `http://localhost:3000`

### Backend

No mandatory `.env` is required for current in-memory flow, but `python-dotenv` and `pydantic-settings` are already included for future configuration.

## Docker

A compose file exists at `docker/docker-compose.yml`.

Current status:
- Frontend service is present.
- Backend and database services are scaffolded as comments.

Run with:

```bash
docker compose -f docker/docker-compose.yml up --build
```

Note:
- You may need to adjust compose build contexts depending on your local Docker setup.
- Frontend Dockerfile expects an `nginx.conf` file that is not currently in `frontend/`.

## Testing

- Backend tests folder exists (`backend/tests/`) but no automated tests are currently committed.
- Recommended next step: add pytest coverage for auth, predict, and history routes.

## Known Limitations (Current State)

- Auth and history use in-memory fake data (not persistent).
- `/predict/video` is not implemented yet.
- YOLO weights path in `backend/app/api/routes/predict.py` is an absolute Windows path and should be moved to config/env for portability.
