from app.db.session import engine
from app.db.base import Base

# import all models here so they are registered with Base
from app.models import user  # noqa: F401


def init_db():
    Base.metadata.create_all(bind=engine)
