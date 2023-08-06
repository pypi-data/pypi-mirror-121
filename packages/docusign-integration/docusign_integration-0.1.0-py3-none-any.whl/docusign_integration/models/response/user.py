from pydantic import BaseModel
from typing import List


class AccountInfoResponse(BaseModel):
    account_id: str
    is_default: bool
    account_name: str
    base_uri: str


class UserInfoResponse(BaseModel):
    sub: str
    name: str
    given_name: str
    family_name: str
    created: str
    email: str
    accounts: List[AccountInfoResponse]
