from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.routers import resume, analysis
from app.database import engine, Base
from app.middleware.rate_limit import limiter
from app.core.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting JD Analyzer API")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
    logger.info("Shutdown complete")


app = FastAPI(title="JD Analyzer API", version="0.1.0", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume.router)
app.include_router(analysis.router)


@app.get("/health")
async def health():
    import os
    import redis.asyncio as aioredis
    from sqlalchemy import text

    checks: dict[str, str] = {}
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        checks["db"] = "ok"
    except Exception as e:
        checks["db"] = f"error: {e}"

    try:
        r = aioredis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
        await r.ping()
        await r.aclose()
        checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = f"error: {e}"

    all_ok = all(v == "ok" for v in checks.values())
    return JSONResponse(
        status_code=200 if all_ok else 503,
        content={"status": "ok" if all_ok else "degraded", **checks},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(status_code=500, content={"detail": str(exc)})
