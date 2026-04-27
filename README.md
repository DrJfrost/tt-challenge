# Project Manager API

A production-ready, scalable FastAPI backend for managing Projects and Tasks with PostgreSQL. Built as a code challenge for a Senior Python Fullstack Engineer position.

## ✨ Features

- **Complete RESTful API** - Full CRUD operations for Projects and Tasks
- **Async Database Operations** - High-performance async PostgreSQL with asyncpg
- **API Key Authentication** - Simple but effective security via API key header
- **Priority-Based Task Sorting** - Tasks automatically sorted by priority (descending)
- **Pagination Support** - Efficient data retrieval with page/page_size parameters
- **Auto-Generated Documentation** - Interactive Swagger UI and ReDoc
- **Docker Containerization** - One-command deployment with Docker Compose
- **Comprehensive Testing** - 7 automated tests covering all endpoints
- **Type Safety** - Full Python type hints with Pydantic v2 validation
- **Database Migrations** - Alembic-based schema management

## 🚀 Quick Start (Choose One Method)

### Method 1: Docker (Recommended - Easiest)

```bash
# Clone the repository
git clone git@github.com:DrJfrost/tt-challenge.git
cd tt-challenge

# Start both PostgreSQL and the API with one command
docker compose up -d

# Wait 10-15 seconds for the database to initialize
# Then verify it's running:
curl http://localhost:8000/docs
```

**That's it!** The API is now running at http://localhost:8000 with:
- PostgreSQL database automatically created
- Tables automatically created
- API key: `dev-key-123`

### Method 2: Local Development (Manual Setup)

#### Prerequisites
- Python 3.13+ (3.11+ also works)
- `uv` package manager (install from https://docs.astral.sh/uv/getting-started/installation/)
- PostgreSQL 14+ installed and running

#### Step-by-Step Setup

1. **Clone and enter directory**
   ```bash
   git clone git@github.com:DrJfrost/tt-challenge.git
   cd tt-challenge
   ```

2. **Install Python dependencies**
   ```bash
   uv sync --group dev
   ```

3. **Create and configure environment**
   ```bash
   cp .env.example .env
   nano .env  # or use your preferred editor
   ```
   
   Update the `.env` file with your PostgreSQL credentials:
   ```env
   DATABASE_URL=postgresql+asyncpg://your_username:your_password@localhost:5432/project_manager
   API_KEY=your-secret-api-key  # Choose any secure key
   ENVIRONMENT=development
   ```

4. **Create the PostgreSQL database**
   ```bash
   # Connect to PostgreSQL
   psql -U your_username
   
   # Inside psql, create the database:
   CREATE DATABASE project_manager;
   \q
   ```

5. **Run database migrations**
   ```bash
   uv run alembic upgrade head
   ```
   This creates the `projects` and `tasks` tables with proper indexes.

6. **Start the development server**
   ```bash
   uv run uvicorn src.main:app --reload
   ```

7. **Open API documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 📖 API Documentation

Once running, visit:
- **Interactive Swagger UI**: http://localhost:8000/docs
- **Alternative ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON Schema**: http://localhost:8000/openapi.json

## 🔧 Configuration

The application uses environment variables for configuration. Copy `.env.example` to `.env` and adjust:

```env
# PostgreSQL connection string (asyncpg driver for async operations)
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/database_name

# API authentication key (used in X-API-Key header)
API_KEY=your-secret-api-key

# Environment: development or production
ENVIRONMENT=development
```

**Important Notes:**
- In Docker, the API key is set to `dev-key-123` (see `docker-compose.yml`)
- For local development, choose your own secure key
- The DATABASE_URL must use the `asyncpg` driver for async operations

## 📡 API Endpoints

### Projects

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/api/v1/projects/` | Create a new project | Required |
| GET | `/api/v1/projects/{project_id}` | Retrieve project details | Required |
| PUT | `/api/v1/projects/{project_id}` | Update project details | Required |
| DELETE | `/api/v1/projects/{project_id}` | Delete a project | Required |

### Tasks

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/api/v1/projects/{project_id}/tasks/` | Add a new task to a project | Required |
| GET | `/api/v1/projects/{project_id}/tasks/` | List all tasks for a project (sorted by priority DESC) | Required |
| PUT | `/api/v1/tasks/{task_id}` | Update a task | Required |
| DELETE | `/api/v1/tasks/{task_id}` | Delete a task | Required |

## 🔐 Authentication

All endpoints require an API key passed in the `X-API-Key` header:

```bash
curl -X GET http://localhost:8000/api/v1/projects/123 \
  -H "X-API-Key: your-secret-api-key"
```

**Default API Keys:**
- Docker: `dev-key-123`
- Local: Whatever you set in `.env`

## 📝 Example Usage

### Create a Project

```bash
curl -X POST http://localhost:8000/api/v1/projects/ \
  -H "X-API-Key: dev-key-123" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Awesome Project",
    "description": "Building something great"
  }'
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "My Awesome Project",
  "description": "Building something great",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Add a Task to a Project

```bash
curl -X POST http://localhost:8000/api/v1/projects/550e8400-e29b-41d4-a716-446655440000/tasks/ \
  -H "X-API-Key: dev-key-123" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Implement authentication",
    "priority": 10,
    "due_date": "2024-01-20"
  }'
```

### List Tasks (Sorted by Priority)

```bash
curl http://localhost:8000/api/v1/projects/550e8400-e29b-41d4-a716-446655440000/tasks/ \
  -H "X-API-Key: dev-key-123"
```

**Response** (automatically sorted by priority descending):
```json
[
  {
    "title": "Implement authentication",
    "priority": 10,
    "completed": false,
    "due_date": "2024-01-20",
    "id": "660f9511-f3ac-52e5-b827-557766551111",
    "project_id": "550e8400-e29b-41d4-a716-446655440000",
    "created_at": "2024-01-15T10:35:00Z"
  },
  {
    "title": "Write documentation",
    "priority": 5,
    "completed": false,
    "due_date": null,
    "id": "771g0622-g4bd-63f6-c938-668877662222",
    "project_id": "550e8400-e29b-41d4-a716-446655440000",
    "created_at": "2024-01-15T10:36:00Z"
  }
]
```

## 🗄️ Data Models

### Project
- `id` (UUID) - Unique identifier, auto-generated
- `name` (string, required) - Project name (1-255 characters)
- `description` (string, optional) - Project description
- `created_at` (datetime) - Creation timestamp, auto-set

### Task
- `id` (UUID) - Unique identifier, auto-generated
- `project_id` (UUID) - Foreign key reference to parent project
- `title` (string, required) - Task title (1-255 characters)
- `priority` (integer) - Priority level (0-100, higher = more important)
- `completed` (boolean) - Completion status (default: false)
- `due_date` (date, optional) - Task due date
- `created_at` (datetime) - Creation timestamp, auto-set

## 🏗️ Project Structure

```
tt-challenge/
├── alembic/                    # Database migrations
│   ├── env.py                 # Alembic environment configuration
│   └── versions/              # Migration scripts
│       └── 001_initial_migration.py
├── src/
│   ├── api/
│   │   └── v1/
│   │       ├── api.py         # Router setup and inclusion
│   │       └── endpoints/     # API endpoint handlers
│   │           ├── projects.py
│   │           └── tasks.py
│   ├── services/              # Business logic layer
│   │   ├── project_service.py
│   │   └── task_service.py
│   ├── config.py              # Configuration management (Settings class)
│   ├── database.py            # Database connection and session
│   ├── dependencies.py        # Dependency injection (auth)
│   ├── exceptions.py          # Custom exception handlers
│   ├── models.py              # SQLAlchemy ORM models
│   ├── schemas.py             # Pydantic schemas for validation
│   └── main.py                # FastAPI application entry point
├── tests/                     # Test suite
│   ├── conftest.py           # Test fixtures and configuration
│   ├── test_projects.py      # Project endpoint tests
│   └── test_tasks.py         # Task endpoint tests
├── docker-compose.yml         # Docker orchestration
├── Dockerfile                 # Application container definition
├── pyproject.toml             # Project metadata and dependencies
├── alembic.ini                # Alembic configuration
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## 🧪 Running Tests

The project includes a comprehensive test suite using pytest.

### Run All Tests
```bash
uv run pytest
```

### Run with Verbose Output
```bash
uv run pytest -v
```

### Run with Coverage Report
```bash
uv run pytest --cov=src --cov-report=html
# Open htmlcov/index.html in your browser
```

### Run Specific Test File
```bash
uv run pytest tests/test_projects.py -v
uv run pytest tests/test_tasks.py -v
```

**Test Coverage:**
- ✅ Create project
- ✅ Get project (found and not found)
- ✅ Update project
- ✅ Delete project
- ✅ Create task
- ✅ List tasks sorted by priority
- ✅ Update task
- ✅ Delete task

## 🛠️ Development

### Code Quality Tools

The project uses modern Python tooling for code quality:

```bash
# Format code with Black
uv run black src/ tests/

# Lint with Ruff (fast, replaces flake8, isort, etc.)
uv run ruff check src/ tests/

# Type checking with MyPy
uv run mypy src/
```

### Database Migrations

After modifying models in `src/models.py`:

```bash
# Generate a new migration
uv run alembic revision --autogenerate -m "Description of changes"

# Apply all pending migrations
uv run alembic upgrade head

# Rollback one migration
uv run alembic downgrade -1

# View migration history
uv run alembic history

# Show current migration status
uv run alembic current
```

## 🐳 Docker Commands

### Basic Operations
```bash
# Start all services (PostgreSQL + API)
docker compose up -d

# View logs
docker compose logs -f app
docker compose logs -f postgres

# Stop all services
docker compose down

# Remove everything including database volume
docker compose down -v
```

### Inside the Container
```bash
# Run migrations
docker compose exec app uv run alembic upgrade head

# Run tests
docker compose exec app uv run pytest

# Open a Python shell
docker compose exec app python

# View environment variables
docker compose exec app env
```

### Rebuilding
```bash
# Rebuild after code changes (with --build flag)
docker compose up --build -d

# Force rebuild without cache
docker compose build --no-cache
docker compose up -d
```

## 📦 Dependencies

### Core Dependencies
- **fastapi** (0.110.0+) - Modern web framework for building APIs
- **uvicorn** (0.29.0+) - ASGI server for running FastAPI
- **sqlalchemy** (2.0.0+) - SQL toolkit and ORM
- **asyncpg** (0.29.0+) - PostgreSQL adapter for async operations
- **psycopg2-binary** (2.9.0+) - PostgreSQL adapter for Alembic migrations
- **pydantic** (2.6.0+) - Data validation using Python type annotations
- **pydantic-settings** (2.2.0+) - Settings management with Pydantic
- **alembic** (1.13.0+) - Database migration tool
- **httpx** (0.27.0+) - Async HTTP client for testing
- **python-multipart** (0.0.9+) - Form data parsing

### Development Dependencies
- **pytest** (8.0.0+) - Testing framework
- **pytest-asyncio** (0.23.0+) - Async support for pytest
- **pytest-cov** (4.1.0+) - Coverage plugin for pytest
- **aiosqlite** (0.20.0+) - Async SQLite driver for testing
- **black** (24.0.0+) - Code formatter
- **ruff** (0.3.0+) - Fast Python linter
- **mypy** (1.8.0+) - Static type checker

## 🔒 Security

- **API Key Authentication** - All endpoints protected by API key header
- **Input Validation** - Pydantic models validate all incoming data
- **SQL Injection Prevention** - SQLAlchemy ORM with parameterized queries
- **CORS Configuration** - Configurable cross-origin request handling
- **Environment Variables** - Sensitive data stored in environment, not code

## 🐛 Troubleshooting

### Docker Issues

**Container won't start:**
```bash
# Check logs
docker compose logs app

# Restart services
docker compose restart

# Rebuild from scratch
docker compose down -v
docker compose up --build -d
```

**Database connection errors:**
```bash
# Wait for PostgreSQL to be healthy
docker compose logs postgres

# Check if PostgreSQL is ready
docker compose exec postgres pg_isready -U user
```

### Local Development Issues

**Alembic migration errors:**
```bash
# Ensure database exists
psql -U username -c "CREATE DATABASE project_manager;"

# Check DATABASE_URL in .env
cat .env

# Run migrations manually
uv run alembic upgrade head
```

**Import errors:**
```bash
# Ensure dependencies are installed
uv sync --group dev

# Check Python version (should be 3.13+)
python --version

# Reinstall dependencies if needed
rm -rf .venv
uv sync --group dev
```

**Port already in use:**
```bash
# Find what's using port 8000
lsof -i :8000

# Kill the process (replace PID)
kill -9 PID

# Or change port in docker-compose.yml
```

## 📄 License

This project is proprietary and confidential. All rights reserved.

## 🤝 Contributing

This is a code challenge project. For production use, please follow standard contribution guidelines:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `uv run pytest`
5. Submit a pull request

## 📞 Support

For issues or questions:
1. Check the API documentation at http://localhost:8000/docs
2. Review the logs: `docker compose logs -f app`
3. Open an issue on the repository

## 🎯 Challenge Requirements Met

This implementation satisfies all requirements from the code challenge:

✅ **Backend API** - FastAPI with all required endpoints  
✅ **Data Model** - Projects and Tasks with proper relationships  
✅ **Database** - PostgreSQL with efficient schema and indexes  
✅ **Async Operations** - All endpoints and database calls are async  
✅ **Validation** - Pydantic models for input validation  
✅ **Error Handling** - Proper HTTP status codes and error messages  
✅ **Code Quality** - Clean, maintainable, well-structured code  

**Bonus Features Implemented:**
✅ **Authentication** - API key header protection  
✅ **Pagination** - Page/page_size parameters for task lists  

---

**Ready to use!** Choose Docker for instant setup or follow local development steps. All endpoints are tested and working.