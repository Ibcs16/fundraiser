from .database import SessionLocal

# Db dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

