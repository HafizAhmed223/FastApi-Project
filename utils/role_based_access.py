from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Users
from auth import get_current_user


def has_role(*allowed_roles: str):
    def role_dependency(user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
        if user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return role_dependency
