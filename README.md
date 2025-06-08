# Sortstay Booking Platform

This repository contains the initial skeleton for a platform that allows local councils to book hotel rooms for individuals experiencing homelessness. The goal is to partner with hotels so that rooms that would otherwise remain empty after a daily cutoff can be reserved quickly by council workers.

## Plan Overview

1. **Backend**
   - Python and Flask provide a lightweight API service.
   - Endpoints allow hotels to publish room availability, list rooms, and create bookings.
   - Initial implementation stores data in memory for demonstration purposes.

2. **Frontend**
   - To be implemented using a modern JavaScript framework (React or Vue) for a responsive portal.

3. **Testing**
   - Pytest is used for backend unit tests. A sample test verifies the health endpoint.

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the development server:
   ```bash
   python backend/app.py
   ```
3. Execute tests:
   ```bash
   pytest
   ```

## API Endpoints

- `POST /availability` – add a room that is available for booking.
- `GET /rooms` – list all available rooms.
- `POST /book` – book a room by specifying the `room_id`.
- `GET /health` – simple health check endpoint.
