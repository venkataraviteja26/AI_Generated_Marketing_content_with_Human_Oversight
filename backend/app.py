from fastapi import FastAPI
from config import config
from api import auth, content, fetch_records, reviews
from db import connection
from utils.logging import setup_logging

# Set up logging
setup_logging(config["development"].LOG_LEVEL)

# Initialize the database connection (make sure this function exists in connection.py)
connection.init_db()

# Create FastAPI app
app = FastAPI(
    title="Marketing Content Generation API",
    description="API for generating and managing AI-driven marketing content.",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Marketing Content Generation API!"}

# Include API routers for different modules
# app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(content.router, prefix="/api/content", tags=["content"])
app.include_router(fetch_records.router, prefix="/api/prompts", tags=["fetch_records"])
app.include_router(reviews.router, prefix="/api/reviews", tags=["reviews"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.PORT)
