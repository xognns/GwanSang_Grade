from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from backend.app.api.analyses import router as analyses_router


def build_app() -> FastAPI:
    app = FastAPI(title="얼굴 성적기 API", version="0.1.0")
    allowed_origins = [origin.strip() for origin in os.getenv("CORS_ALLOW_ORIGINS", "").split(",") if origin.strip()]
    allow_origin_regex = os.getenv("CORS_ALLOW_ORIGIN_REGEX", r"^https://.*\\.vercel\\.app$")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_origin_regex=allow_origin_regex,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=False,
    )
    app.include_router(analyses_router)
    return app


app = build_app()
