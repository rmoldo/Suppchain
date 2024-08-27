from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from config.database import get_db
from schemas.mailConfigSchema import MailSchema
from controllers.mailController import MailController

router = APIRouter(prefix="/mail", tags=["Mail"])


@router.get("/")
def getAll(db: Session = Depends(get_db)):
    return MailController.getAll(db=db)


@router.post("/")
def createEmailOwner(request: MailSchema, db: Session = Depends(get_db)):
    return MailController.createEmailConfiguration(request=request, db=db)


@router.get("/{mailID}")
def orderByUser(owner_email: str, db: Session = Depends(get_db)):
    return MailController.getMailByID(owner_email=owner_email, db=db)
#
#
# @router.get("/orderbyid/{id}")
# def orderById(id: int, db: Session = Depends(get_db)):
#     return OrderController.getOrderById(id=id, db=db)


