# AI Task Manager

> **Agentic Code Project**: This project was built using Claude Code's multi-agent workflow system, leveraging specialized agents (backend-dev, frontend-design-architect, code-quality-enforcer, integration-tester) for efficient development.

## Project Overview

AI Task Manager is an intelligent task management application that helps developers stay accountable to their deadlines through AI-powered motivation and content generation. The application combines a FastAPI backend with a Next.js frontend to deliver a seamless task management experience with unique AI-driven features.

**Key Capabilities:**
- Create and manage tasks with specific deadlines
- Receive AI-generated humorous insults when deadlines are missed (developer-themed motivation)
- Generate and modify task summaries using AI or manual editing
- Track productivity with comprehensive analytics and visual graphs
- RESTful API with full OpenAPI documentation

## Features

- **Deadline-Based Task Management**: Create tasks with specific deadlines and track completion
- **AI-Powered Insults**: Get funny, developer-themed motivational insults when you miss deadlines
- **Smart Summaries**: Generate concise AI-powered task summaries with natural language modification
- **Analytics Dashboard**: Track completion rates, deadline adherence, and productivity trends
- **REST API**: Complete FastAPI backend with OpenAPI documentation

## Technology Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI/LLM**: LangChain for external API integration (vLLM compatible)
- **Configuration**: Hydra for hierarchical configuration management
- **Testing**: pytest with comprehensive mocking

### Frontend
- **Framework**: Next.js 14+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: React with modern hooks
- **API Client**: Fetch API for backend communication
- **Charts**: Recharts for analytics visualization

## Project Structure

```
taskmanager/
├── backend/
│   ├── app/
│   │   ├── endpoint/          # API route handlers
│   │   ├── models/            # SQLAlchemy database models
│   │   ├── schemas/           # Pydantic validation schemas
│   │   ├── utils/             # Business logic and utilities
│   │   └── main.py            # FastAPI application entry point
│   ├── config/                # Hydra configuration files
│   │   ├── llm/              # LLM model settings and prompts
│   │   └── db/               # Database configuration
│   └── test/                  # Unit tests
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js App Router pages
│   │   ├── components/       # React components
│   │   ├── lib/              # API client and utilities
│   │   └── types/            # TypeScript type definitions
│   ├── public/               # Static assets
│   └── package.json          # Node.js dependencies
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Getting Started

### Prerequisites

- Python 3.12 or higher
- PostgreSQL 14 or higher
- vLLM server (or OpenAI-compatible API endpoint)
- Node.js 18+ and npm (for frontend)
- uv (Python package installer) - Install via: `pip install uv`

### Installation

#### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd taskmanager
   ```

2. **Install Python dependencies using uv**
   ```bash
   uv pip install -r requirements.txt
   ```

   Or if you prefer creating a virtual environment first:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -r requirements.txt
   ```

3. **Set up PostgreSQL database**
   ```sql
   CREATE DATABASE taskmanager;
   CREATE USER taskmanager_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE taskmanager TO taskmanager_user;
   ```

4. **Configure application settings**

   All configuration is managed through Hydra YAML files in `backend/config/`. Update the following files:

   **Database Configuration** - `backend/config/db/database.yaml`:
   ```yaml
   database:
     host: "localhost"
     port: 5432
     database: "taskmanager"
     user: "taskmanager_user"
     password: "your_password"  # Replace with your actual password
   ```

   **LLM Configuration** - `backend/config/llm/model_config.yaml`:
   ```yaml
   llm:
     model_name: "meta-llama/Llama-2-7b-chat-hf"
     api_base: "http://localhost:8001/v1"  # Your vLLM API endpoint
     api_key: "EMPTY"  # Set if your vLLM server requires authentication
     temperature: 0.7
     max_tokens: 150
   ```

   **Optional**: Customize AI prompt templates:
   - `backend/config/llm/insult_prompts.yaml` - Deadline insult generation
   - `backend/config/llm/summary_prompts.yaml` - Task summary generation

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Configure API endpoint** (Optional)

   Update the API base URL in `frontend/src/lib/api.ts` if your backend runs on a different port:
   ```typescript
   const API_BASE_URL = 'http://localhost:8000/api';
   ```

### Running the Application

You need to run both the backend and frontend servers simultaneously.

#### Start Backend Server

1. **Navigate to project root and start FastAPI server**
   ```bash
   cd backend
   python -m backend.app.main
   ```

   Or using uvicorn directly:
   ```bash
   uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Verify backend is running**
   - Interactive API docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc
   - Health check: http://localhost:8000/health

#### Start Frontend Server

1. **Open a new terminal and navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Start the Next.js development server**
   ```bash
   npm run dev
   ```

3. **Access the application**
   - Frontend application: http://localhost:3000
   - The frontend will automatically connect to the backend API at http://localhost:8000

#### Production Build

**Frontend:**
```bash
cd frontend
npm run build
npm start
```

**Backend:**
```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks` - Get tasks with filters (user_id, completed, overdue_only)
- `GET /api/tasks/{task_id}` - Get a specific task
- `PUT /api/tasks/{task_id}` - Update a task
- `DELETE /api/tasks/{task_id}` - Delete a task

### Summaries
- `POST /api/summaries/generate` - Generate AI summary for a task
- `POST /api/summaries/modify` - Modify summary with natural language prompt
- `POST /api/summaries/regenerate/{task_id}` - Regenerate task summary

### Analytics
- `GET /api/analytics` - Get comprehensive analytics for a user
- `GET /api/analytics/completion-stats` - Get task completion statistics
- `GET /api/analytics/deadline-adherence` - Get deadline adherence metrics
- `GET /api/analytics/productivity-trends` - Get productivity trends over time

### Deadlines
- `GET /api/deadlines/check` - Check for missed deadlines and generate insults
- `POST /api/deadlines/regenerate-insult/{task_id}` - Regenerate insult for a task
- `GET /api/deadlines/overdue` - Get all overdue tasks

## Configuration

All configuration is managed through Hydra YAML files in `backend/config/`. No environment variables or .env files are used.

### Database Configuration

Edit `backend/config/db/database.yaml`:

```yaml
database:
  host: "localhost"
  port: 5432
  database: "taskmanager"
  user: "taskmanager_user"
  password: "your_password"  # Set your actual database password here
```

### LLM Configuration

Edit `backend/config/llm/model_config.yaml`:

```yaml
llm:
  model_name: "meta-llama/Llama-2-7b-chat-hf"
  api_base: "http://localhost:8001/v1"  # Your vLLM API endpoint
  api_key: "EMPTY"  # Set if authentication is required
  temperature: 0.7
  max_tokens: 150
```

### Prompt Templates

Customize AI behavior by editing:
- `backend/config/llm/insult_prompts.yaml` - Deadline insult generation
- `backend/config/llm/summary_prompts.yaml` - Task summary generation and modification

## Testing

### Run all tests
```bash
cd backend
pytest
```

### Run tests with coverage
```bash
pytest --cov=backend.app --cov-report=html
```

### Run specific test file
```bash
pytest test/test_task_routes.py
```

### Run tests with verbose output
```bash
pytest -v
```

## Development

### Code Quality

The project follows Python best practices:
- PEP 8 compliance (enforced by pylint)
- Type hints on all functions
- Comprehensive docstrings
- Parameterized database queries (SQL injection prevention)
- Input validation with Pydantic
- Proper error handling and logging

### Running Linting
```bash
pylint backend/app
```

### Code Formatting
```bash
black backend/app
```

## Database Schema

### Users Table
- `id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `created_at`

### Tasks Table
- `id` (Primary Key)
- `title`
- `description`
- `deadline`
- `completed` (Boolean)
- `created_at`
- `updated_at`
- `user_id` (Foreign Key → users.id)
- `summary` (AI-generated)
- `insult_message` (AI-generated for missed deadlines)

### Analytics Table
- `id` (Primary Key)
- `user_id` (Foreign Key → users.id)
- `task_id` (Reference to task)
- `event_type` (created, completed, missed_deadline)
- `event_timestamp`
- `task_title`
- `deadline`
- `was_completed_on_time`
- `completion_delay_hours`

## AI Features

### Insult Generation
When a deadline is missed, the AI generates funny, developer-themed insults:
- Single-line witty messages
- Context-aware based on task details
- Motivational and lighthearted

Example: "Even Internet Explorer would have finished this task by now."

### Summary Generation
Generate concise task summaries:
- Single-line descriptions
- Action-oriented and clear
- Manual editing or AI-based modification with natural language prompts

### Analytics Tracking
Comprehensive metrics including:
- Task completion rates
- Deadline adherence percentages
- Productivity trends over time
- Historical performance data

## Troubleshooting

### Database Connection Issues
1. Verify PostgreSQL is running: `pg_isready`
2. Check database credentials in `backend/config/db/database.yaml`
3. Verify database exists: `psql -l`
4. Ensure user has proper permissions

### LLM Client Issues
1. Verify vLLM server is running
2. Check API endpoint in `backend/config/llm/model_config.yaml`
3. Test health endpoint: `GET /health`
4. Review logs in `backend.log`

### Import Errors
1. Ensure virtual environment is activated
2. Reinstall dependencies: `uv pip install -r requirements.txt`
3. Verify PYTHONPATH includes project root

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and write tests
4. Run tests and linting
5. Commit changes: `git commit -m "Description"`
6. Push to branch: `git push origin feature-name`
7. Create a Pull Request

## Security

- Never commit secrets or API keys to version control
- Sensitive configuration stored in Hydra YAML files (add to .gitignore if needed)
- All database queries use parameterized statements (SQL injection prevention)
- Input validation on all API endpoints with Pydantic schemas
- Proper error handling without exposing internal details
- CORS protection configured in FastAPI middleware
