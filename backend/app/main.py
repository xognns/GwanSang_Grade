from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.analyses import router as analyses_router


def build_app() -> FastAPI:
    app = FastAPI(title="얼굴 성적기 API", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r"^https://.*\\.vercel\\.app$",
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=False,
    )
    app.include_router(analyses_router)
    return app


app = build_app()
