# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**AI Task Manager** is an intelligent task management application that helps developers stay accountable to their deadlines through AI-powered motivation and content generation.

### Core Features

1. **Deadline-Based Task Management**
   - Users can create tasks with specific deadlines
   - When a deadline is crossed and the task remains incomplete, the AI generates funny, developer-related insult lines to motivate completion
   - Single-line witty messages tailored to the specific task context

2. **AI-Powered Summary Generation**
   - Generate concise single-line task summaries with a dedicated button
   - After generation, a "Modify" button appears with two options:
     - **Manual Edit**: Direct text editing by the user
     - **AI Edit**: Query-based regeneration/modification using natural language prompts

3. **Task Analysis & Tracking**
   - Comprehensive analytics to track user task records
   - Visual representation in graph format (completion rates, deadline adherence, productivity trends)
   - Historical data visualization for performance insights

### Technology Stack

- **Backend**: Python + FastAPI
- **Frontend**: Next.js
- **Database**: PostgreSQL
- **LLM Integration**: vLLM for API connectivity (external API calls via LangChain)
- **Configuration Management**: Hydra
- **Testing**: pytest with comprehensive mocking

**Note**: vLLM will call external APIs - use LangChain for external API integrations and LLM model interactions.

## Common Commands

### Backend Development
```bash
# IMPORTANT: Activate virtual environment first
# Detection: Look for directories with Scripts/activate.bat (Windows) or bin/activate (Unix)
# Common names: .venv, venv, env, but can be any custom name (env3, myenv, etc.)
# Activate: <venv_name>\Scripts\activate (Windows) or source <venv_name>/bin/activate (Unix)

# Run backend server (from project root)
cd backend
python -m backend.app.main

# Or using uvicorn directly
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

# Run all tests
pytest

# Run tests with coverage
pytest --cov=backend.app --cov-report=html

# Run specific test file
pytest test/test_task_routes.py

# Run tests with verbose output
pytest -v

# Run linting
pylint backend/app

# Initialize database (if scripts exist)
python -m backend.scripts.init_db
```

### Frontend Development
```bash
# Navigate to frontend and install dependencies
cd frontend
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linting
npm run lint
```

### Project Structure

```
taskmanager/
├── README.md                           # Root documentation with setup and config instructions
├── requirements.txt                    # Python dependencies (FastAPI, SQLAlchemy, psycopg2, vLLM, Hydra)
├── .gitignore
│
├── backend/
│   ├── app/                            # Application core folder
│   │   ├── __init__.py
│   │   ├── main.py                     # FastAPI application entry point
│   │   │
│   │   ├── endpoint/                   # All API endpoint files
│   │   │   ├── __init__.py
│   │   │   ├── task_routes.py         # Task CRUD operations
│   │   │   ├── summary_routes.py      # AI summary generation endpoints
│   │   │   ├── analytics_routes.py    # Task analytics and tracking endpoints
│   │   │   └── deadline_routes.py     # Deadline monitoring endpoints
│   │   │
│   │   ├── utils/                      # Backend logic and utility functions
│   │   │   ├── __init__.py
│   │   │   ├── task_manager.py        # Core task management logic
│   │   │   ├── ai_insult_generator.py # Deadline insult generation logic
│   │   │   ├── summary_generator.py   # Summary generation utilities
│   │   │   ├── analytics_processor.py # Analytics data processing
│   │   │   ├── database.py            # PostgreSQL database connection and session management
│   │   │   └── llm_client.py          # vLLM API client wrapper
│   │   │
│   │   ├── models/                     # Database models (SQLAlchemy ORM)
│   │   │   ├── __init__.py
│   │   │   ├── task.py                # Task model
│   │   │   ├── user.py                # User model
│   │   │   └── analytics.py           # Analytics model
│   │   │
│   │   └── schemas/                    # Pydantic schemas for validation
│   │       ├── __init__.py
│   │       ├── task_schema.py
│   │       ├── summary_schema.py
│   │       └── analytics_schema.py
│   │
│   ├── config/                         # Hydra configuration files
│   │   ├── __init__.py
│   │   ├── config.yaml                # Main configuration file
│   │   │
│   │   ├── llm/                        # LLM model configuration and prompts
│   │   │   ├── model_config.yaml      # vLLM model settings
│   │   │   ├── insult_prompts.yaml    # Deadline insult prompt templates
│   │   │   └── summary_prompts.yaml   # Summary generation prompts
│   │   │
│   │   └── db/                         # Database connection configuration
│   │       └── database.yaml          # DB connection strings and settings
│   │
│   └── test/                           # Unit tests using pytest
│       ├── __init__.py
│       ├── conftest.py                # Pytest fixtures
│       ├── test_task_routes.py
│       ├── test_summary_generator.py
│       ├── test_analytics.py
│       └── test_llm_client.py
│
├── frontend/                           # Next.js application
│   ├── package.json
│   ├── next.config.js
│   ├── tsconfig.json
│   │
│   ├── src/
│   │   ├── app/                        # Next.js App Router
│   │   │   ├── layout.tsx             # Root layout
│   │   │   ├── page.tsx               # Home/dashboard page
│   │   │   ├── tasks/                 # Task management pages
│   │   │   └── analytics/             # Analytics dashboard pages
│   │   │
│   │   ├── components/                 # React components
│   │   │   ├── TaskCard.tsx
│   │   │   ├── TaskForm.tsx
│   │   │   ├── SummaryGenerator.tsx
│   │   │   ├── DeadlineAlert.tsx
│   │   │   └── AnalyticsChart.tsx
│   │   │
│   │   ├── lib/                        # Utilities and helpers
│   │   │   ├── api.ts                 # API client functions
│   │   │   └── utils.ts
│   │   │
│   │   └── types/                      # TypeScript type definitions
│   │       └── task.ts
│   │
│   └── public/                         # Static assets
│
└── test_data/
    └── testing.md                      # Integration test logs
```

**Important**: Refer to the root `README.md` for:
- Getting started guide
- How to run the application
- Where to modify configurations (Hydra configs, LLM prompts, database settings)

This project is configured with a specialized multi-agent workflow system for efficient development. The project uses custom Claude Code agents to handle different aspects of the development lifecycle.

## Architecture Patterns

### Backend Architecture

**Configuration Management with Hydra**:
- All configuration is in YAML files under `backend/config/`
- Main config at `backend/config/config.yaml` uses Hydra's defaults system
- Config is loaded at startup using `hydra.compose()` and `hydra.initialize()`
- Access config via dependency injection through `backend.app.dependencies.load_config()`

**Database Architecture**:
- SQLAlchemy ORM with session management in `backend/app/utils/database.py`
- Models in `backend/app/models/` define database schema
- Database initialization happens in FastAPI lifespan context manager
- Session management uses dependency injection pattern via `get_db()` dependency

**API Routing Pattern**:
- All routes organized by domain in `backend/app/endpoint/`
- Each route file has its own APIRouter with consistent prefix pattern
- Routers included in main app via `app.include_router()`
- Standard endpoint structure:
  - Task operations: `/api/tasks`
  - Summary operations: `/api/summaries`
  - Analytics: `/api/analytics`
  - Deadlines: `/api/deadlines`

**LLM Client Architecture**:
- Centralized LLM client in `backend/app/utils/llm_client.py`
- Uses LangChain for LLM API calls (OpenAI-compatible via vLLM)
- Client initialized at app startup and accessed via dependency injection
- Prompt templates stored in Hydra config files (`backend/config/llm/`)

**Dependency Injection Pattern**:
- Global dependencies in `backend/app/dependencies.py`
- LLM client singleton pattern with `get_llm_client()` function
- Database sessions via `get_db()` generator function
- Config loaded once at startup and cached

### Frontend Architecture

**Next.js App Router Structure**:
- Uses Next.js 14+ App Router (not Pages Router)
- Server-side and client-side components mixed
- Pages in `src/app/` directory with route-based file structure
- Layout component at `src/app/layout.tsx` wraps all pages

**API Client Pattern**:
- Centralized API functions in `src/lib/api.ts`
- Uses fetch API with consistent error handling
- Base URL configured for backend communication
- Type-safe responses using TypeScript types from `src/types/`

**Component Organization**:
- Reusable components in `src/components/`
- Each component handles its own state and side effects
- Props interfaces defined inline or in types file
- Follows React hooks pattern (no class components)

**State Management**:
- Uses React built-in state (useState, useEffect)
- No external state management library (Redux, Zustand)
- API calls trigger re-renders via state updates

### Database Schema Overview

The application uses three main tables with the following relationships:

**Users Table** (`backend/app/models/user.py`):
- Primary key: `id`
- Fields: `username`, `email`, `created_at`
- Relationships: One-to-many with tasks and analytics

**Tasks Table** (`backend/app/models/task.py`):
- Primary key: `id`
- Foreign key: `user_id` → users.id
- Core fields: `title`, `description`, `deadline`, `completed`
- AI-generated fields: `summary`, `insult_message`
- Timestamps: `created_at`, `updated_at`

**Analytics Table** (`backend/app/models/analytics.py`):
- Primary key: `id`
- Foreign key: `user_id` → users.id
- Event tracking: `event_type`, `event_timestamp`, `task_title`, `deadline`
- Performance metrics: `was_completed_on_time`, `completion_delay_hours`

### Key Technical Decisions

**Why Hydra instead of .env files**:
- Provides hierarchical configuration with composition
- Supports environment-specific configs without code changes
- Type-safe config access with OmegaConf
- Easier to manage complex LLM prompt templates in YAML

**Why LangChain for LLM integration**:
- Abstracts different LLM providers (OpenAI, vLLM, etc.)
- Built-in retry logic and error handling
- Template management for prompts
- Easy to swap LLM providers without code changes

**FastAPI Lifespan Pattern**:
- Database connections initialized once at startup
- LLM client health check performed during startup
- Graceful cleanup on shutdown
- Prevents connection leaks and ensures proper resource management

## Important Guidelines

**Virtual Environment Management**:
- Always detect and activate virtual environment before running Python code
- Virtual environments can have any name (not just .venv, venv, env)
- Detect by checking for `Scripts/activate.bat` (Windows) or `bin/activate` (Unix)
- Or check for `pyvenv.cfg` file in directories
- Use `python -m <module>` to ensure using venv Python

**Changelog and Task Tracking (CRITICAL)**:
- **ALWAYS update `.claude-workspace/CHANGELOG.md`** after making ANY code changes
- Format: `## [YYYY-MM-DD HH:MM:SS] - [Agent Name]` with task, changes, files, status, testing results
- When asked about completed/pending tasks, check CHANGELOG.md FIRST - do NOT scan code
- When asked about test results, check `.claude-workspace/TESTING.md` FIRST
- Create `.claude-workspace/` directory if it doesn't exist

**Do NOT create extra or unwanted markdown files**:
- Do not create documentation markdown files unless explicitly requested by the user
- Do not create summary or changelog markdown files after completing tasks
- Do not create notes or planning markdown files
- Focus on code implementation and updating existing documentation only
- The only markdown files that should exist are: README.md, CLAUDE.md, and agent files in .claude/agents/

**Do NOT create .env or .env.example files**:
- This project does NOT use .env files
- All configuration is managed through Hydra YAML files in backend/config/
- Environment-specific settings go in config YAML files, not .env files
- Never create .env, .env.example, .env.local, or similar files

## Development Workflow

This repository uses a **multi-agent development workflow** with specialized agents for different responsibilities. The workflow follows this pattern:

1. **Backend Development** → backend-dev agent implements server-side logic
2. **Frontend Development** → frontend-design-architect agent designs and creates user interfaces
3. **Code Quality** → code-quality-enforcer agent writes unit tests and runs linting
4. **Integration Testing** → integration-tester agent performs comprehensive testing and logs results
5. **Security Audit** → security-auditor agent scans for vulnerabilities and auto-remediates if score < 90%

### Agent Coordination Pattern

When implementing features, follow this sequence:

1. **Implementation Phase**: Use backend-dev or frontend-design-architect agents based on the task
2. **Quality Assurance**: After code is written, **automatically** invoke code-quality-enforcer agent
3. **Integration Testing**: After backend/frontend work is complete, **automatically** invoke integration-tester agent
4. **Security Audit**: After testing is complete, **automatically** invoke security-auditor agent
5. **Auto-Remediation Loop**: If security score < 90%, agents fix issues and re-audit until >= 90%
6. **Resolution Loop**: If tests fail, communicate back to the appropriate dev agent for fixes

## Specialized Agents

### backend-dev (Python-focused)
Use for: API endpoints, database schemas, authentication, AI/ML pipelines, async processing, backend optimization

Key practices:
- Type-annotated Python with modern syntax
- Comprehensive error handling and logging
- Design patterns: dependency injection, repository pattern
- SQLAlchemy ORM for PostgreSQL database interactions
- Database migrations using Alembic
- Proper database indexing and query optimization
- Hydra YAML files for configuration (no .env files)
- Security: parameterized queries, input validation, proper auth

### frontend-design-architect
Use for: Landing pages, dashboards, responsive interfaces, conversion-focused designs

Key practices:
- Mobile-first responsive design
- Semantic HTML and accessibility (WCAG)
- Performance optimization (lazy loading, code splitting)
- Modern CSS (Tailwind, CSS Modules, styled-components)
- 4.5:1 contrast ratio minimum
- Keyboard navigation and screen reader support

### code-quality-enforcer
Automatically invoked after development. Executes:
1. Framework detection (pytest default)
2. Unit test creation (85%+ coverage target)
3. Pylint linting on all modified code
4. Test execution with coverage reporting
5. Automated issue resolution
6. Re-verification until all tests pass and linting is clean

### integration-tester
Automatically invoked after features are complete. Performs:
1. Comprehensive test case generation
2. Integration and regression testing
3. Detailed logging to `test_data/testing.md`
4. Bug reporting with root cause analysis
5. Communication with dev agents for fixes

## Testing and Quality Standards

### Claude Workspace Location
All Claude-related logs and files: `.claude-workspace/`
- **CHANGELOG.md**: All code changes made by agents with timestamps (YYYY-MM-DD HH:MM:SS)
- **test_log/**: Directory containing timestamped test execution logs
  - Format: `testing_YYYYMMDD_HHMMSS.md` (e.g., `testing_20260102_143055.md`)
  - Each test run creates a NEW file with collapsible sections using `<details>` tags
  - Never appends to existing files
- **SECURITY_AUDIT.md**: All security audit results with scores and remediation tracking
- **IMPORTANT**: When asked "what's completed" or "what's pending", check CHANGELOG.md - do NOT scan code

### Testing Strategy
- **Unit tests**: Written by code-quality-enforcer for all new code
- **Integration tests**: Generated by integration-tester for feature workflows
- **Coverage target**: Minimum 80% for new code
- **Test isolation**: All tests must run independently
- **Mocking requirement**: All pytest tests MUST mock external dependencies:
  - Mock all database calls (PostgreSQL connections, queries)
  - Mock all vLLM API requests
  - Mock all external services and third-party libraries
  - Use pytest fixtures and unittest.mock or pytest-mock
  - Never connect to real database or external services during unit tests

### Code Quality Requirements
- PEP 8 compliance (enforced by pylint)
- Type hints on function signatures
- Docstrings for public APIs
- No critical linting errors
- All tests passing before completion

### Testing Patterns in This Codebase

**Pytest Fixtures** (`backend/test/conftest.py`):
- Shared fixtures for database sessions, test clients, mock LLM clients
- Use fixtures to set up test data and tear down after tests
- Fixtures follow pytest's scope model (function, module, session)

**Mocking LLM Calls**:
- Always mock LangChain LLM calls in unit tests
- Use `unittest.mock.patch` or `pytest-mock` for mocking
- Mock at the `llm_client.py` level, not individual LangChain classes
- Example pattern:
  ```python
  @patch('backend.app.utils.llm_client.LLMClient.generate_insult')
  def test_deadline_check(mock_generate):
      mock_generate.return_value = "Test insult"
      # test logic here
  ```

**Database Testing Pattern**:
- Use SQLAlchemy session fixtures that rollback after each test
- Create test data using model instances, not raw SQL
- Test database operations in isolation from API layer
- Never use production database for tests

**API Route Testing**:
- Use FastAPI TestClient from `fastapi.testclient`
- Mock all dependencies (database, LLM client) via dependency overrides
- Test HTTP status codes, response schemas, and error cases
- Example:
  ```python
  from fastapi.testclient import TestClient
  client = TestClient(app)
  response = client.get("/api/tasks")
  assert response.status_code == 200
  ```

## Security Best Practices

**Critical requirements across all agents:**
- Never hardcode secrets, API keys, or credentials
- Use Hydra YAML configuration files for sensitive configuration (not .env files)
- Parameterized queries to prevent SQL injection
- Input validation at all API boundaries
- Proper authentication and authorization checks
- CORS and CSRF protection for web APIs
- Security-focused code reviews

## Communication Protocol

When agents need to interact:
- Use the Task tool to invoke specialized agents
- Provide clear context about what was completed
- Include file paths and specific changes made
- For bugs: include reproduction steps, expected vs actual behavior
- For clarifications: ask specific questions with options

## Automation Philosophy

This repository is configured for **proactive quality automation**:
- Quality checking happens automatically, not on request
- Testing is part of the development process, not separate
- Agents collaborate without manual coordination
- Issues are fixed in automated cycles until resolution
