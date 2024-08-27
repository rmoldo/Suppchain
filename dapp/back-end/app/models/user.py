from typing import List, Optional, Type
from sqlmodel import Field, SQLModel, Relationship, Column, JSON

from pydantic import BaseModel, create_model
from functools import lru_cache
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from config.utils import Utils

class UserBase(SQLModel):
    name: str
    email: str
    # set exclude to True so it is never returned
    password: str = Field(exclude=True)
    user_type: "Permission.acl_group" = Relationship(back_populates="users")
    permissions: List["Permission.permissions"] = Relationship(back_populates="users")
    acl_group: Optional[int] = Field(default=1, foreign_key="permission.id")


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    key_pairs: bytes = Field(default= None, exclude= False)

    @classmethod
    def sign(self, data, keyPair):
        data_hash = Utils.hash(data)
        sign_cypher = PKCS1_v1_5.new(keyPair)
        signature = sign_cypher.sign(data_hash)
        return signature.hex()

    @classmethod
    def signature_valid(data, signature, public_key_string):
        bytes_signature = bytes.fromhex(signature)
        data_hash = Utils.hash(data)
        public_key = RSA.importKey(public_key_string)
        verify_cypher = PKCS1_v1_5.new(public_key)

        return verify_cypher.verify(data_hash, bytes_signature)

    @classmethod
    def public_key_to_string(self, key_pair_string):
        RSA_key_pair = RSA.importKey(key_pair_string)
        return RSA_key_pair.publickey().exportKey("PEM").decode("utf-8")

    @staticmethod
    def signature_valid(data, signature, public_key_string):
        bytes_signature = bytes.fromhex(signature)
        data_hash = Utils.hash(data)
        public_key = RSA.importKey(public_key_string)
        verify_cypher = PKCS1_v1_5.new(public_key)

        return verify_cypher.verify(data_hash, bytes_signature)





@lru_cache
def partial(baseclass: Type[BaseModel]) -> Type[BaseModel]:
    """Make all fields in supplied Pydantic BaseModel Optional, for use in PATCH calls.

    Iterate over fields of baseclass, descend into sub-classes, convert fields to Optional and return new model.
    Cache newly created model with lru_cache to ensure it's only created once.
    Use with Body to generate the partial model on the fly, in the PATCH path operation function.

    - https://stackoverflow.com/questions/75167317/make-pydantic-basemodel-fields-optional-including-sub-models-for-patch
    - https://stackoverflow.com/questions/67699451/make-every-fields-as-optional-with-pydantic
    - https://github.com/pydantic/pydantic/discussions/3089
    - https://fastapi.tiangolo.com/tutorial/body-updates/#partial-updates-with-patch
    """
    fields = {}
    for name, field in baseclass.__fields__.items():
        type_ = field.type_
        if type_.__base__ is BaseModel:
            fields[name] = (Optional[partial(type_)], {})
        else:
            fields[name] = (Optional[type_], None) if field.required else (type_, field.default)
    # https://docs.pydantic.dev/usage/models/#dynamic-model-creation
    validators = {"__validators__": baseclass.__validators__}
    return create_model(baseclass.__name__ + "Partial", **fields, __validators__=validators)
