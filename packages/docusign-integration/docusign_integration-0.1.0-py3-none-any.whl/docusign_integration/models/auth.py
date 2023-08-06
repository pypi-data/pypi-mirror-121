from pydantic.dataclasses import dataclass
from typing import List, Union, Optional, Callable


@dataclass(frozen=True)
class Scope:
    """https://developers.docusign.com/platform/auth/reference/scopes/"""

    IMPERSONATION = "impersonation"
    EXTENDED = "extended"
    SIGNATURE = "signature"
    OPENID = "openid"
    CLICK_MANAGE = "click.manage"
    CLICK_SEND = "click.send"
    ORGANIZATION_READ = "organization_read"
    GROUP_READ = "group_read"
    PERMISSION_READ = "permission_read"
    USER_READ = "user_read"
    USER_WRITE = "user_write"
    ACCOUNT_READ = "account_read"
    DOMAIN_READ = "domain_read"
    IDENTITY_PROVIDER_READ = "identity_provider_read"
    DATAFEEDS = "datafeeds"
    DTR_ROOMS_READ = "dtr.rooms.read"
    DTR_ROOMS_WRITE = "dtr.rooms.write"
    DTR_DOCUMENTS_READ = "dtr.documents.read"
    DTR_DOCUMENTS_WRITE = "dtr.documents.write"
    DTR_PROFILE_READ = "dtr.profile.read"
    DTR_PROFILE_WRITE = "dtr.profile.write"
    DTR_COMPANY_READ = "dtr.company.read"
    DTR_COMPANY_WRITE = "dtr.company.write"
    ROOM_FORMS = "room_forms"
    NOTARY_WRITE = "notary_write"
    NOTARY_READ = "notary_read"


@dataclass
class AuthParams:
    base_url: str
    refresh_url: str
    client_id: str
    client_secret: str
    scope: List[Union[Scope, str]]
    access_token: str
    refresh_token: str
    token_updater: Optional[Callable[[str], None]] = None
