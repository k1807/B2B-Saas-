"""FastAPI application entry point."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.models import User, Product, Sale  # noqa: F401 - register models for create_all
from app.api import auth, products, sales, predictions


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create all tables on startup (User, Product, Sale)."""
    Base.metadata.create_all(bind=engine)
    yield
    # Cleanup if needed (optional)


app = FastAPI(
    title="Inventory SaaS API",
    description="AI-powered inventory and sales tracking",
    version="1.0.0",
    lifespan=lifespan,
)

# Allow frontend to call API (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(sales.router, prefix="/api")
app.include_router(predictions.router, prefix="/api")


@app.get("/")
def root():
    """Health check."""
    return {"status": "ok", "message": "Inventory SaaS API is running"}
