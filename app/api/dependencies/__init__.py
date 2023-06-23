from fastapi import FastAPI

from sqlalchemy.orm import sessionmaker

from app.api.dependencies.database import DbProvider, dao_provider


def setup(app: FastAPI, pool: sessionmaker) -> None:
    db_provider = DbProvider(pool=pool)
    app.dependency_overrides[dao_provider] = db_provider
