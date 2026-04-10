from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.db.models import User
from fastapi import Depends


def get_current_user(db: Session = Depends(get_db)) -> User:
    email = "test@example.com"
    user = db.query(User).filter(User.email == email).first()

    if not user:
        user = User(email=email, auth_provider="fitbit")
        db.add(user)
        db.commit()
        db.refresh(user)

    return user