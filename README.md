# Multi-Tenant Management System
## Fullstack Project: FastAPI + React + Postgres

**Description:**  
A full-stack application using FastAPI (backend), React (frontend), PostgreSQL database, and Docker containerization. The project demonstrates multi-tenant architecture where each tenant’s data is isolated. Includes Alembic migrations, JWT authentication, and basic unit tests.
---

## Table of Contents

1. [Prerequisites](#1--prerequisites)  
2. [Setup Instructions](#2--setup-instructions)  
   - Clone Repository  
   - Environment Configuration  
   - Build and Start Services  
   - Run Alembic Migrations  
   - Access Applications  
3. [Architecture & Design Decisions](#3--architecture--design-decisions)  
4. [API Documentation](#4--api-documentation)  
5. [Assumptions](#5--assumptions)  

---

## 1- Prerequisites

Before starting, ensure you have the following installed:

- Docker & Docker Compose  
- Git  
- Node.js & npm (optional if using Docker for frontend)  

---

## 2- Setup Instructions

###  Clone Repository

```bash
git clone https://github.com/berlnty-kerlos/multi-tenant-management-system.git
cd multi-tenant-management-system
```

### Environment Configuration

	Create environment files:

	cp backend/.env.example backend/.env
	cp backend/.env.test.example backend/.env.test
	
### Build and Start Services

	docker-compose up --build

### Run Alembic Migrations (Backend)

	docker exec -it <backend_container_name> bash
	alembic upgrade head
	
	#Ensure the database is ready before running the backend.
### Access Applications

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- FastAPI auto docs: http://localhost:8000/docs or http://localhost:8000/redoc
---
	
## 3- Architecture & Design Decisions

###  Backend

- FastAPI with async endpoints
- Pydantic models for request/response validation
- PostgreSQL with Alembic migrations
- JWT authentication (access + refresh tokens)
- Multi-tenant support via tenant IDs

###  Frontend

- React functional components and hooks
- React Router for navigation
- Context API for global state

###  Docker

- Separate containers for backend, frontend, and database
- Docker Compose manages networking and volumes

###  Design Choices

- Multi-tenant architecture for scalability
- Async backend for performance
- Environment variables managed via `.env` for security
- Clear separation of frontend/backend for maintainability
---

## 4- API Documentation

**FastAPI auto docs:** [http://localhost:8000/docs](http://localhost:8000/docs) or [http://localhost:8000/redoc](http://localhost:8000/redoc)

###  Auth

| Method | Endpoint        | Description        |
|--------|----------------|------------------|
| POST   | /auth/register | Register          |
| POST   | /auth/login    | Login             |
| POST   | /auth/refresh  | Refresh token     |

###  Tenants

| Method | Endpoint          | Description   |
|--------|-----------------|---------------|
| POST   | /tenants/create | Create Tenant |

###  Projects

| Method | Endpoint                  | Description     |
|--------|---------------------------|----------------|
| GET    | /projects                 | List Projects  |
| POST   | /projects                 | Create Project |
| GET    | /projects/{project_id}    | Get Project    |
| PUT    | /projects/{project_id}    | Update Project |
| DELETE | /projects/{project_id}    | Delete Project |

###  Tasks

| Method | Endpoint                         | Description   |
|--------|---------------------------------|---------------|
| POST   | /projects/{project_id}/tasks     | Create Task   |
| GET    | /projects/{project_id}/tasks     | List Tasks    |
| PUT    | /tasks/{task_id}                 | Update Task   |
| DELETE | /tasks/{task_id}                 | Delete Task   |

###  Default

| Method | Endpoint | Description |
|--------|---------|-------------|
| GET    | /       | Root        |

---

## 5- Assumptions

- Each tenant has a unique ID  
- Data isolation is via separate schemas or tenant IDs  
- JWT secrets should be replaced for production  
- Database must exist and migrations applied before running backend  
- Frontend assumes backend runs at http://localhost:8000  
---