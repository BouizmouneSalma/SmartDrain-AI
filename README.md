# SmartDrain AI - Intelligent Cover Detection System

SmartDrain is a full-stack AI-powered application for **automated detection and classification of sewer cover conditions** from images. The system uses a fine-tuned YOLO11 deep learning model to identify cover states (Good, Broken, Lose, Uncovered) in real-time, with a modern web interface and comprehensive monitoring infrastructure.

## 📋 Overview

**SmartDrain AI** combines cutting-edge computer vision with a professional full-stack architecture to provide:

- **AI-Powered Detection**: YOLO-based model for multi-class cover detection with 4 distinct cover states
- **User-Centric Web Interface**: React/Vite frontend for intuitive image upload and result visualization
- **RESTful API**: FastAPI backend with authentication, inference, and prediction history management
- **Data Persistence**: PostgreSQL database for secure user account and prediction history storage
- **Real-time Monitoring**: Prometheus + Grafana dashboards for system health and inference metrics
- **Production-Ready Deployment**: Docker containerization for seamless cloud and on-premise deployment
- **Comprehensive Testing**: pytest-based automated test suite covering auth, prediction, and history routes
- **Experiment Tracking**: MLflow integration for model training and versioning

## 🎯 Key Features

| Feature | Status | Details |
|---------|--------|---------|
| **User Authentication** | ✅ Complete | Secure login/register with token-based auth |
| **Image Prediction** | ✅ Complete | Real-time YOLO inference with 4-class detection |
| **Prediction History** | ✅ Complete | User-isolated database storage of inference results |
| **Image Enhancement** | ✅ Complete | CLAHE preprocessing for improved robustness |
| **Business Logic** | ✅ Complete | IoU-based overlap detection for compound states |
| **Video Prediction** | 🚧 Planned | Frame-by-frame processing with temporal filtering |
| **Model Training** | ✅ Complete | YOLO fine-tuning on custom dataset with MLflow tracking |
| **Monitoring & Alerts** | ✅ Complete | Prometheus metrics + Grafana visualization |
| **Automated Testing** | ✅ Complete | 8+ pytest test cases covering all endpoints |
| **Docker Deployment** | ✅ Complete | Full containerized stack with docker-compose |

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18 • Vite • Material-UI (MUI) • Axios • Recharts |
| **Backend** | FastAPI • Uvicorn • SQLAlchemy • Pydantic |
| **Database** | PostgreSQL (with SQLite fallback for dev) |
| **AI/ML** | Ultralytics YOLO11 • OpenCV • NumPy • Torch |
| **Monitoring** | Prometheus • Grafana • Fastapi-instrumentator |
| **ML Tracking** | MLflow (2.17.2) |
| **Testing** | pytest • pytest-cov |
| **DevOps** | Docker • Docker Compose |
| **Security** | python-jose • passlib • hashlib/hmac

## 📁 Project Architecture

### Directory Structure

```
SmartDrain-AI/
├── backend/                          # FastAPI backend application
│   ├── app/
│   │   ├── main.py                  # FastAPI app initialization
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── auth.py          # User registration & login
│   │   │       ├── predict.py       # YOLO inference endpoint
│   │   │       └── history.py       # Prediction history management
│   │   ├── core/
│   │   │   ├── database.py          # SQLAlchemy setup + DB session
│   │   │   └── auth.py              # Authentication utilities
│   │   ├── models/                  # SQLAlchemy ORM models
│   │   │   ├── user.py              # User account model
│   │   │   └── history.py           # HistoryEntry model
│   │   ├── schemas/                 # Pydantic request/response schemas
│   │   │   ├── user.py
│   │   │   ├── history.py
│   │   │   └── prediction.py
│   │   └── services/                # Business logic layer
│   │       ├── auth_service.py      # Auth operations
│   │       ├── history_service.py   # History operations
│   │       └── inference.py         # YOLO inference wrapper
│   ├── tests/
│   │   ├── conftest.py              # pytest fixtures & DB setup
│   │   ├── test_auth_routes.py      # Auth endpoint tests
│   │   ├── test_history_routes.py   # History endpoint tests
│   │   └── test_predict_route.py    # Prediction endpoint tests
│   ├── requirements.txt              # Python dependencies
│   ├── pytest.ini                   # pytest configuration
│   └── Dockerfile                   # Backend container image
│
├── frontend/                         # React + Vite frontend
│   ├── src/
│   │   ├── App.jsx                  # Main app component
│   │   ├── components/
│   │   │   ├── ErrorBoundary.jsx
│   │   │   └── ...                  # UI components
│   │   ├── pages/                   # Page components
│   │   ├── context/                 # React context for state
│   │   └── utils/                   # Helper functions
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   ├── nginx.conf
│   ├── Dockerfile
│   └── .env.example
│
├── ml/                              # Machine Learning components
│   ├── train_cover_detector.py      # YOLO training script with MLflow
│   ├── models/
│   │   └── yolov8_cover-detector/   # Fine-tuned YOLO weights
│   ├── notebooks/
│   │   └── cover_detection.ipynb    # Exploration & analysis
│   └── yolo11n.pt                   # Base model weights
│
├── dataset/                         # Training dataset
│   ├── data.yaml                    # YOLO dataset configuration
│   ├── train/                       # Training images + labels
│   ├── val/                         # Validation split
│   └── test/                        # Test split
│
├── docker/                          # Docker & Kubernetes configs
│   ├── docker-compose.yml           # Multi-container orchestration
│   └── mlflow/
│       └── Dockerfile               # MLflow server container
│
├── monitoring/                      # Observability configs
│   ├── prometheus.yml               # Prometheus scrape config
│   ├── grafana-datasources.yml      # Grafana data sources
│   ├── grafana-dashboards.yml       # Dashboard provisioning
│   └── grafana-dashboards/
│       └── smartdrain-dashboard.json
│
├── diagrams/                        # Architecture & sequence diagrams
│   ├── class-diagram.mmd            # Mermaid class diagram
│   ├── class-diagram.pdf
│   ├── sequence-predict-image.mmd   # Mermaid sequence diagram
│   └── sequence-predict-image.pdf
│
└── README.md                        # This file
```

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE LAYER                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  React 18 Frontend (Vite)                                │  │
│  │  • User authentication                                   │  │
│  │  • Image upload & drag-drop                              │  │
│  │  • Real-time result visualization                        │  │
│  │  • Prediction history dashboard                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│             ↕ Axios HTTP Client (Rest API)                     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                       API GATEWAY LAYER                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  FastAPI (Uvicorn)                                       │  │
│  │  ├─ /auth/register, /auth/login                         │  │
│  │  ├─ /predict/image → YOLO Inference                      │  │
│  │  └─ /history/ ← User-isolated predictions                │  │
│  └──────────────────────────────────────────────────────────┘  │
│             ↕ SQLAlchemy ORM                                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────┬──────────────────┐
│       BUSINESS LOGIC / PERSISTENCE LAYER     │   ML INFERENCE   │
│  ┌──────────────────────────────────────┐   │  ┌────────────┐  │
│  │  Services                             │   │  │ YOLO11n   │  │
│  │  ├─ AuthService (hash, validation)   │   │  │ Model     │  │
│  │  ├─ HistoryService (CRUD)            │   │  ├─ Detect  │  │
│  │  └─ InferenceService (detection)     │   │  ├─ Enhance │  │
│  │         ↕                             │   │  └─ Decide │  │
│  │  SQLAlchemy Models                   │   │             │  │
│  │  ├─ User (id, email, hash)           │   │             │  │
│  │  └─ HistoryEntry (predictions)       │   │             │  │
│  └──────────────────────────────────────┘   │  └────────────┘  │
└──────────────────────────────────────────────┴──────────────────┘
                              ↓
┌──────────────────────────────────────────────┬──────────────────┐
│        DATA & PERSISTENCE LAYER              │  MONITORING      │
│  ┌──────────────────────────────────────┐   │  ┌────────────┐  │
│  │  PostgreSQL Database                 │   │  │ Prometheus │  │
│  │  • User accounts                      │   │  │ Scraper    │  │
│  │  • Prediction history per user        │   │  └────────────┘  │
│  │  • Model metadata                     │   │         ↓         │
│  │                                       │   │  ┌────────────┐  │
│  │  SQLite (dev fallback)                │   │  │ Grafana    │  │
│  │                                       │   │  │ Dashboards │  │
│  └──────────────────────────────────────┘   │  └────────────┘  │
│                                              │                   │
│  MLflow Backend Store (sqlite)               │  FastAPI         │
│  • Training run metadata                     │  Instrumentator  │
│  • Model artifacts                           │  (Prometheus)    │
│  • Hyperparameters & metrics                 │                   │
└──────────────────────────────────────────────┴──────────────────┘
```

## 🚀 Main API Endpoints

| Method | Endpoint | Authentication | Description |
|--------|----------|----------------|-------------|
| `POST` | `/auth/register` | ❌ | Create new user account |
| `POST` | `/auth/login` | ❌ | Generate auth token |
| `POST` | `/predict/image` | ✅ | Upload image → YOLO inference + history |
| `POST` | `/predict/video` | ✅ | Video inference (coming soon) |
| `GET` | `/history/` | ✅ | Fetch user's prediction history |
| `POST` | `/history/` | ✅ | Add history entry manually |
| `GET` | `/` | ❌ | Health check message |
| `GET` | `/health` | ❌ | Detailed health status |

**Response Example** (`POST /predict/image`):
```json
{
  "detections": [
    {
      "class": 0,
      "class_name": "Lose",
      "confidence": 0.87,
      "bbox": [10, 20, 100, 120]
    }
  ],
  "primary_detection": {
    "class_name": "Lose",
    "confidence": 0.87
  },
  "final_decision": {
    "label": "Broken",
    "confidence": 0.75,
    "reason": "lose_uncovered_overlap"
  },
  "inference": {
    "conf": 0.25,
    "iou": 0.45,
    "imgsz": 1024,
    "enhance": true
  }
}
```

## 💻 Getting Started

### Prerequisites

- **Python 3.11+** (for backend and ML)
- **Node.js 18+** with npm (for frontend)
- **Docker & Docker Compose** (optional, for containerized deployment)
- **GPU recommended** (NVIDIA CUDA) for faster YOLO training (optional)

### Local Development (Native Python/Node)

#### Step 1: Clone the Repository

```bash
git clone https://github.com/BouizmouneSalma/SmartDrain-AI.git
cd SmartDrain-AI
```

#### Step 2: Backend Setup (FastAPI)

From project root:

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Or activate (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

**Run the API:**

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Access API documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- API Health: http://localhost:8000/health

#### Step 3: Frontend Setup (React + Vite)

Open a **new terminal** from project root:

```bash
cd frontend
npm install
npm run dev
```

**Frontend running at:** http://localhost:3000

#### Step 4: Run Backend Tests (Optional)

```bash
cd backend
pytest -v
```

Expected output:
```
tests/test_auth_routes.py::test_register_success PASSED
tests/test_auth_routes.py::test_login_success PASSED
tests/test_history_routes.py::test_add_history_then_list_returns_saved_item PASSED
tests/test_predict_route.py::test_predict_image_invalid_file_returns_empty PASSED
======================== 8 passed in 1.23s ========================
```

### Docker Deployment (Recommended for Demo)

#### Start Full Stack with Docker Compose

```bash
cd docker
docker compose up -d --build
```

This will spawn 5 services:

| Service | URL | Port |
|---------|-----|------|
| Frontend (Nginx) | http://localhost:3002 | 3002 |
| Backend API | http://localhost:8000 | 8000 |
| PostgreSQL | localhost:5432 | 5432 |
| Prometheus | http://localhost:9091 | 9091 |
| Grafana | http://localhost:3001 | 3001 |

#### Access Grafana Dashboards

1. Open http://localhost:3001
2. Login with **admin** / **admin123**
3. View SmartDrain dashboard showing:
   - Request count & latency
   - Inference success rate
   - Model accuracy metrics
   - System uptime

#### View Prometheus Metrics

Open http://localhost:9091 and query:
- `fastapi_requests_total` - Total API requests
- `fastapi_requests_duration_seconds` - Request latency
- `fastapi_exceptions_total` - Error count

#### Stop All Services

```bash
cd docker
docker compose down
```

## 🧪 Testing & Quality Assurance

### Run All Backend Tests

```bash
cd backend
pytest -v --cov=app tests/
```

### Test Coverage

SmartDrain includes **8+ automated tests** covering:

- ✅ User registration & duplicate validation
- ✅ Login with correct/wrong credentials
- ✅ Image prediction with mock YOLO model
- ✅ Prediction history storage & retrieval
- ✅ YOLO detection logic & decision making
- ✅ User-isolated data (privacy)

### Example Test Output

```
test_auth_routes.py::test_register_success PASSED                [ 12%]
test_auth_routes.py::test_register_duplicate_user_returns_400 PASSED [ 25%]
test_auth_routes.py::test_login_success PASSED                  [ 37%]
test_auth_routes.py::test_login_invalid_credentials_returns_401 PASSED [ 50%]
test_history_routes.py::test_add_history_then_list_returns_saved_item PASSED [ 62%]
test_predict_route.py::test_predict_image_invalid_file_returns_empty PASSED [ 75%]
test_predict_route.py::test_predict_image_final_decision_overlap_to_broken PASSED [ 87%]
test_predict_route.py::test_resolve_final_decision_prefers_direct_broken PASSED [100%]

======================== 8 passed in 0.84s ========================
```

## 🔬 Model Training & Experiment Tracking with MLflow

### View Training Experiments

MLflow UI tracks all model training runs:

```bash
# Start MLflow server (via Docker)
cd docker
docker compose up -d mlflow

# Or locally:
mlflow ui --backend-store-uri sqlite:///ml/mlruns.db
```

Access at: http://localhost:5000

### Train the Model

```bash
cd backend
python ../ml/train_cover_detector.py
```

This will:
1. Load base YOLOv8s model
2. Train on the dataset (150 epochs)
3. Log metrics, parameters & artifacts to MLflow
4. Save best weights to `ml/models/yolov8_cover-detector/`

**MLflow tracks:**
- Hyperparameters (learning rate, batch size, etc.)
- Metrics (precision, recall, mAP)
- Model artifacts (weights, plots)
- Training duration & resource usage

## 📊 Architecture Diagrams

### Class Diagram
See [diagrams/class-diagram.pdf](diagrams/class-diagram.pdf) for detailed ORM/schema relationships.

### Sequence Diagram (Image Prediction Flow)
See [diagrams/sequence-predict-image.pdf](diagrams/sequence-predict-image.pdf) for end-to-end prediction flow.

## ⚙️ Configuration

### Backend Environment Variables

Create/edit `backend/.env`:

```env
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/smartdrain
# or SQLite:
DATABASE_URL=sqlite:///./smartdrain.db

# Authentication
AUTH_SALT=your-secret-salt-key

# Model/Inference
MODEL_PATH=/app/ml/models/yolov8_cover-detector/weights/best.pt

# MLflow Tracking
MLFLOW_TRACKING_URI=http://localhost:5000
MLFLOW_EXPERIMENT_NAME=smartdrain-cover-detector
```

### Frontend Configuration

Create `frontend/.env` (copy from `.env.example`):

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_TIMEOUT=30000
```

## 📈 Current Status & Roadmap

### ✅ Implemented

- [x] User authentication (register/login)
- [x] Image upload & YOLO inference
- [x] 4-class cover detection (Good, Broken, Lose, Uncovered)
- [x] Image enhancement (CLAHE preprocessing)
- [x] Business logic (IoU overlap for compound detection)
- [x] User-isolated prediction history
- [x] PostgreSQL persistence
- [x] Prometheus + Grafana monitoring
- [x] Docker containerization
- [x] Automated test suite
- [x] MLflow experiment tracking
- [x] Architecture diagrams (class + sequence)

### 🚧 In Progress / Planned

- [ ] Video inference (frame-by-frame YOLO)
- [ ] Real-time notifications
- [ ] Mobile app (React Native)
- [ ] Advanced filtering & search in history
- [ ] Model performance analytics dashboard
- [ ] A/B testing framework
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] API rate limiting & quota management

## 📝 Documentation Files

- [diagrams/class-diagram.pdf](diagrams/class-diagram.pdf) - System class relationships
- [diagrams/sequence-predict-image.pdf](diagrams/sequence-predict-image.pdf) - Prediction flow
- [backend/pytest.ini](backend/pytest.ini) - Test configuration
- [docker/docker-compose.yml](docker/docker-compose.yml) - Container orchestration

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is [YOUR LICENSE HERE - e.g., MIT, GPL-3.0].

## 👤 Author

**Salma Bouizmoun**  
🎓 Student Project - Final Year Capstone  
📧 bouizmoun.salma@example.com  
🔗 GitHub: [@BouizmouneSalma](https://github.com/BouizmouneSalma)

## ❓ Troubleshooting

### Port Already in Use

If port 8000 (FastAPI) is already in use:
```bash
uvicorn backend.app.main:app --port 8001
```

### Database Connection Error

Ensure PostgreSQL is running:
```bash
# Windows
docker run --name smartdrain-db -e POSTGRES_PASSWORD=smartdrain_pass -d postgres:15

# Or use SQLite in dev mode (no config needed)
```

### YOLO Model Not Found

Download weights:
```bash
cd ml
python -m ultralytics.hub.session  # Or download from Ultralytics Hub
```

### Docker Build Fails

Try clean rebuild:
```bash
docker system prune -a
docker compose up --build
```

## 📞 Support & Contact

For questions or issues:
- 📧 Email: bouizmoun.salma@example.com
- 🐛 GitHub Issues: [SmartDrain-AI/issues](https://github.com/BouizmouneSalma/SmartDrain-AI/issues)
- 💬 Discussions: [SmartDrain-AI/discussions](https://github.com/BouizmouneSalma/SmartDrain-AI/discussions)

---

**Made with ❤️ for intelligent cover detection**
