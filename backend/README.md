# Resume Management System - Backend

FastAPI-based backend for the Resume Management System.

## Setup

### 1. Create and activate virtual environment

```bash
cd backend
uv venv
source .venv/bin/activate  # On macOS/Linux
```

### 2. Install dependencies

```bash
uv pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
# Edit .env and set the following required values:
#   SECRET_KEY  - generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"
#   ADMIN_USERNAME - the admin login username
#   ADMIN_PASSWORD - the admin login password (use a strong password in production)
```

### 4. Run the application

```bash
# Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using the run script
python run.py
```

The API will be available at:
- API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Admin Credentials

Admin credentials are **required** and have no defaults. The application will refuse to start if they are not set.

Set them in your `.env` file:

```
ADMIN_USERNAME="your-admin-username"
ADMIN_PASSWORD="your-strong-password"
```

See `.env.example` for reference.

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login and get access token
- `GET /api/auth/verify` - Verify token
- `POST /api/auth/logout` - Logout

### Personal Information
- `GET /api/personal-info` - Get personal info (public)
- `POST /api/personal-info` - Create personal info (auth required)
- `PUT /api/personal-info` - Update personal info (auth required)

### Work Experience
- `GET /api/work-experience` - Get all work experiences (public)
- `GET /api/work-experience/{id}` - Get specific work experience (public)
- `POST /api/work-experience` - Create work experience (auth required)
- `PUT /api/work-experience/{id}` - Update work experience (auth required)
- `DELETE /api/work-experience/{id}` - Delete work experience (auth required)

## Database

The application uses SQLite database (`resume.db`) which will be created automatically on first run.

## Development

### Run tests

```bash
pytest
```

### Code formatting

```bash
black app/
isort app/
```
