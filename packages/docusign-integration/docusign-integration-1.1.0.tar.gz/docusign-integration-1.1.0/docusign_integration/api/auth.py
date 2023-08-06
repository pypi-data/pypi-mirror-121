from typing import Any, Dict, Type

from pydantic.decorator import validate_arguments
from docusign_integration.models.auth import AuthParams
from requests_oauthlib.oauth2_session import OAuth2Session
from urllib.parse import urljoin


class BaseApi(OAuth2Session):
    _base_url: str
    api_version: str

    @validate_arguments
    def __init__(self, auth_params: AuthParams, api_version: str = "v2.1") -> None:
        if auth_params.base_url[-1] != "/":
            auth_params.base_url += "/"
        self._base_url = auth_params.base_url
        self._api_version = api_version

        OAuth2Session.__init__(
            self,
            client_id=auth_params.client_id,
            token={
                "access_token": auth_params.access_token,
                "refresh_token": auth_params.refresh_token,
                "token_type": "Bearer",
                "expires_in": 3600,
            },
            scope=auth_params.scope,
            auto_refresh_url=auth_params.refresh_url,
            auto_refresh_kwargs={
                "client_id": auth_params.client_id,
                "client_secret": auth_params.client_secret,
            },
            token_updater=auth_params.token_updater,
        )

        self.refresh_token(self.auto_refresh_url)

    @classmethod
    def from_session(
        cls: Type["BaseApi"], session: Type["BaseApi"], **kwargs
    ) -> Type["BaseApi"]:
        """Create a new session from another one.

        Returns:
            New session with this type.
        """

        if not isinstance(session, BaseApi):
            raise TypeError("Session must be a BaseApi")

        auth_params = dict(
            base_url=session.base_url,
            refresh_url=session.auto_refresh_url,
            client_id=session.client_id,
            client_secret=session.auto_refresh_kwargs.get("client_secret"),
            scope=session.scope,
            access_token=session.token.get("access_token"),
            refresh_token=session.token.get("refresh_token"),
        )
        auth_params.update(**kwargs)

        data = AuthParams(**auth_params)
        return cls(data)

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def api_version(self) -> str:
        return self._api_version

    def get_user_info(self) -> Dict[str, Any]:
        """Get user logged info.

        Returns:
            UserInfoResponse
        """

        response = self.get(url=urljoin(self.base_url, "oauth/userinfo"))
        response.raise_for_status()
        return response.json()
