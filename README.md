# Hotel Manager - FastAPI Hotel Management System | Python 3.12 • FastAPI • SQLAlchemy • PostgreSQL

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128+-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A robust, asynchronous hotel management API built with clean architecture principles. This system provides comprehensive booking, guest, room, and user management with JWT authentication and enterprise-grade error handling.
## Architectural Overview
The project follows **layered architecture** with clear separation of concerns:
```
src/
├── routers/          # API endpoints and request handling
├── services/         # Business logic and orchestration
├── repositories/     # Data access layer abstraction
├── models/          # SQLAlchemy ORM models
├── schemas/         # Pydantic request/response validation
├── utils/           # Security, hashing, and utilities
├── handlers/        # Global exception handling
├── config/          # Environment configuration
└── database/        # Database session management
```
**Benefits of this architecture:**
- **Testability**: Each layer can be unit tested in isolation
- **Maintainability**: Clear boundaries make modifications predictable
- **Scalability**: Service layer enables easy business logic expansion
- **Security**: Centralized authentication and validation
## Tech Stack
- **Runtime**: Python 3.12+
- **Framework**: FastAPI 0.128+ with async support
- **ORM**: SQLAlchemy 2.0+ with async operations
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Authentication**: JWT with PyJWT
- **Password Hashing**: Argon2 via pwdlib
- **Validation**: Pydantic v2 settings and schemas
- **Migration**: Alembic for database versioning
- **Server**: Uvicorn ASGI server
- **CORS**: Cross-origin resource sharing configured
## Quick Start
### Prerequisites
- Python 3.12 or higher
- Git
### Installation
```bash
# Clone the repository
git clone https://github.com/JoaoPedroHenriquesB/HotelManager.git
cd HotelManager

# Create and activate virtual environment
uv venv

# Windows
.venv\Scripts\activate

# Linux / MacOS
source.venv/bin/activate

# Install dependencies
uv sync

# Apply database migrations
alembic upgrade head

# Run application
uv run main.py
```
The API will be available at `http://localhost:8000`
## API Documentation
Once running, access interactive API documentation:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
### Key Endpoints
- `POST /auth/login` - User authentication
- `GET /users` - User management (admin only)
- `GET /rooms` - Room inventory
- `POST /guests` - Guest registration
- `POST /bookings` - Stay reservations
## Security Features
- **JWT Authentication**: Stateless token-based auth with configurable expiration
- **Password Security**: Argon2 hashing for resistance against brute force attacks
- **Role-Based Access**: Admin-only endpoints with `requires_admin` decorator
- **Input Validation**: Comprehensive Pydantic schema validation
- **CORS Configuration**: Controlled cross-origin access
- **SQL Injection Protection**: SQLAlchemy ORM parameterized queries
## Error Handling
The system implements **global exception handling** with consistent error responses:
```python
# Custom exceptions for different scenarios
- TokenExpiredSignatureError
- CouldNotValidateCredentialsError  
- NotAdminError
- ValidationError
```
All errors return structured JSON with appropriate HTTP status codes for client-side handling.
## Contact
**João Pedro Henriques** - Backend Developer
- **E-Mail**: mailto:joaopedrohbalbino@gmail.com
- **GitHub**: https://github.com/JoaoPedroHenriquesB
