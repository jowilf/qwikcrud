from app.models import Base
from app.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

Session = sessionmaker(engine)


async def init_db():
    Base.metadata.create_all(engine)
