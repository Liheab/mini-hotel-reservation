
# Mini Hotel Reservation System
A lightweight hotel reservation system built with Django REST Framework (backend) and Vue 3 (frontend).
A simple hotel reservation system with **room management**, **booking management**, and **staff dashboard**
using **Vue (Frontend)** and **Django DRF (Backend)**.

## Features

- **Frontend (Vue.js)**
  - Search and filter rooms
  - View room details
  - Book rooms with guest details
  - View and cancel bookings
  - Staff dashboard for rooms and bookings
- **Backend (Django + DRF)**
  - CRUD for rooms
  - CRUD and status updates for bookings
  - REST API endpoints for frontend consumption
- **Booking Features**
  - Confirm bookings
  - Cancel bookings (updates status instead of delete)
  - Payment simulation
- **Filtering**
  - Filter bookings by **check-in/check-out date** and **status**
  - Filter rooms by **number, type, price, capacity**

---

## Architecture

```text
                  ┌─────────────┐
                  │   Browser   │
                  │             |
                  └─────┬───────┘
                        │ Browser
                        ▼
                  ┌─────────────┐
                  │ Vue Router  │
                  └─────┬───────┘
                        │ API Calls (Axios)
                        ▼
                  ┌─────────────┐
                  │ Django DRF  │
                  │  REST API   │
                  └─────┬───────┘
                        │ ORM
                        ▼
                  ┌─────────────┐
                  │   Database  │
                  │ (PostgreSQL)│
                  └─────────────┘
```

Frontend: Vue with Vue Router, Axios for API calls, Tailwind CSS for UI.

Backend: Django + Django REST Framework, PostgreSQL database.

Data Flow: Browser → Vue Router → Axios → DRF API → Database → DRF → Vue → Browser.

---

| Decision                           | Reason / Trade-off                                                                                                                |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **Vue.js**                         | Lightweight SPA, easier to integrate with DRF, better for reactive UIs.                                                           |
| **Django REST Framework**          | Quick API development; trade-off is slightly heavier backend than Flask or FastAPI.                                               |
| **Booking Cancellation via PATCH** | Avoids deletion of historical records, keeps audit trail. Trade-off: database grows over time.                                    |
| **Tailwind CSS**                   | Fast UI styling, but custom complex designs may require overrides.                                                                |
 -------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Setup Guide

1. Clone project from repository https://github.com/Liheab/mini-hotel-reservation.git
2. run docker command below 1 of them:
   - docker-compose up
   - docker-compose up -d <!-- -(detached mode)   -->
3. after run go to broswer http://localhost:5173
4. stop docker run command:

   - docker-compose down -v <!--remove everything include volumes -->

5. addtional test on backend to run test makesure docker in up running (backend name of service):

   - docker compose exec backend python manage.py test <!--run test Backend -->
