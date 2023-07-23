from fastapi import Depends, FastAPI
import uvicorn

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import settings
from model import DogModel

# engine = create_engine('sqlite:///:memory:', echo=True)
engine = engine = create_engine(
    '{engine}://{username}:{password}@{host}/{db_name}'.format(
        **settings.SQLSERVER
    ),
    echo=settings.SQLALCHEMY['debug']
)
session_local = sessionmaker(
    bind=engine,
    autoflush=settings.SQLALCHEMY['autoflush'],
    autocommit=settings.SQLALCHEMY['autocommit']
)
app = FastAPI()

# Dependency
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

@app.get('/dog')
def get_all(db: Session = Depends(get_db)):
    dogs = db.query(DogModel).all()
    results = [
        {
            "id": dog.id,
            "breed": dog.breed,
            "color": dog.color
        } for dog in dogs]

    return {"results": results}

if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0')
