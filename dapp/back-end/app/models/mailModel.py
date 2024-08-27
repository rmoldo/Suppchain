from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlmodel import Field, SQLModel


class MailConfiguration(SQLModel, table= True):
    __tablename__ = "mailconfiguration"
    id: int = Field(Integer, primary_key=True, index=True)
    mail_config_owner: str= Field(String)
    owner_email: str= Field(String)
    MAIL_USERNAME: str= Field(String)
    MAIL_PASSWORD: str= Field(String)
    MAIL_FROM: str= Field(String)
    MAIL_PORT: str= Field(String)
    MAIL_SERVER: str= Field(String)
    MAIL_FROM_NAME: str= Field(String)
    MAIL_STARTTLS: str= Field(String)
    MAIL_SSL_TLS: str= Field(String)
    USE_CREDENTIALS: bool = Field(default=False)
    VALIDATE_CERTS: bool = Field(default=False)

