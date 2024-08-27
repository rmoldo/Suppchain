import stripe
from sqlalchemy.orm import Session
from models.mailModel import MailConfiguration as MailModel
from schemas.mailConfigSchema import MailSchema
from config.hashing import Hashing

# from uuid import uuid4


stripe.api_key = "test"


class MailController:
    def getAll(db: Session):
        mails_configs = db.query(MailModel).all()
        # for mail_config in mails_configs:
        #     mail_config.MAIL_PASSWORD = None
        return mails_configs


    def getMailByID(owner_email: str, db: Session):
        return db.query(MailModel).filter(MailModel.owner_email == owner_email).first()

    def createEmailConfiguration(request: MailSchema, db: Session):
        db_email_configuration = MailModel(
            mail_config_owner = request.mail_config_owner,
            owner_email = request.owner_email,
            MAIL_USERNAME = request.MAIL_USERNAME,
            MAIL_PASSWORD = request.MAIL_PASSWORD,
            MAIL_FROM = request.MAIL_FROM,
            MAIL_PORT = request.MAIL_PORT,
            MAIL_SERVER = request.MAIL_SERVER,
            MAIL_FROM_NAME = request.MAIL_FROM_NAME,
            MAIL_STARTTLS = request.MAIL_STARTTLS,
            MAIL_SSL_TLS = request.MAIL_SSL_TLS,
            USE_CREDENTIALS = request.USE_CREDENTIALS,
            VALIDATE_CERTS = request.VALIDATE_CERTS,
        )

        db.add(db_email_configuration)
        db.commit()

        db.refresh(db_email_configuration)
        db_email_configuration.MAIL_PASSWORD = None

        return db_email_configuration
