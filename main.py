from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.settings import settings

app = FastAPI(
    title="Book Store API",
    description="Book Store API",
    default_response_class=ORJSONResponse
)

if __name__ == '__main__':
    from uvicorn import run

    run(
        app=app,
        host=settings.HOST,
        port=settings.PORT,
    )
