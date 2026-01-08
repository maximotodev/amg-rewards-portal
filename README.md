# AMG Rewards Portal - Technical Demo

A high-performance, full-stack prototype for a consumer-facing receipt promotion and loyalty platform, mirroring core features of AMG products like **ORA** and **Shop. Snap. Earn.℠**.

## 🚀 Tech Stack

- **Frontend:** Angular 21 (Zoneless, Signals, Reactive Forms)
- **Backend:** Python 3.12+ / FastAPI (Asynchronous, Pydantic v2)
- **Database:** MySQL 8.4 (Relational, ACID compliant)
- **Infrastructure:** Docker Desktop (Local Parity)
- **Migrations:** Alembic (Schema-as-Code)

## 🏗️ Architectural Decisions

### 1. Zoneless Angular + Signals

I opted for the **Experimental Zoneless** configuration provided in Angular 21. By leveraging **Signals** for state management, the application bypasses the overhead of `Zone.js`, leading to faster change detection and a smaller bundle footprint. This is ideal for high-traffic consumer environments where performance is critical.

### 2. Modular Monolith Backend

The FastAPI backend follows a **Service Layer pattern**. By decoupling API routing from business logic (point calculation), the system remains highly testable and allows for easy evolution into microservices if domain complexity increases.

### 3. Schema Management with Alembic

To ensure deployment reliability, database changes are handled via **Alembic migrations**. This ensures local, staging, and production environments remain synchronized without manual SQL execution.

## 🛠️ How to Run

### Prerequisites

- Docker Desktop
- Node.js 20+ & Angular CLI 21+
- Python 3.12+

### 1. Infrastructure

```bash
docker-compose up -d
```

### 2. Backend

````cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=$PYTHONPATH:.
alembic upgrade head
uvicorn app.main:app --reload```


### 3. Frontend

```cd frontend
npm install
npm start
````

🔒 Security Measures

CORS Allow-listing: Explicitly restricted to the frontend origin.
Input Validation: Strict Pydantic schemas on the backend and Reactive Form validators on the frontend.
Statelessness: The API is designed to be horizontally scalable and stateless.
