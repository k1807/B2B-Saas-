# Inventory SaaS Backend

Production-ready FastAPI backend for an AI-powered inventory and sales tracking SaaS.

## Features

- **User authentication** – JWT-based login and registration
- **Product management** – Full CRUD for products (name, SKU, quantity, price)
- **Sales tracking** – Record daily sales, auto-update inventory
- **PostgreSQL** – SQLAlchemy ORM with clean models

## Project Structure

```
backend/
├── app/
│   ├── api/          # Route handlers (auth, products, sales)
│   ├── core/         # Security (JWT, password hashing), dependencies
│   ├── crud/         # Database operations
│   ├── models/       # SQLAlchemy models (User, Product, Sale)
│   ├── schemas/      # Pydantic request/response schemas
│   ├── config.py     # Settings from .env
│   ├── database.py   # DB engine and session
│   └── main.py       # FastAPI app
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

### 1. Create virtual environment

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Database

**PostgreSQL (production):** Create a database and set `DATABASE_URL` in `.env`:

```sql
CREATE DATABASE inventory_saas;
```

**SQLite (local dev):** No setup needed. In `.env`:

```env
DATABASE_URL=sqlite:///./inventory.db
```

### 4. Environment variables

Copy `.env.example` to `.env` and update:

```bash
copy .env.example .env   # Windows
# cp .env.example .env   # macOS/Linux
```

Edit `.env` with your database URL and a strong `SECRET_KEY`:

```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/inventory_saas
SECRET_KEY=your-secret-key  # Use: openssl rand -hex 32
```

### 5. Run the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: http://localhost:8000/docs

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/auth/register` | No | Register new user |
| POST | `/api/auth/login` | No | Login, get JWT token |
| GET | `/api/auth/me` | Yes | Get current user |
| GET | `/api/products` | Yes | List products |
| POST | `/api/products` | Yes | Create product |
| GET | `/api/products/{id}` | Yes | Get product |
| PATCH | `/api/products/{id}` | Yes | Update product |
| DELETE | `/api/products/{id}` | Yes | Delete product |
| POST | `/api/sales` | Yes | Record a sale |
| GET | `/api/sales` | Yes | List sales (filter by product, dates) |
| GET | `/api/sales/daily/{date}` | Yes | Daily sales summary |

## Usage Example

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"secret123","full_name":"John Doe"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"secret123"}'
# Returns: {"access_token":"eyJ...","token_type":"bearer"}

# Create product (use token from login)
curl -X POST http://localhost:8000/api/products \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Widget","sku":"WDG-001","quantity":100,"price":9.99}'

# Record sale
curl -X POST http://localhost:8000/api/sales \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id":1,"quantity_sold":5,"sale_date":"2025-03-23"}'
```

## License

MIT
