# Sortstay Booking Platform

This repository contains the initial skeleton for a platform that allows local councils to book hotel rooms for individuals experiencing homelessness. The goal is to partner with hotels so that rooms that would otherwise remain empty after a daily cutoff can be reserved quickly by council workers.

## Plan Overview

1. **Backend**
   - PostgreSQL will serve as the persistent database via SQLAlchemy.
   - Python and Flask provide a lightweight API service.
   - Endpoints allow hotels to publish room availability, list rooms, and create bookings.
   - Uses SQLite via SQLAlchemy for persistent storage.
   - Token authentication persists in the `session` table.

2. **Frontend**
   - React will power the web portal shown to councils and hotels.

3. **Testing**
   - Pytest is used for backend unit tests. A sample test verifies the health endpoint.

## Getting Started

1. Install dependencies (offline):
   ```bash
   pip install Flask pytest --no-index --find-links=/path/to/packages
   ```
# Place downloaded wheel files for Flask and pytest in the directory specified by --find-links.
2. Run the development server (this creates `sortstay.db` in the project directory):
   ```bash
   python backend/app.py
   ```
3. Execute tests:
   ```bash
   pytest
   ```

## API Endpoints

- `POST /register` – create a user account (role=`hotel` or `council`).
- `POST /login` – obtain an auth token to include in the `Authorization` header.
- `POST /availability` – add a room that is available for booking (hotel auth required). Supports optional `price` and `date_available` fields.
- `GET /rooms` – list all available rooms (requires login).
- `POST /book` – book a room by specifying the `room_id` and optional `nights` (council auth required).
- `GET /health` – simple health check endpoint.

See [docs/requirements_and_userstories.md](docs/requirements_and_userstories.md) for initial requirements and user stories.
