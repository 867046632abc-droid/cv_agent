import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/jd_analyzer")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB
