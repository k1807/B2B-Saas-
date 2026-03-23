# Inventory SaaS Frontend

React + Vite + Tailwind frontend for the Inventory SaaS API.

## Setup

1. Install Node.js (https://nodejs.org) if you don't have it.

2. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

3. Start the backend (from project root):
   ```bash
   cd backend
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

4. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

5. Open http://localhost:5173

## Features

- **Login / Register** – JWT authentication
- **Dashboard** – Product count, recent sales summary
- **Products** – List, add, edit, delete products
- **Sales** – Record sales, view sales list

API requests are proxied to `http://localhost:8000` via Vite proxy.
