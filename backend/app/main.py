from fastapi import FastAPI

from backend.app.api.analyses import router as analyses_router


def build_app() -> FastAPI:
    app = FastAPI(title="얼굴 성적기 API", version="0.1.0")
    app.include_router(analyses_router)
    return app


app = build_app()
