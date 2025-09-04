# Truthbrush API Server

A professional FastAPI server that exposes Truth Social data via the truthbrush package. 

## Project Structure

```
truthbrush-api/
├── app/                    # Main application package
│   ├── main.py            # FastAPI application entry point
│   ├── api/               # API routes and endpoints
│   │   └── endpoints/
│   │       └── statuses.py # Statuses endpoint
│   ├── core/              # Core configuration and utilities
│   │   ├── config.py      # Application settings
│   │   ├── logging.py     # Logging configuration
│   │   └── auth.py        # Authentication utilities
│   └── services/          # Business logic layer
│       └── truthbrush_service.py # Truth Social integration
├── logs/                  # Application logs
├── data/                  # Data files
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .gitignore           # Git ignore rules
```

## Setup

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your credentials:**

   Create a `.env` file in the project root:

   ```
   # Truth Social credentials
   TRUTHSOCIAL_USERNAME=your_truthsocial_username
   TRUTHSOCIAL_PASSWORD=your_truthsocial_password
   TRUTHSOCIAL_TOKEN=your_token  # (optional)

   # API Authentication credentials
   API_USERNAME=your_api_username
   API_PASSWORD=your_api_password
   ```

3. **Run the API server:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Authentication

**All endpoints require JWT Bearer Authentication.**

The API uses JWT (JSON Web Token) authentication. You must first obtain a token, then include it in all subsequent requests.

### Step 1: Get JWT Token

**Login via OAuth2 form (recommended):**
```bash
curl -X POST "http://localhost:8000/auth/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=your_api_username&password=your_api_password"
```

**Login via JSON:**
```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "your_api_username", "password": "your_api_password"}'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Step 2: Use JWT Token in Requests

**Using curl:**
```bash
curl -H "Authorization: Bearer your_jwt_token" "http://localhost:8000/statuses?username=realDonaldTrump&created_after=2025-07-23"
```

**Using Postman:**
1. Go to the "Authorization" tab
2. Type: Bearer Token
3. Enter your JWT token

### Default credentials (if not set in .env):

- Username: `admin`
- Password: `password`

**⚠️ Security Notes:** 
- Change these defaults in your `.env` file for production use!
- JWT tokens expire after 30 minutes - you'll need to get a new token when it expires

## API Endpoints

### Authentication Endpoints

#### Get JWT Token (OAuth2 Form)
```
POST /auth/token
```
**Content-Type:** `application/x-www-form-urlencoded`

**Parameters:**
- `username`: Your API username
- `password`: Your API password

#### Get JWT Token (JSON)
```
POST /auth/login
```
**Content-Type:** `application/json`

**Body:**
```json
{
  "username": "your_api_username",
  "password": "your_api_password"
}
```

### Get User Statuses

```
GET /statuses?username={username}&created_after={date}&replies={bool}&pinned={bool}
```

**Parameters:**

- `username` (required): Truth Social username
- `created_after` (optional): ISO date string (e.g., "2025-07-23" or "2025-07-23T00:00:00")
- `replies` (optional): Include replies (default: false)
- `pinned` (optional): Only pinned posts (default: false)

**Example:**

```bash
curl -H "Authorization: Bearer your_jwt_token" "http://localhost:8000/statuses?username=realDonaldTrump&created_after=2025-07-23"
```

### Health Check

```
GET /health
```

### API Documentation

```
GET /docs
```

Interactive API documentation (Swagger UI) - requires JWT Bearer authentication

## Features

- **Professional Structure**: Clean separation of concerns with proper layering
- **Configuration Management**: Centralized settings via environment variables
- **JWT Authentication**: Bearer token authentication for all endpoints with 30-minute expiration
- **Dual Login Methods**: OAuth2 form-based and JSON-based authentication endpoints
- **Logging**: Both console and file logging with configurable levels
- **Error Handling**: Proper HTTP status codes and error messages
- **CORS Support**: Cross-origin requests enabled
- **API Documentation**: Auto-generated with FastAPI

## Development

The application follows a layered architecture:

1. **API Layer** (`app/api/`): FastAPI routes and request/response handling
2. **Service Layer** (`app/services/`): Business logic and external integrations
3. **Core Layer** (`app/core/`): Configuration, logging, authentication, and utilities

This structure makes it easy to:

- Add new endpoints
- Modify business logic
- Test individual components
- Maintain and scale the application

## Logging

Logs are written to both:

- Console (terminal output)
- File (`logs/truthbrush_api.log`)

Each API call is logged with client IP, authenticated user, and parameters for monitoring and debugging.

## Security

- All endpoints require JWT Bearer Authentication
- JWT tokens expire after 30 minutes for enhanced security
- Credentials are stored in environment variables (not in code)
- Secure credential comparison using `secrets.compare_digest()`
- JWT tokens are signed with HS256 algorithm
- Proper HTTP status codes for authentication failures
