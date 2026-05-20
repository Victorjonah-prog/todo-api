from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1 import router as api_v1_router

app = FastAPI(
    title="Todo API",
    description="Production-grade MVP Todo API with authenticated and guest todo systems.",
    version="1.0.0",
)

app.include_router(api_v1_router)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred"},
    )


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
