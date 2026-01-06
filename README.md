### **Backend Repository README**

```md
# Resource Sharing Platform – Backend

The Django backend for a resource-sharing platform that handles user management and educational resource management for teachers and learners.

## Overview

This backend provides:
- User authentication and management (login, logout, registration)
- CRUD operations for resources
- API endpoints for the frontend
- Storage of resources in PostgreSQL (Neon)

## Key Features

- User authentication and session management
- Resource management (add, edit, delete, retrieve)
- Support for open educational resources
- Search functionality via backend queries

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL (Neon)

## Project Status

- 🟡 Functional prototype

## Running Locally

### Prerequisites

- Python 3.x
- pip

### Setup

```bash
git clone <backend-repo-url>
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Runs on http://localhost:8000.

Notes

Supports frontend API requests

Environment variables (if any) should be defined in a .env file

What This Repo Demonstrates

Backend API design for educational platforms
User authentication and session management
Resource management and search functionality