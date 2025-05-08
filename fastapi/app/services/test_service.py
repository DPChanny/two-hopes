from sqlalchemy.orm import Session
from sqlalchemy import text


def get_test_service(db: Session) -> str:
    result = db.execute(text("SELECT 1"))
    db.close()
    return result.scalar()
