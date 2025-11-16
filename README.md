# My FastAPI Project

A modern FastAPI application with SQLAlchemy, PostgreSQL, and a clean layered architecture.

## Features

- RESTful API with FastAPI
- PostgreSQL database with SQLAlchemy ORM
- Pydantic schemas for request/response validation
- Clean architecture with separation of concerns
- Database migrations support (Alembic)
- Environment-based configuration

## Tech Stack

- **FastAPI** 0.121.2 - Modern, fast web framework
- **SQLAlchemy** 2.0.44 - ORM for database operations
- **PostgreSQL** - Database (via psycopg2-binary)
- **Alembic** 1.17.2 - Database migrations
- **Pydantic** - Data validation and settings management
- **Uvicorn** - ASGI server
- **Gunicorn** - Production WSGI server
- **Pytest** - Testing framework

## Project Structure

```
myfastapi/
├── alembic/                    # Alembic migrations directory
│   ├── versions/               # Migration files
│   ├── env.py                  # Alembic environment configuration
│   └── script.py.mako          # Migration template
├── alembic.ini                 # Alembic configuration file
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── api/
│   │   ├── api_router.py       # Main API router
│   │   ├── deps.py             # Dependency injection (DB sessions)
│   │   └── v1/
│   │       └── users.py        # User endpoints
│   ├── core/
│   │   └── config.py           # Application settings
│   ├── db/
│   │   ├── base.py             # SQLAlchemy base
│   │   ├── session.py          # Database session factory
│   │   └── init_db.py          # Database initialization (legacy)
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py             # User SQLAlchemy model
│   ├── schemas/
│   │   └── user.py             # Pydantic schemas (UserCreate, UserRead)
│   └── services/
│       └── user_service.py     # Business logic layer
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Prerequisites

- Python 3.13+
- PostgreSQL database
- Virtual environment (recommended)

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory:

   ```bash
   cd myfastapi
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory:

   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname
   PROJECT_NAME=My FastAPI App
   ENV=development
   DEBUG=True
   ```

5. **Run database migrations**:

   ```bash
   alembic upgrade head
   ```

   This will create all database tables based on the migration files.

## Running the Application

### Development Mode

Run with Uvicorn in development mode (with auto-reload):

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

Run with Gunicorn and Uvicorn workers:

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

The API will be available at:

- **API**: http://localhost:8000
- **Interactive API Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

### Users

- **POST** `/api/v1/users/` - Create a new user

  - Request body: `{"email": "user@example.com", "full_name": "John Doe"}`
  - Returns: Created user object

- **GET** `/api/v1/users/{user_id}` - Get user by ID
  - Returns: User object or 404 if not found

## Database Models

### User

- `id` (Integer, Primary Key)
- `email` (String, Unique, Required)
- `full_name` (String, Optional)

## Database Migrations

This project uses Alembic for database migrations. The Alembic configuration is already set up and uses the `DATABASE_URL` from your `.env` file.

### Common Migration Commands

**Create a new migration** (after modifying models):

```bash
alembic revision --autogenerate -m "Description of changes"
```

**Apply migrations**:

```bash
alembic upgrade head
```

**Rollback one migration**:

```bash
alembic downgrade -1
```

**Rollback to a specific revision**:

```bash
alembic downgrade <revision_id>
```

**View migration history**:

```bash
alembic history
```

**View current database revision**:

```bash
alembic current
```

**Create an empty migration** (for custom SQL):

```bash
alembic revision -m "Description"
```

### Migration Workflow

1. Modify your SQLAlchemy models in `app/models/`
2. Generate a migration: `alembic revision --autogenerate -m "your message"`
3. Review the generated migration file in `alembic/versions/`
4. Apply the migration: `alembic upgrade head`

## Configuration

Configuration is managed through environment variables loaded from `.env`:

- `DATABASE_URL` - PostgreSQL connection string (required)
- `PROJECT_NAME` - Application name (default: "My FastAPI App")
- `ENV` - Environment (default: "development")
- `DEBUG` - Debug mode (default: False)

## Development

### Running Tests

```bash
pytest
```

### Code Structure

The project follows a clean architecture pattern:

- **API Layer** (`app/api/`) - HTTP endpoints and routing
- **Service Layer** (`app/services/`) - Business logic
- **Model Layer** (`app/models/`) - Database models (SQLAlchemy)
- **Schema Layer** (`app/schemas/`) - Data validation (Pydantic)

## Architecture & Data Flow

This section provides a comprehensive overview of how data flows through the application, from HTTP requests to database operations and back.

### Data Flow Summary

**Request Flow (Incoming):**

1. **HTTP Request** → Client sends request to Uvicorn ASGI server
2. **FastAPI Router** → Routes request to appropriate endpoint based on URL
3. **API Endpoint** → Receives request, validates with Pydantic schemas
4. **Dependency Injection** → `get_db()` creates and provides database session
5. **Service Layer** → Business logic processes the request
6. **SQLAlchemy Model** → ORM operations interact with database
7. **PostgreSQL** → Database executes query and returns data

**Response Flow (Outgoing):**

1. **Database** → Returns data (model instances or None)
2. **Service Layer** → Returns processed data
3. **API Endpoint** → Converts SQLAlchemy models to Pydantic schemas
4. **FastAPI** → Serializes to JSON
5. **HTTP Response** → Returns to client

**Key Transformations:**

- **JSON → Pydantic Schema**: Request validation and type safety
- **Pydantic Schema → SQLAlchemy Model**: Data persistence
- **SQLAlchemy Model → Pydantic Schema**: Response serialization
- **Pydantic Schema → JSON**: HTTP response

### System Architecture

```mermaid
graph TB
    Client[Client/HTTP Request] --> Uvicorn[Uvicorn ASGI Server]
    Uvicorn --> FastAPI[FastAPI Application<br/>app.main:app]
    FastAPI --> Router[API Router<br/>app.api.api_router]
    Router --> Endpoints[API Endpoints<br/>app.api.v1.users]
    Endpoints --> Dependencies[Dependencies<br/>app.api.deps]
    Dependencies --> Services[Service Layer<br/>app.services.user_service]
    Services --> Models[SQLAlchemy Models<br/>app.models.user]
    Models --> DB[(PostgreSQL Database)]

    Endpoints --> Schemas[Pydantic Schemas<br/>app.schemas.user]
    Schemas --> Client

    Config[Configuration<br/>app.core.config] --> FastAPI
    Config --> Services
    Config --> DB

    Alembic[Alembic Migrations] --> DB

    style Client fill:#e1f5ff
    style DB fill:#ffebee
    style FastAPI fill:#f3e5f5
    style Services fill:#e8f5e9
    style Models fill:#fff3e0
```

### Request Flow: Creating a User (POST)

```mermaid
sequenceDiagram
    participant Client
    participant Uvicorn
    participant FastAPI
    participant Router
    participant Endpoint
    participant Deps
    participant Schema
    participant Service
    participant Model
    participant Database

    Client->>Uvicorn: POST /api/v1/users/<br/>{email, full_name}
    Uvicorn->>FastAPI: HTTP Request
    FastAPI->>Router: Route to /users/
    Router->>Endpoint: api_create_user()

    Note over Endpoint: Validate request body
    Endpoint->>Schema: UserCreate schema validation
    Schema-->>Endpoint: Validated data

    Note over Endpoint: Get database session
    Endpoint->>Deps: get_db() dependency
    Deps->>Database: Create session
    Database-->>Deps: Session object
    Deps-->>Endpoint: db: Session

    Note over Endpoint: Call service layer
    Endpoint->>Service: create_user(db, payload)

    Note over Service: Convert schema to model
    Service->>Model: User(**user_in.model_dump())
    Model-->>Service: User instance

    Note over Service: Persist to database
    Service->>Database: db.add(user)
    Service->>Database: db.commit()
    Service->>Database: db.refresh(user)
    Database-->>Service: User with ID

    Service-->>Endpoint: User model

    Note over Endpoint: Convert model to response
    Endpoint->>Schema: UserRead.from_orm(user)
    Schema-->>Endpoint: UserRead schema

    Endpoint-->>Router: Response
    Router-->>FastAPI: JSON response
    FastAPI-->>Uvicorn: HTTP 201 Created
    Uvicorn-->>Client: Response with user data
```

### Request Flow: Getting a User (GET)

```mermaid
sequenceDiagram
    participant Client
    participant Uvicorn
    participant FastAPI
    participant Router
    participant Endpoint
    participant Deps
    participant Service
    participant Model
    participant Database
    participant Schema

    Client->>Uvicorn: GET /api/v1/users/{user_id}
    Uvicorn->>FastAPI: HTTP Request
    FastAPI->>Router: Route to /users/{user_id}
    Router->>Endpoint: api_get_user(user_id)

    Note over Endpoint: Get database session
    Endpoint->>Deps: get_db() dependency
    Deps->>Database: Create session
    Database-->>Deps: Session object
    Deps-->>Endpoint: db: Session

    Note over Endpoint: Call service layer
    Endpoint->>Service: get_user(db, user_id)

    Note over Service: Query database
    Service->>Model: db.get(User, user_id)
    Model->>Database: SELECT query
    Database-->>Model: User row or None
    Model-->>Service: User instance or None

    Service-->>Endpoint: User model or None

    alt User Found
        Note over Endpoint: Convert model to response
        Endpoint->>Schema: UserRead.from_orm(user)
        Schema-->>Endpoint: UserRead schema
        Endpoint-->>Router: Response
        Router-->>FastAPI: JSON response
        FastAPI-->>Uvicorn: HTTP 200 OK
        Uvicorn-->>Client: Response with user data
    else User Not Found
        Endpoint-->>Router: HTTPException(404)
        Router-->>FastAPI: Error response
        FastAPI-->>Uvicorn: HTTP 404 Not Found
        Uvicorn-->>Client: Error message
    end
```

### Data Flow Layers

```mermaid
graph LR
    subgraph "HTTP Layer"
        A[HTTP Request/Response]
    end

    subgraph "API Layer"
        B[FastAPI Router]
        C[API Endpoints]
        D[Request Validation]
    end

    subgraph "Dependency Layer"
        E[get_db Dependency]
        F[Database Session]
    end

    subgraph "Service Layer"
        G[Business Logic]
        H[Data Transformation]
    end

    subgraph "Model Layer"
        I[SQLAlchemy Models]
        J[ORM Operations]
    end

    subgraph "Database Layer"
        K[(PostgreSQL)]
    end

    subgraph "Schema Layer"
        L[Pydantic Schemas]
        M[Data Validation]
    end

    A --> B
    B --> C
    C --> D
    D --> L
    L --> M
    M --> C
    C --> E
    E --> F
    F --> G
    G --> H
    H --> I
    I --> J
    J --> K
    K --> J
    J --> I
    I --> H
    H --> G
    G --> L
    L --> C
    C --> B
    B --> A

    style A fill:#e1f5ff
    style K fill:#ffebee
    style G fill:#e8f5e9
    style L fill:#fff3e0
```

### Database Interaction Flow

```mermaid
graph TD
    Start[Application Start] --> Config[Load Config from .env]
    Config --> DBConfig[Database Configuration]
    DBConfig --> Engine[Create SQLAlchemy Engine]
    Engine --> SessionFactory[Create Session Factory]

    Request[HTTP Request Arrives] --> GetDB[get_db Dependency]
    GetDB --> SessionFactory
    SessionFactory --> CreateSession[Create Database Session]
    CreateSession --> Service[Service Layer]

    Service --> Query{Query Type}
    Query -->|Create| AddModel[Add Model Instance]
    Query -->|Read| GetModel[Get Model by ID]
    Query -->|Update| UpdateModel[Update Model Instance]
    Query -->|Delete| DeleteModel[Delete Model Instance]

    AddModel --> Commit[Commit Transaction]
    GetModel --> Return[Return Model]
    UpdateModel --> Commit
    DeleteModel --> Commit

    Commit --> Refresh[Refresh Model]
    Refresh --> Return
    Return --> CloseSession[Close Session]
    CloseSession --> Response[HTTP Response]

    style Start fill:#e1f5ff
    style Engine fill:#f3e5f5
    style Service fill:#e8f5e9
    style Commit fill:#fff3e0
    style Response fill:#e1f5ff
```

### Component Interaction Overview

```mermaid
graph TB
    subgraph "External"
        HTTP[HTTP Client]
        ENV[.env File]
    end

    subgraph "Application Entry"
        MAIN[main.py<br/>FastAPI App]
        ROUTER[api_router.py<br/>Main Router]
    end

    subgraph "API Layer"
        USERS[users.py<br/>User Endpoints]
        DEPS[deps.py<br/>Dependencies]
    end

    subgraph "Business Logic"
        SERVICE[user_service.py<br/>User Service]
    end

    subgraph "Data Layer"
        SCHEMAS[user.py Schemas<br/>Pydantic Models]
        MODELS[user.py Model<br/>SQLAlchemy Model]
    end

    subgraph "Infrastructure"
        CONFIG[config.py<br/>Settings]
        SESSION[session.py<br/>DB Session]
        BASE[base.py<br/>SQLAlchemy Base]
    end

    subgraph "Database"
        POSTGRES[(PostgreSQL)]
    end

    HTTP --> MAIN
    ENV --> CONFIG
    MAIN --> ROUTER
    ROUTER --> USERS
    USERS --> DEPS
    USERS --> SCHEMAS
    DEPS --> SESSION
    SESSION --> POSTGRES
    USERS --> SERVICE
    SERVICE --> MODELS
    SERVICE --> SCHEMAS
    MODELS --> BASE
    BASE --> POSTGRES
    CONFIG --> SESSION
    CONFIG --> MAIN

    style HTTP fill:#e1f5ff
    style POSTGRES fill:#ffebee
    style SERVICE fill:#e8f5e9
    style SCHEMAS fill:#fff3e0
    style CONFIG fill:#f3e5f5
```

### Data Transformation Flow

```mermaid
graph LR
    subgraph "Request"
        A[JSON Request Body]
        B[UserCreate Schema]
    end

    subgraph "Processing"
        C[Service Layer]
        D[User Model Instance]
    end

    subgraph "Database"
        E[SQLAlchemy ORM]
        F[PostgreSQL Table]
    end

    subgraph "Response"
        G[User Model]
        H[UserRead Schema]
        I[JSON Response]
    end

    A -->|Pydantic Validation| B
    B -->|model_dump| C
    C -->|User**| D
    D -->|db.add| E
    E -->|INSERT| F
    F -->|SELECT| E
    E -->|ORM Mapping| G
    G -->|from_attributes| H
    H -->|JSON Serialization| I

    style A fill:#e1f5ff
    style F fill:#ffebee
    style C fill:#e8f5e9
    style B fill:#fff3e0
    style H fill:#fff3e0
```

## Notes

- The user creation endpoint currently doesn't handle duplicate email errors gracefully. Consider adding proper error handling for `IntegrityError` when email uniqueness is violated.
- Authentication/authorization is not yet implemented.
- Database migrations are managed through Alembic. Always use migrations instead of `init_db.py` for production deployments.

## License

[Add your license here]
