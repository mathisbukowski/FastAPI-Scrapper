from fastapi import FastAPI

app = FastAPI(title="FastAPI Scrapper", version="1.0.0")


@app.get("/")
async def root():
    """Root endpoint returning a welcome message."""
    return {"message": "Welcome to FastAPI Scrapper"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
