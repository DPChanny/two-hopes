from sqlalchemy.orm import Session
from sqlalchemy import text


def add_group_service(db: Session) -> str:
    result = db.execute(text("SELECT 1"))
    db.close()
    return result.scalar()
