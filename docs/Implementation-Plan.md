# Paper Summary Agent - Implementation Plan

## Phase 0: Initial Setup with UV

- [ ] 1. Install UV package manager by running `curl -LsSf https://astral.sh/uv/install.sh | sh` (Tech Stack: Package Management).
- [ ] 2. Add UV to PATH by running `source $HOME/.cargo/env` or adding to shell profile (Tech Stack: Environment).
- [ ] 3. Verify UV installation with `uv --version` (Tech Stack: Verification).
- [ ] 4. Create project directory `paper-agent` at `/Users/echo/codeProjects/paper-summarizer/paper-agent` (Project Structure: Root).
- [ ] 5. Navigate to project directory with `cd paper-agent` (Project Structure: Navigation).
- [ ] 6. Create Python 3.11 virtual environment using UV with `uv venv --python 3.11` (Environment: Python).
- [ ] 7. Activate the UV virtual environment with `source .venv/bin/activate` (Environment: Activation).
- [ ] 8. Create initial project structure directories:
    ```bash
    mkdir -p backend/app/{api/v1/endpoints,core,models,schemas,services,tasks,utils}
    mkdir -p frontend/src/{components,pages,hooks,services,contexts,utils,types}
    mkdir -p docs scripts data/samples legacy/outputs
    ```
- [ ] 9. Move existing paper-summarizer files to legacy directory:
    ```bash
    mkdir -p legacy/outputs
    cp ../agent_crewai.py legacy/
    cp ../test.py legacy/
    cp ../*.md legacy/outputs/
    cp ../requirements.txt legacy/
    ```
- [ ] 10. Generate this Implementation Plan document at `docs/Implementation-Plan.md` (Documentation: Planning).
- [ ] 11. Create initial README.md with project overview (Documentation: README).
- [ ] 12. Initialize Git repository with `git init` and create `.gitignore` file (Version Control: Setup).

## Phase 1: Environment Setup

- [ ] 1. Verify Python 3.11 is active in UV environment by running `python --version` (Tech Stack: Verification).
- [ ] 2. Create `pyproject.toml` for UV dependency management with project metadata (Project: Configuration).
- [ ] 3. Install core backend dependencies using UV:
    ```bash
    uv pip install fastapi uvicorn[standard] sqlalchemy psycopg2-binary redis celery python-jose[cryptography] passlib[bcrypt] python-multipart email-validator alembic
    ```
    (Tech Stack: Backend Dependencies).
- [ ] 4. Install AI and data processing dependencies:
    ```bash
    uv pip install openai httpx beautifulsoup4 python-dotenv backoff imaplib-utf7 pydantic-settings crewai
    ```
    (Tech Stack: AI Integration).
- [ ] 5. Install development dependencies:
    ```bash
    uv pip install pytest pytest-asyncio pytest-cov black ruff mypy
    ```
    (Tech Stack: Development Tools).
- [ ] 6. Generate requirements files with `uv pip freeze > backend/requirements.txt` (Dependencies: Export).
- [ ] 7. Install Docker Desktop for macOS from official website (Tech Stack: Containerization).
- [ ] 8. Verify Docker installation with `docker --version` and `docker-compose --version` (Tech Stack: Verification).
- [ ] 9. Create development branch with `git checkout -b development` (Version Control: Branching).
- [ ] 10. Create comprehensive `.gitignore` with Python, Node.js, Docker, and IDE patterns (Version Control: Ignore).
- [ ] 11. Commit initial project structure with `git add . && git commit -m "Initial project setup with UV"` (Version Control: Commit).

## Phase 2: Backend Development

### 2.1 Project Structure Setup

- [ ] 1. **Establish Backend Project Structure**:
    * Inside `backend/`, verify the application directory structure:
      * `app/api/`: For API endpoints/routers
        * `v1/`: API version 1
          * `endpoints/`: Individual route modules
            * `__init__.py`: Package initialization
            * `auth.py`: Authentication endpoints (register, login, logout, refresh)
            * `users.py`: User management endpoints (profile, settings, statistics)
            * `keywords.py`: Keyword and category management
            * `papers.py`: Paper CRUD and search operations
            * `email_configs.py`: Email configuration management
            * `tasks.py`: Background task monitoring
      * `app/core/`: Core functionalities
        * `__init__.py`: Package initialization
        * `config.py`: Application settings with Pydantic Settings
        * `security.py`: JWT tokens and password hashing
        * `database.py`: SQLAlchemy session management
        * `logging.py`: Structured logging setup
        * `celery_app.py`: Celery configuration
      * `app/models/`: SQLAlchemy ORM models
        * `__init__.py`: Model exports
        * `base.py`: Base model class
        * `user.py`: User account model
        * `keyword.py`: Keywords and categories
        * `paper.py`: Papers and annotations
        * `email_config.py`: Email configurations
        * `task.py`: Background task tracking
      * `app/schemas/`: Pydantic validation schemas
        * Request/response models for each endpoint
        * Shared schema components
      * `app/services/`: Business logic layer
        * `auth_service.py`: Authentication logic
        * `email_service.py`: IMAP email operations
        * `paper_service.py`: Paper processing
        * `ai_service.py`: OpenRouter/Gemini integration
        * `firecrawl_service.py`: Web content extraction
        * `task_service.py`: Task management
        * `search_service.py`: Full-text search
      * `app/tasks/`: Celery background tasks
        * `__init__.py`: Task exports
        * `paper_tasks.py`: Paper fetching and processing
        * `email_tasks.py`: Scheduled email checks
        * `summary_tasks.py`: Daily summary generation
      * `app/utils/`: Helper utilities
        * `deps.py`: FastAPI dependencies
        * `validators.py`: Custom validators
        * `exceptions.py`: Custom exceptions
      * `app/main.py`: FastAPI application entry point
    * Additional backend files:
      * `backend/alembic.ini`: Alembic configuration
      * `backend/.env.example`: Environment variables template
      * `backend/Dockerfile`: Container definition
      * `backend/docker-compose.yml`: Local development services

### 2.2 Database Setup

- [ ] 2. Configure PostgreSQL connection in `backend/app/core/database.py`:
    ```python
    - Async SQLAlchemy engine setup
    - Session factory configuration
    - Database URL from environment
    - Connection pool settings
    ```
    (Database: Connection).

- [ ] 3. Initialize Alembic migrations:
    ```bash
    cd backend && alembic init alembic
    ```
    (Database: Migrations).

- [ ] 4. Configure Alembic for async SQLAlchemy in `backend/alembic/env.py` (Database: Async Config).

- [ ] 5. Create base model class in `backend/app/models/base.py`:
    - UUID primary keys
    - Created/updated timestamps
    - Soft delete support
    (Database: Base Model).

- [ ] 6. Implement User model in `backend/app/models/user.py`:
    ```python
    - id: UUID primary key
    - email: Unique, indexed
    - username: Unique, indexed
    - password_hash: Bcrypt hash
    - is_active: Boolean
    - is_verified: Boolean
    - created_at, updated_at: Timestamps
    - last_login: Nullable timestamp
    ```
    (Database: User Model).

- [ ] 7. Create Category model with hierarchy support:
    ```python
    - id: UUID
    - user_id: Foreign key
    - parent_id: Self-referential foreign key
    - name: String(100)
    - description: Text
    - color: String(7) for hex colors
    - icon: String(50)
    - sort_order: Integer
    ```
    (Database: Category Model).

- [ ] 8. Implement Paper model with full-text search:
    ```python
    - id: UUID
    - title: Text, indexed
    - title_cn: Text
    - authors: Array of strings
    - abstract: Text
    - summary_cn: Text
    - keywords: Array
    - research_question: Text
    - methods: Text
    - innovations: Text
    - conclusions: Text
    - source_url: Unique
    - publication_date: Date
    - crawl_date: Timestamp
    - processing_model: String
    - search_vector: TSVector for PostgreSQL FTS
    ```
    (Database: Paper Model).

- [ ] 9. Create relationship models:
    - UserPaper: Many-to-many with annotations
    - UserKeyword: User's keywords with categories
    - EmailConfig: Encrypted email credentials
    (Database: Relationships).

- [ ] 10. Generate and apply initial migration:
    ```bash
    alembic revision --autogenerate -m "Initial models"
    alembic upgrade head
    ```
    (Database: Migration).

- [ ] 11. Create database indexes for performance:
    - Email and username unique indexes
    - Paper title and URL indexes
    - Full-text search GIN index
    - Foreign key indexes
    (Database: Indexes).

- [ ] 12. Implement database health check endpoint (Database: Health).

### 2.3 Core Services Implementation

- [ ] 13. Create application configuration in `backend/app/core/config.py`:
    ```python
    - Database settings
    - Redis settings
    - JWT secret and expiration
    - OpenRouter API configuration
    - Email settings
    - Celery configuration
    - CORS origins
    - Environment detection
    ```
    (Core: Configuration).

- [ ] 14. Implement JWT authentication in `backend/app/core/security.py`:
    - Token generation with claims
    - Token validation and decoding
    - Refresh token logic
    - Password hashing with bcrypt
    - Password strength validation
    (Core: Security).

- [ ] 15. Set up structured logging in `backend/app/core/logging.py`:
    - JSON format for production
    - Correlation ID injection
    - Request/response logging
    - Performance metrics
    - Error tracking
    (Core: Logging).

- [ ] 16. Create dependency injection utilities in `backend/app/utils/deps.py`:
    - Database session dependency
    - Current user dependency
    - Admin user dependency
    - Rate limiting dependency
    (Core: Dependencies).

- [ ] 17. Implement custom exceptions in `backend/app/utils/exceptions.py`:
    - Authentication exceptions
    - Validation exceptions
    - Business logic exceptions
    - External service exceptions
    (Core: Exceptions).

- [ ] 18. Create Celery app configuration in `backend/app/core/celery_app.py`:
    - Redis broker setup
    - Task routing
    - Retry policies
    - Task priorities
    - Result backend
    (Core: Task Queue).

### 2.4 Authentication System

- [ ] 19. Implement user registration in `backend/app/api/v1/endpoints/auth.py`:
    - Email uniqueness validation
    - Password strength requirements
    - Account activation email
    - Rate limiting
    (Auth: Registration).

- [ ] 20. Create login endpoint with:
    - Email/password validation
    - JWT access token generation
    - Refresh token generation
    - Failed attempt tracking
    - Device fingerprinting
    (Auth: Login).

- [ ] 21. Implement token refresh endpoint:
    - Validate refresh token
    - Generate new access token
    - Rotate refresh tokens
    - Blacklist old tokens
    (Auth: Token Refresh).

- [ ] 22. Create password reset flow:
    - Request endpoint with email
    - Token generation and email
    - Reset confirmation endpoint
    - Token expiration (1 hour)
    (Auth: Password Reset).

- [ ] 23. Implement email verification:
    - Verification token generation
    - Email sending with link
    - Verification endpoint
    - Resend functionality
    (Auth: Email Verification).

- [ ] 24. Create OAuth2 password flow compliance (Auth: Standards).

- [ ] 25. Implement session management:
    - Active session tracking
    - Device management
    - Force logout functionality
    (Auth: Sessions).

- [ ] 26. Add two-factor authentication preparation:
    - TOTP secret generation
    - QR code generation
    - Backup codes
    (Auth: 2FA Prep).

### 2.5 AI Integration

- [ ] 27. Create OpenRouter client in `backend/app/services/ai_service.py`:
    ```python
    - HTTP client with retry logic
    - Request/response logging
    - Error handling
    - Timeout configuration
    - Rate limit handling
    ```
    (AI: Client Setup).

- [ ] 28. Configure Gemini Flash 2.0:
    - Model selection logic
    - Temperature settings
    - Token limits
    - Response streaming
    - Cost tracking
    (AI: Model Config).

- [ ] 29. Implement paper summarization:
    - Prompt engineering for academic content
    - Structured output parsing
    - Language detection
    - Fallback strategies
    - Quality validation
    (AI: Summarization).

- [ ] 30. Create prompt templates:
    ```python
    - Title translation prompt
    - Abstract summarization
    - Key findings extraction
    - Method explanation
    - Innovation highlighting
    ```
    (AI: Prompts).

- [ ] 31. Implement token usage tracking:
    - Per-request tracking
    - User quota management
    - Cost calculation
    - Usage analytics
    - Billing preparation
    (AI: Usage Tracking).

- [ ] 32. Add caching layer:
    - Redis cache for responses
    - Cache key generation
    - TTL configuration
    - Cache invalidation
    - Hit rate monitoring
    (AI: Caching).

### 2.6 Email and Paper Processing

- [ ] 33. Create IMAP client in `backend/app/services/email_service.py`:
    - Multi-provider support (Gmail, QQ, Outlook)
    - OAuth2 and password auth
    - Folder navigation
    - Message filtering
    - Attachment handling
    (Email: IMAP Client).

- [ ] 34. Implement email parser:
    - Google Scholar alert detection
    - Paper link extraction
    - Metadata parsing
    - De-duplication logic
    - Error recovery
    (Email: Parser).

- [ ] 35. Create Firecrawl integration:
    - API client setup
    - Job submission
    - Status polling
    - Result parsing
    - Fallback to direct scraping
    (Scraping: Firecrawl).

- [ ] 36. Implement content extraction:
    - PDF text extraction
    - HTML cleaning
    - Markdown conversion
    - Image handling
    - Reference parsing
    (Scraping: Content).

- [ ] 37. Create paper processing pipeline:
    - Queue management
    - Parallel processing
    - Progress tracking
    - Error handling
    - Retry logic
    (Processing: Pipeline).

- [ ] 38. Implement CrewAI agents adaptation:
    - Agent initialization
    - Task definition
    - Workflow orchestration
    - Result aggregation
    - Quality control
    (Processing: Agents).

- [ ] 39. Add paper categorization:
    - Keyword matching
    - ML-based classification
    - User preference learning
    - Confidence scoring
    - Manual override
    (Processing: Categorization).

- [ ] 40. Create deduplication service:
    - URL normalization
    - Title similarity
    - Content hashing
    - Author matching
    - Date proximity
    (Processing: Deduplication).

### 2.7 API Endpoints

- [ ] 41. Implement keyword endpoints in `backend/app/api/v1/endpoints/keywords.py`:
    ```python
    GET    /keywords - List user keywords
    POST   /keywords - Create keyword
    PUT    /keywords/{id} - Update keyword
    DELETE /keywords/{id} - Delete keyword
    POST   /keywords/import - Bulk import
    GET    /keywords/export - Export to CSV/JSON
    GET    /keywords/suggestions - AI suggestions
    ```
    (API: Keywords).

- [ ] 42. Create category endpoints:
    ```python
    GET    /categories - List with hierarchy
    POST   /categories - Create category
    PUT    /categories/{id} - Update
    DELETE /categories/{id} - Delete with cascade
    POST   /categories/{id}/move - Change parent
    ```
    (API: Categories).

- [ ] 43. Implement paper endpoints in `backend/app/api/v1/endpoints/papers.py`:
    ```python
    GET    /papers - Paginated list with filters
    GET    /papers/{id} - Full details
    POST   /papers/{id}/star - Toggle star
    PUT    /papers/{id}/notes - Update notes
    PUT    /papers/{id}/category - Assign category
    POST   /papers/{id}/tags - Add tags
    DELETE /papers/{id} - Soft delete
    POST   /papers/{id}/regenerate - Re-summarize
    ```
    (API: Papers).

- [ ] 44. Create search endpoints:
    ```python
    GET    /papers/search - Full-text search
    GET    /papers/advanced - Complex queries
    GET    /papers/similar/{id} - Find similar
    POST   /papers/search/save - Save search
    ```
    (API: Search).

- [ ] 45. Implement recommendation endpoints:
    ```python
    GET    /papers/recommendations - Personal recommendations
    GET    /papers/trending - Trending papers
    GET    /papers/unread - Unread queue
    ```
    (API: Recommendations).

- [ ] 46. Create email config endpoints:
    ```python
    GET    /email-configs - List configs
    POST   /email-configs - Add email
    PUT    /email-configs/{id} - Update
    DELETE /email-configs/{id} - Remove
    POST   /email-configs/{id}/test - Test connection
    POST   /email-configs/{id}/sync - Manual sync
    ```
    (API: Email Config).

- [ ] 47. Implement task endpoints:
    ```python
    GET    /tasks - List recent tasks
    GET    /tasks/{id} - Task details
    POST   /tasks/paper-fetch - Trigger fetch
    DELETE /tasks/{id} - Cancel task
    GET    /tasks/schedule - View schedules
    ```
    (API: Tasks).

- [ ] 48. Create user endpoints in `backend/app/api/v1/endpoints/users.py`:
    ```python
    GET    /users/me - Current user
    PUT    /users/me - Update profile
    PUT    /users/me/password - Change password
    GET    /users/me/stats - Usage statistics
    DELETE /users/me - Delete account
    GET    /users/me/export - Export data
    ```
    (API: Users).

- [ ] 49. Add admin endpoints:
    ```python
    GET    /admin/users - List all users
    GET    /admin/stats - System statistics
    POST   /admin/broadcast - Send announcement
    ```
    (API: Admin).

- [ ] 50. Implement webhook endpoints:
    ```python
    GET    /webhooks - List webhooks
    POST   /webhooks - Create webhook
    PUT    /webhooks/{id} - Update
    DELETE /webhooks/{id} - Delete
    POST   /webhooks/{id}/test - Test webhook
    ```
    (API: Webhooks).

### 2.8 Background Tasks

- [ ] 51. Configure Celery in `backend/app/core/celery_app.py`:
    - Redis broker connection
    - Task serialization (JSON)
    - Result backend setup
    - Task routing rules
    - Worker configuration
    (Tasks: Setup).

- [ ] 52. Create email checking task:
    ```python
    @celery.task
    def check_user_emails(user_id: str):
        - Fetch email configs
        - Connect to each IMAP
        - Parse new emails
        - Queue paper processing
        - Update last check time
    ```
    (Tasks: Email Check).

- [ ] 53. Implement paper processing task:
    ```python
    @celery.task(bind=True)
    def process_paper(self, paper_url: str, user_id: str):
        - Update task progress
        - Fetch content via Firecrawl
        - Clean and extract text
        - Generate summary via AI
        - Store in database
        - Notify user
    ```
    (Tasks: Paper Process).

- [ ] 54. Create daily summary task:
    ```python
    @celery.task
    def generate_daily_summary(user_id: str):
        - Fetch new papers (24h)
        - Group by categories
        - Generate summary email
        - Update recommendations
    ```
    (Tasks: Daily Summary).

- [ ] 55. Implement cleanup tasks:
    - Old task cleanup
    - Cache expiration
    - Temporary file removal
    - Log rotation
    (Tasks: Maintenance).

- [ ] 56. Set up Celery Beat schedules:
    ```python
    - Email check: Every 30 minutes
    - Daily summary: 9 AM user timezone
    - Cleanup: Daily at 3 AM
    - Stats calculation: Hourly
    ```
    (Tasks: Scheduling).

### 2.9 Testing

- [ ] 57. Set up pytest configuration in `backend/pytest.ini`:
    - Test discovery patterns
    - Coverage settings
    - Async test support
    - Fixture scopes
    (Testing: Config).

- [ ] 58. Create test fixtures in `backend/tests/conftest.py`:
    - Test database setup
    - Authenticated client
    - Sample data factories
    - Mock services
    (Testing: Fixtures).

- [ ] 59. Write unit tests for services:
    - Auth service tests
    - Email parser tests
    - AI service mocking
    - Paper processor tests
    (Testing: Unit).

- [ ] 60. Create API integration tests:
    - Authentication flow
    - CRUD operations
    - Search functionality
    - Task triggering
    (Testing: Integration).

- [ ] 61. Implement performance tests:
    - API response times
    - Database query optimization
    - Concurrent user handling
    - Memory usage
    (Testing: Performance).

- [ ] 62. Add security tests:
    - SQL injection attempts
    - XSS prevention
    - Authentication bypass
    - Rate limit testing
    (Testing: Security).

## Phase 3: Frontend Development

### 3.1 Project Setup with Next.js 14

- [ ] 1. Create frontend directory and initialize Next.js:
    ```bash
    cd /Users/echo/codeProjects/paper-summarizer/paper-agent
    npx create-next-app@14 frontend --typescript --app --tailwind --no-src-dir
    cd frontend
    ```
    (Frontend: Setup).

- [ ] 2. Install core dependencies:
    ```bash
    npm install @tanstack/react-query @tanstack/react-query-devtools zustand 
    npm install react-hook-form @hookform/resolvers zod
    npm install axios date-fns
    ```
    (Frontend: Core Deps).

- [ ] 3. Install UI dependencies:
    ```bash
    npm install class-variance-authority clsx tailwind-merge
    npm install lucide-react @radix-ui/react-avatar @radix-ui/react-dialog
    npm install @radix-ui/react-dropdown-menu @radix-ui/react-label
    ```
    (Frontend: UI Deps).

- [ ] 4. Initialize shadcn/ui:
    ```bash
    npx shadcn-ui@latest init
    # Choose: TypeScript, Tailwind CSS, CSS variables, React Server Components
    ```
    (Frontend: shadcn).

- [ ] 5. Install shadcn/ui components:
    ```bash
    npx shadcn-ui@latest add button card dialog form input label 
    npx shadcn-ui@latest add select toast dropdown-menu avatar
    npx shadcn-ui@latest add table tabs badge command
    ```
    (Frontend: Components).

- [ ] 6. Create project structure:
    ```bash
    mkdir -p app/{auth,dashboard,api}
    mkdir -p app/dashboard/{papers,keywords,settings}
    mkdir -p components/{ui,layout,papers,auth,keywords}
    mkdir -p lib/{api,utils,validations}
    mkdir -p hooks stores types
    ```
    (Frontend: Structure).

### 3.2 Core Infrastructure

- [ ] 7. Create API client in `frontend/lib/api/client.ts`:
    ```typescript
    - Axios instance configuration
    - Base URL from environment
    - Request/response interceptors
    - Token refresh logic
    - Error handling
    ```
    (Frontend: API Client).

- [ ] 8. Implement authentication interceptor:
    - Add bearer token to requests
    - Handle 401 responses
    - Automatic token refresh
    - Logout on refresh failure
    (Frontend: Auth Interceptor).

- [ ] 9. Set up React Query in `frontend/lib/api/query-client.ts`:
    - Query client configuration
    - Default options
    - Retry logic
    - Cache time settings
    (Frontend: React Query).

- [ ] 10. Create auth store in `frontend/stores/auth-store.ts`:
    ```typescript
    - User state
    - Token management
    - Login/logout actions
    - Persist to localStorage
    ```
    (Frontend: Auth Store).

- [ ] 11. Implement auth provider in `frontend/components/providers/auth-provider.tsx`:
    - Token validation on mount
    - Auto-refresh setup
    - User context provision
    (Frontend: Auth Provider).

- [ ] 12. Create middleware in `frontend/middleware.ts`:
    - Protected route checking
    - Redirect to login
    - Public route list
    (Frontend: Middleware).

### 3.3 Authentication Pages

- [ ] 13. Create login page in `frontend/app/(auth)/login/page.tsx`:
    - Email/password form
    - Remember me checkbox
    - Forgot password link
    - Social login placeholders
    - Form validation with Zod
    (UI: Login).

- [ ] 14. Implement registration page:
    - Multi-step form
    - Email validation
    - Password strength meter
    - Terms acceptance
    - Success confirmation
    (UI: Register).

- [ ] 15. Create password reset flow:
    - Request page with email
    - Token validation page
    - New password form
    - Success redirect
    (UI: Password Reset).

- [ ] 16. Add email verification page:
    - Token extraction from URL
    - Auto-verification on load
    - Resend option
    - Success message
    (UI: Email Verify).

- [ ] 17. Create auth layout in `frontend/app/(auth)/layout.tsx`:
    - Center card design
    - Background pattern
    - Logo placement
    - Responsive design
    (UI: Auth Layout).

- [ ] 18. Implement loading states:
    - Button loading spinners
    - Form disable during submit
    - Skeleton screens
    (UI: Loading).

### 3.4 Dashboard Layout

- [ ] 19. Create dashboard layout in `frontend/app/dashboard/layout.tsx`:
    - Sidebar navigation
    - Header with user menu
    - Main content area
    - Mobile responsive
    (UI: Dashboard Layout).

- [ ] 20. Implement sidebar in `frontend/components/layout/sidebar.tsx`:
    - Navigation items
    - Active state
    - Collapse/expand
    - User info section
    - Logout button
    (UI: Sidebar).

- [ ] 21. Create header component:
    - Search bar
    - Notifications icon
    - User dropdown
    - Theme toggle
    (UI: Header).

- [ ] 22. Add breadcrumb navigation:
    - Dynamic path generation
    - Clickable segments
    - Current page highlight
    (UI: Breadcrumbs).

- [ ] 23. Implement theme system:
    - Light/dark toggle
    - System preference
    - Persist selection
    - Smooth transitions
    (UI: Theme).

- [ ] 24. Create mobile navigation:
    - Hamburger menu
    - Slide-out drawer
    - Touch gestures
    - Backdrop overlay
    (UI: Mobile Nav).

### 3.5 Dashboard Home

- [ ] 25. Create dashboard home in `frontend/app/dashboard/page.tsx`:
    - Welcome message
    - Quick stats cards
    - Recent papers
    - Daily recommendations
    (UI: Dashboard Home).

- [ ] 26. Implement stats cards:
    - Total papers count
    - Unread count
    - Keywords count
    - This week's papers
    - Animated counters
    (UI: Stats Cards).

- [ ] 27. Create recommendations section:
    - Paper cards
    - Category badges
    - Quick actions
    - Load more button
    (UI: Recommendations).

- [ ] 28. Add activity timeline:
    - Recent reads
    - New annotations
    - Paper additions
    - Time grouping
    (UI: Activity).

- [ ] 29. Implement quick actions:
    - Add keyword
    - Check emails
    - View unread
    - Export data
    (UI: Quick Actions).

- [ ] 30. Create empty states:
    - No papers message
    - Setup prompts
    - Action buttons
    - Illustrations
    (UI: Empty States).

### 3.6 Paper Management

- [ ] 31. Create paper list page in `frontend/app/dashboard/papers/page.tsx`:
    - Data table component
    - Pagination
    - Sorting
    - Filtering
    - Bulk actions
    (UI: Paper List).

- [ ] 32. Implement paper card in `frontend/components/papers/paper-card.tsx`:
    - Title and authors
    - Summary preview
    - Keywords display
    - Action buttons
    - Read status
    (UI: Paper Card).

- [ ] 33. Create paper detail page:
    - Full summary display
    - Markdown rendering
    - Original link
    - Related papers
    - Export options
    (UI: Paper Detail).

- [ ] 34. Add annotation dialog:
    - Rich text editor
    - Tag input
    - Category selection
    - Save/cancel
    (UI: Annotations).

- [ ] 35. Implement search interface:
    - Search input
    - Filter dropdowns
    - Date range picker
    - Clear filters
    - Search history
    (UI: Search).

- [ ] 36. Create bulk operations:
    - Select all
    - Bulk categorize
    - Bulk export
    - Bulk delete
    (UI: Bulk Ops).

### 3.7 Keyword Management

- [ ] 37. Create keywords page in `frontend/app/dashboard/keywords/page.tsx`:
    - Keyword list/grid
    - Category tree
    - Add keyword form
    - Import/export
    (UI: Keywords Page).

- [ ] 38. Implement keyword input:
    - Auto-complete
    - Validation
    - Duplicate check
    - Quick add
    (UI: Keyword Input).

- [ ] 39. Create category manager:
    - Tree view
    - Drag and drop
    - Add/edit/delete
    - Color picker
    - Icon selector
    (UI: Categories).

- [ ] 40. Add keyword cloud:
    - Size by usage
    - Interactive clicks
    - Filter by category
    - Responsive layout
    (UI: Word Cloud).

- [ ] 41. Implement import/export:
    - File upload
    - CSV/JSON support
    - Preview changes
    - Conflict resolution
    (UI: Import Export).

- [ ] 42. Create keyword suggestions:
    - AI-powered suggestions
    - Based on papers
    - Approval interface
    - Batch add
    (UI: Suggestions).

### 3.8 Settings Pages

- [ ] 43. Create settings layout:
    - Tab navigation
    - Section headers
    - Save notifications
    - Responsive design
    (UI: Settings Layout).

- [ ] 44. Implement profile settings:
    - Avatar upload
    - Name/email edit
    - Bio section
    - Time zone selection
    (UI: Profile).

- [ ] 45. Create email settings:
    - Email list
    - Add email form
    - Provider guides
    - Test connection
    - Sync schedule
    (UI: Email Settings).

- [ ] 46. Add security settings:
    - Password change
    - Two-factor auth
    - Active sessions
    - Login history
    (UI: Security).

- [ ] 47. Implement preferences:
    - Language selection
    - Date format
    - Notification settings
    - Display density
    (UI: Preferences).

- [ ] 48. Create data management:
    - Export all data
    - Import data
    - Delete account
    - Privacy settings
    (UI: Data Mgmt).

### 3.9 Responsive Design

- [ ] 49. Optimize for mobile:
    - Touch-friendly buttons
    - Swipe gestures
    - Bottom navigation
    - Adaptive layouts
    (UI: Mobile).

- [ ] 50. Create tablet layouts:
    - Two-column views
    - Collapsible panels
    - Optimal spacing
    (UI: Tablet).

- [ ] 51. Implement responsive tables:
    - Horizontal scroll
    - Column priority
    - Mobile cards
    - Sticky headers
    (UI: Tables).

- [ ] 52. Add responsive modals:
    - Full-screen mobile
    - Proper sizing
    - Touch dismissal
    - Keyboard support
    (UI: Modals).

- [ ] 53. Create print styles:
    - Hide navigation
    - Optimize layout
    - Page breaks
    - Print preview
    (UI: Print).

- [ ] 54. Test accessibility:
    - Keyboard navigation
    - Screen reader support
    - ARIA labels
    - Color contrast
    (UI: A11y).

### 3.10 Performance Optimization

- [ ] 55. Implement code splitting:
    - Route-based splitting
    - Component lazy loading
    - Dynamic imports
    (Performance: Splitting).

- [ ] 56. Add image optimization:
    - Next.js Image component
    - Lazy loading
    - Format selection
    - Responsive sizes
    (Performance: Images).

- [ ] 57. Create loading states:
    - Skeleton screens
    - Progressive loading
    - Optimistic updates
    (Performance: Loading).

- [ ] 58. Implement caching:
    - React Query caching
    - Static asset caching
    - Service worker
    (Performance: Cache).

- [ ] 59. Add performance monitoring:
    - Web Vitals tracking
    - Error boundaries
    - Analytics integration
    (Performance: Monitoring).

- [ ] 60. Optimize bundle size:
    - Tree shaking
    - Dependency analysis
    - Compression
    - CDN usage
    (Performance: Bundle).

## Phase 4: Integration and Testing

### 4.1 Docker Configuration

- [ ] 1. Create root `docker-compose.yml`:
    ```yaml
    services:
      postgres:
        image: postgres:15-alpine
        environment:
          POSTGRES_DB: paper_agent
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: ${DB_PASSWORD}
        volumes:
          - postgres_data:/var/lib/postgresql/data
        ports:
          - "5432:5432"
      
      redis:
        image: redis:7-alpine
        ports:
          - "6379:6379"
      
      backend:
        build: ./backend
        environment:
          DATABASE_URL: postgresql://postgres:${DB_PASSWORD}@postgres:5432/paper_agent
          REDIS_URL: redis://redis:6379
        depends_on:
          - postgres
          - redis
        ports:
          - "8000:8000"
      
      frontend:
        build: ./frontend
        environment:
          NEXT_PUBLIC_API_URL: http://backend:8000
        ports:
          - "3000:3000"
      
      celery:
        build: ./backend
        command: celery -A app.core.celery_app worker --loglevel=info
        depends_on:
          - backend
          - redis
      
      celery-beat:
        build: ./backend
        command: celery -A app.core.celery_app beat --loglevel=info
        depends_on:
          - backend
          - redis
    ```
    (Docker: Compose).

- [ ] 2. Create backend Dockerfile:
    ```dockerfile
    FROM python:3.11-slim as builder
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --user -r requirements.txt
    
    FROM python:3.11-slim
    WORKDIR /app
    COPY --from=builder /root/.local /root/.local
    COPY . .
    ENV PATH=/root/.local/bin:$PATH
    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    ```
    (Docker: Backend).

- [ ] 3. Create frontend Dockerfile:
    ```dockerfile
    FROM node:18-alpine as builder
    WORKDIR /app
    COPY package*.json .
    RUN npm ci
    COPY . .
    RUN npm run build
    
    FROM node:18-alpine
    WORKDIR /app
    COPY --from=builder /app/.next/standalone ./
    COPY --from=builder /app/.next/static ./.next/static
    COPY --from=builder /app/public ./public
    EXPOSE 3000
    CMD ["node", "server.js"]
    ```
    (Docker: Frontend).

- [ ] 4. Create Nginx configuration:
    - Reverse proxy setup
    - SSL termination
    - Rate limiting
    - Compression
    - Cache headers
    (Docker: Nginx).

- [ ] 5. Add health checks:
    - Database connection
    - Redis connection
    - API endpoints
    - Frontend status
    (Docker: Health).

- [ ] 6. Configure volumes:
    - Database persistence
    - Upload directory
    - Log files
    - SSL certificates
    (Docker: Volumes).

### 4.2 Environment Setup

- [ ] 7. Create `.env.example` files:
    - Backend variables
    - Frontend variables
    - Docker variables
    - Documentation
    (Env: Templates).

- [ ] 8. Implement secrets management:
    - Environment validation
    - Secret rotation
    - Vault integration prep
    (Env: Secrets).

- [ ] 9. Create environment configs:
    - Development
    - Staging
    - Production
    - Testing
    (Env: Configs).

- [ ] 10. Add configuration validation:
    - Required variables check
    - Type validation
    - Default values
    - Error messages
    (Env: Validation).

### 4.3 Database Management

- [ ] 11. Create init scripts:
    - Database creation
    - User permissions
    - Extensions (pg_trgm)
    - Initial data
    (DB: Init).

- [ ] 12. Implement backup script:
    ```bash
    #!/bin/bash
    # Automated PostgreSQL backup
    # With compression and rotation
    # S3 upload option
    ```
    (DB: Backup).

- [ ] 13. Create restore script:
    - Backup validation
    - Point-in-time recovery
    - Test restore
    (DB: Restore).

- [ ] 14. Add migration CI checks:
    - Auto-migration on deploy
    - Rollback capability
    - Migration testing
    (DB: Migrations).

### 4.4 Integration Testing

- [ ] 15. Set up E2E framework:
    - Playwright installation
    - Test structure
    - Page objects
    - Fixtures
    (E2E: Setup).

- [ ] 16. Create auth E2E tests:
    - Registration flow
    - Login/logout
    - Password reset
    - Email verification
    (E2E: Auth).

- [ ] 17. Test paper workflow:
    - Email setup
    - Paper fetching
    - Annotation
    - Search
    (E2E: Papers).

- [ ] 18. Test keyword management:
    - Add/edit/delete
    - Categories
    - Import/export
    (E2E: Keywords).

- [ ] 19. Create performance tests:
    - Load testing with k6
    - API benchmarks
    - Database stress
    - Frontend metrics
    (E2E: Performance).

- [ ] 20. Add visual regression:
    - Screenshot comparison
    - Component snapshots
    - Cross-browser testing
    (E2E: Visual).

### 4.5 Monitoring Setup

- [ ] 21. Configure Prometheus:
    - Metrics collection
    - Custom metrics
    - Alerting rules
    - Dashboards
    (Monitor: Metrics).

- [ ] 22. Set up Grafana:
    - Import dashboards
    - Custom panels
    - Alert channels
    - User access
    (Monitor: Grafana).

- [ ] 23. Implement logging:
    - Centralized logging
    - Log aggregation
    - Search interface
    - Retention policies
    (Monitor: Logs).

- [ ] 24. Add APM:
    - Transaction tracing
    - Error tracking
    - Performance profiling
    - User monitoring
    (Monitor: APM).

- [ ] 25. Create alerts:
    - System health
    - Error rates
    - Performance degradation
    - Security events
    (Monitor: Alerts).

### 4.6 Security Hardening

- [ ] 26. Implement rate limiting:
    - API endpoints
    - Login attempts
    - Email sending
    - Configuration
    (Security: Rate Limit).

- [ ] 27. Configure CORS:
    - Allowed origins
    - Credentials handling
    - Preflight caching
    (Security: CORS).

- [ ] 28. Add security headers:
    - CSP policy
    - HSTS
    - X-Frame-Options
    - XSS protection
    (Security: Headers).

- [ ] 29. Set up WAF rules:
    - SQL injection protection
    - XSS prevention
    - Bot detection
    - DDoS mitigation
    (Security: WAF).

- [ ] 30. Create security scanning:
    - Dependency scanning
    - Container scanning
    - Code analysis
    - Penetration testing
    (Security: Scanning).

## Phase 5: Deployment and Delivery

### 5.1 Production Optimization

- [ ] 1. Optimize containers:
    - Multi-stage builds
    - Layer caching
    - Size reduction
    - Security hardening
    (Deploy: Containers).

- [ ] 2. Database optimization:
    - Connection pooling
    - Query optimization
    - Index tuning
    - Vacuum scheduling
    (Deploy: Database).

- [ ] 3. Configure CDN:
    - Static assets
    - API caching
    - Geographic distribution
    - Purge strategy
    (Deploy: CDN).

- [ ] 4. Implement auto-scaling:
    - Horizontal scaling
    - Load balancing
    - Health checks
    - Graceful shutdown
    (Deploy: Scaling).

### 5.2 CI/CD Pipeline

- [ ] 5. Create GitHub Actions:
    ```yaml
    - Lint and format check
    - Unit test execution
    - Build verification
    - Security scanning
    - Docker build and push
    - Deployment triggers
    ```
    (CI/CD: Actions).

- [ ] 6. Implement deployment:
    - Blue-green deployment
    - Database migrations
    - Cache warming
    - Smoke tests
    - Rollback procedure
    (CI/CD: Deploy).

- [ ] 7. Add quality gates:
    - Code coverage threshold
    - Performance benchmarks
    - Security scan pass
    - Documentation check
    (CI/CD: Quality).

### 5.3 Documentation

- [ ] 8. Update README.md:
    ```markdown
    # Paper Summary Agent
    
    ## Overview
    AI-powered academic paper management system with Gemini Flash 2.0
    
    ## Features
    - Automatic paper fetching from email subscriptions
    - AI-powered summarization using Gemini Flash 2.0
    - Multi-user support with custom keywords
    - Advanced search and annotation capabilities
    - Real-time notifications and daily summaries
    
    ## Quick Start
    1. Install UV: `curl -LsSf https://astral.sh/uv/install.sh | sh`
    2. Clone repository: `git clone <repo-url>`
    3. Navigate to project: `cd paper-agent`
    4. Create virtual environment: `uv venv --python 3.11`
    5. Activate environment: `source .venv/bin/activate`
    6. Copy environment file: `cp .env.example .env`
    7. Start services: `docker-compose up -d`
    8. Access application: http://localhost:3000
    
    ## Architecture
    - **Backend**: FastAPI with PostgreSQL and Redis
    - **Frontend**: Next.js 14 with shadcn/ui
    - **AI**: OpenRouter API with Gemini Flash 2.0
    - **Tasks**: Celery with Redis broker
    - **Deployment**: Docker containers with Nginx
    
    ## Development
    See [Implementation Plan](docs/Implementation-Plan.md) for detailed development guide.
    
    ## Contributing
    1. Fork the repository
    2. Create feature branch
    3. Follow coding standards
    4. Write tests
    5. Submit pull request
    ```
    (Docs: README).

- [ ] 9. Write API documentation:
    - OpenAPI specification
    - Authentication guide
    - Endpoint reference
    - Code examples
    - Rate limits
    (Docs: API).

- [ ] 10. Create user guide:
    - Getting started tutorial
    - Feature walkthroughs
    - Video demonstrations
    - FAQ section
    - Troubleshooting guide
    (Docs: User).

- [ ] 11. Add developer docs:
    - Architecture overview
    - Development setup
    - Testing guide
    - Deployment guide
    - API integration examples
    (Docs: Developer).

### 5.4 Demo and Launch

- [ ] 12. Prepare demo data:
    - Sample academic papers
    - Demo user accounts
    - Pre-configured keyword sets
    - Example annotations
    - Category structures
    (Demo: Data).

- [ ] 13. Create demo environment:
    - Isolated instance
    - Reset capability
    - Guided tour mode
    - Sample workflows
    (Demo: Environment).

- [ ] 14. Record demo videos:
    - Product overview (5 minutes)
    - User onboarding flow
    - Paper management workflow
    - Search and filtering features
    - AI summarization showcase
    (Demo: Videos).

- [ ] 15. Launch preparation:
    - Final system testing
    - Performance validation
    - Security audit completion
    - Documentation review
    - Stakeholder sign-off
    (Launch: Prep).

## Estimated Timeline

- **Phase 0**: 1 day (UV Setup and Planning) ✅
- **Phase 1**: 2-3 days (Environment Setup)
- **Phase 2**: 2-3 weeks (Backend Development)
- **Phase 3**: 2 weeks (Frontend Development)
- **Phase 4**: 1 week (Integration and Testing)
- **Phase 5**: 1 week (Deployment and Delivery)

**Total**: 6-7 weeks for MVP

## Key Milestones

- **M0**: UV environment ready, Implementation Plan created ✅
- **M1**: Development environment ready (Day 3)
- **M2**: Backend API complete with authentication (Week 2)
- **M3**: Core paper processing workflow functional (Week 3)
- **M4**: Frontend UI complete and integrated (Week 5)
- **M5**: System tested and deployment-ready (Week 6)
- **M6**: Production launch (Week 7)

## Success Criteria

- [x] UV environment properly configured with Python 3.11
- [x] Implementation Plan document created
- [x] Project structure established
- [ ] All dependencies managed through UV
- [ ] System handles 100+ concurrent users
- [ ] Paper processing < 30 seconds per paper using Gemini Flash 2.0
- [ ] 99.5% uptime achieved
- [ ] Full test coverage > 80%
- [ ] Documentation complete and reviewed
- [ ] All security best practices implemented

## Risk Mitigation

1. **UV Compatibility**: Ensure all packages work with UV package manager - test installations early
2. **OpenRouter API Limits**: Implement caching, rate limiting, and fallback mechanisms
3. **Firecrawl Availability**: Create alternative scraping methods and API fallbacks
4. **Email Provider Blocks**: Support multiple email services and authentication methods
5. **Performance Issues**: Design for horizontal scaling and implement monitoring from start
6. **Security Vulnerabilities**: Regular security audits, dependency scanning, and penetration testing
7. **Gemini Model Changes**: Abstract model interface to allow easy switching between AI providers

## Technical Notes

### UV Package Management
- UV provides faster dependency resolution than traditional pip
- UV's lock file ensures reproducible builds across environments
- Consider using UV's workspace feature for monorepo management if expanding
- UV integrates well with Docker for production builds
- UV automatically manages Python versions and virtual environments

### AI Integration Considerations
- Gemini Flash 2.0 optimized for speed and cost-effectiveness
- Implement request batching for efficiency
- Use structured prompts for consistent output format
- Monitor token usage and implement user quotas
- Cache AI responses to reduce API calls and costs

### Database Optimization
- Use PostgreSQL's full-text search capabilities
- Implement proper indexing strategy for paper search
- Consider partitioning for large datasets
- Regular maintenance tasks for performance

### Security Best Practices
- JWT token rotation and blacklisting
- API rate limiting per user and endpoint
- Input validation and sanitization
- HTTPS everywhere with proper certificate management
- Regular security dependency updates

This implementation plan provides a comprehensive roadmap for building a production-ready paper summarization system using modern technologies and best practices.