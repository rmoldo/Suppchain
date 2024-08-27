from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import controllers.authController as authController
from config.database import get_db

router = APIRouter(tags=["Authentication"])


@router.post("/login")
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
   return await authController.login(request=request, db=db)
