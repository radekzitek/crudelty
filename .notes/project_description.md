# Objective:

- create a system wchich will dynamically read a database structure and generate folllowing:
    - a backend with REST API for the CRUD operations
    - a frontend with a VueJS+Vuetify application to display and manage the data

# Priorities:

## Top priority:

- the system should be able to read the database structure from the database itself
- it should respect the relationships between the tables
- it should create visually appealing UI for the frontend

## Priority 2:

- it should be able to handle authentication and authorization
- it should be able to handle error handling and logging
    - using ELK stack or similar
- it should employ data driven approach to the frontend customization
    - menu structure
    - labels and descriptions

## Optional:

- it should be able to handle data validation and sanitization
- it should be able to handle data encryption and decryption
- it should be able to handle data backup and restore
- it should be able to handle data export and import

# Technology stack:

## Database:

- MySQL

## Backend:

- FastAPI

## Frontend:

- VueJS
- Vuetify

## Authentication:

- OAuth2
- JWT


# Implementation details:

## MariaDB database:

- host: localhost
- port: 3306
- user: root
- password: user1234
- database: organization_db

## Directory structure:

- sql/
- docs/
- .notes/
- tests/
- src/
- .venv/
- backend/
- frontend/
- .gitignore
- .cursorignore
- .cursorrules
- README.md
- LICENSE
- requirements.txt
- setup.py
- Dockerfile
- docker-compose.yml


Project Structure

my-web-app/
├── backend/             # Python FastAPI backend
│   ├── app/            # Main application logic
│   │   ├── __init__.py
│   │   ├── main.py      # FastAPI application entry point
│   │   ├── api/        # API routes and controllers
│   │   │   ├── __init__.py
│   │   │   ├── v1/   # Example: versioned API
│   │   │   │   ├── __init__.py
│   │   │   │   ├── users.py   # User related routes
│   │   │   │   └── items.py   # Item related routes
│   │   ├── core/       # Core functionality (e.g., database, config)
│   │   │   ├── __init__.py
│   │   │   ├── config.py   # Environment-specific configurations
│   │   │   └── database.py # Database connection and setup
│   │   ├── models/     # Data models (e.g., SQLAlchemy or Pydantic)
│   │   │   ├── __init__.py
│   │   │   └── user.py      # User model
│   │   └── schemas/    # Pydantic schemas for request/response validation
│   │       ├── __init__.py
│   │       └── user.py      # User schemas
│   ├── tests/          # Unit and integration tests
│   │   ├── __init__.py
│   │   ├── conftest.py  # Pytest fixtures
│   │   └── test_main.py  # Example test file
│   ├── requirements.txt  # Backend dependencies
│   └── .env.example     # Example environment variables for backend
├── frontend/            # Vue.js + Vuetify frontend
│   ├── public/         # Static assets (e.g., favicon)
│   │   └── index.html  # Base HTML template
│   ├── src/            # Frontend source code
│   │   ├── App.vue     # Root Vue component
│   │   ├── main.js     # Vue application entry point
│   │   ├── assets/      # Images, fonts, etc.
│   │   ├── components/ # Reusable Vue components
│   │   ├── router/     # Vue Router configuration
│   │   │   └── index.js
│   │   ├── store/      # Vuex store (optional, for state management)
│   │   │   └── index.js
│   │   ├── views/      # Page-level Vue components
│   │   └── plugins/    # Vuetify configuration and other plugins
│   │       └── vuetify.js
│   ├── tests/          # Frontend tests (unit, e2e)
│   ├── .env.development  # Development environment variables for frontend
│   ├── .env.integration  # Integration environment variables for frontend
│   ├── .env.test         # Test environment variables for frontend
│   ├── .env.production   # Production environment variables for frontend
│   ├── package.json      # Frontend dependencies and scripts
│   ├── vue.config.js   # Vue CLI configuration
│   └── ...             # Other frontend configuration files
├── scripts/             # Helper scripts (e.g., database migration)
│   ├── db_init.py      # Initialize the database
│   └── ...
├── .gitignore          # Files and folders to be ignored by Git
├── docker-compose.yml  # Docker Compose configuration (optional)
├── docker-compose.dev.yml # Docker Compose override for development
├── Dockerfile           # Dockerfile for backend
├── Dockerfile.frontend   # Dockerfile for frontend
└── README.md           # Project documentation
Environment Management

Here's how to handle different environments (development, integration, test, production) for both the frontend and backend:

1. Environment Variables

Backend (.env.example, located in backend/)

Create an .env.example file in your backend/ directory. This file serves as a template for your environment variables.
Developers will copy .env.example to .env (which should be added to .gitignore) and fill in their local development settings.
For other environments (integration, test, production), you'll create separate .env files or, preferably, set environment variables directly in your deployment environment (e.g., using your cloud provider's settings).
# .env.example (Backend)
DATABASE_URL=postgresql://user:password@localhost:5432/mydatabase
SECRET_KEY=your_secret_key_here
DEBUG=True # Or False
API_VERSION_STRING=/api/v1
# ... other backend environment variables
Load in backend/app/core/config.py:
Python
# backend/app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    debug: bool = False  # Default to False
    api_version_string: str = "/api/v1"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
 Frontend (.env.development, .env.integration, .env.test, .env.production)

Create separate .env files in your frontend/ directory for each environment.
Vue CLI will automatically load these files based on the mode you're running in (e.g., npm run serve loads .env.development, npm run build loads .env.production).
# .env.development (Frontend)
VUE_APP_API_BASE_URL=http://localhost:8000/api/v1
# ... other development-specific variables

# .env.production (Frontend)
VUE_APP_API_BASE_URL=https://your-production-api.com/api/v1
# ... other production-specific variables
Access in Vue Components:
Code snippet
<template>
  <div>
    <p>API Base URL: {{ apiBaseUrl }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      apiBaseUrl: process.env.VUE_APP_API_BASE_URL,
    };
  },
};
</script>
 2. Configuration Files

Backend (backend/app/core/config.py)

As shown above, the config.py file in the backend loads environment variables and sets default values.
You can use the Settings class to access configuration variables throughout your backend code.
Frontend (vue.config.js)

Use vue.config.js for environment-specific configurations that are not sensitive (e.g., public path, output directory).
You can use the process.env.NODE_ENV variable in vue.config.js to conditionally apply settings based on the environment.
3. Build and Deployment

Development:

Backend: Use uvicorn with the --reload flag for automatic reloading:
Bash
cd backend
uvicorn app.main:app --reload --port 8000
Frontend: Use the Vue CLI development server:
Bash
cd frontend
npm run serve
 Other Environments (Integration, Test, Production):

CI/CD: Use a CI/CD pipeline (e.g., GitHub Actions, GitLab CI, Jenkins) to automate building, testing, and deploying your application for different environments.
Docker: Containerize your backend and frontend using Docker. Use Docker Compose for local development and potentially for managing multiple environments (e.g., a docker-compose.prod.yml for production).
Cloud Deployment: Deploy your Docker containers to a cloud provider (e.g., AWS, Google Cloud, Azure) using services like:
AWS: ECS, EKS, Elastic Beanstalk
Google Cloud: Cloud Run, GKE
Azure: Azure Container Instances, AKS, App Service
4. VS Code Configuration

Launch Configurations (.vscode/launch.json)

Create debug configurations for your backend and frontend to easily start and debug them from VS Code.
You can specify environment variables in the launch.json file to override the ones loaded from .env files for debugging purposes.
JSON
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "app.main:app",
        "--reload",
        "--port",
        "8000"
      ],
      "cwd": "${workspaceFolder}/backend",
      "env": {
        "DATABASE_URL": "postgresql://user:password@localhost:5432/mydatabase_dev"
      },
      "justMyCode": true
    },
    {
      "name": "Vue.js: Serve",
      "type": "chrome",
      "request": "launch",
      "url": "http://localhost:8080",
      "webRoot": "${workspaceFolder}/frontend/src",
      "breakOnLoad": true,
      "sourceMapPathOverrides": {
        "webpack:///./src/*": "${webRoot}/*"
      },
      "runtimeArgs": [
        "--auto-open-devtools-for-tabs"
      ],
      "server": {
        "command": "npm run serve",
        "cwd": "${workspaceFolder}/frontend",
        "port": 8080
      }
    }
  ]
}
 Extensions:

Install relevant extensions in VS Code:
Python: For Python development.
Vetur: For Vue.js development.
Docker: For working with Docker.
REST Client: For testing your API endpoints.
Example Workflow (with Docker Compose for Development)

Create docker-compose.yml and docker-compose.dev.yml:

YAML
# docker-compose.yml
version: '3.8'
services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/mydatabase
    depends_on:
      - db
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.frontend
    ports:
      - "8080:8080"
    volumes:
      - ./frontend:/app
    environment:
      - VUE_APP_API_BASE_URL=http://backend:8000/api/v1
    depends_on:
      - backend
  db:
    image: postgres:14
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=mydatabase
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
YAML
# docker-compose.dev.yml
version: '3.8'
services:
  backend:
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
  frontend:
    command: npm run serve -- --port 8080 --host 0.0.0.0
 Create Dockerfile and Dockerfile.frontend:

Dockerfile
# backend/Dockerfile
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
Dockerfile
# frontend/Dockerfile.frontend
FROM node:16

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

CMD ["npm", "run", "serve"]
 Start Development Environment:

Bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build
 This structure and the environment management techniques provide a solid foundation for building and maintaining your web application across different environments. Remember to adjust the configurations and deployment strategies based on your specific needs and the requirements of your project.