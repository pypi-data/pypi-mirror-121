import os
from typing import Optional, Tuple, Any, no_type_check
from importlib import import_module
from fastapi import Request, HTTPException, Security
from fastapi.param_functions import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.openapi.models import HTTPBearer as HTTPBearerModel
from fastapi.security.oauth2 import get_authorization_scheme_param
from integration_tools.api import BaseCredentialMixin
from integration_tools.exceptions import PermissionDenied

settings = import_module(os.environ.get('FASTAPI_SETTINGS', 'app.config.settings'))
credential_module_path, credential_model_name = settings.CREDENTIAL_MODEL.rsplit('.', 1)
module = import_module(credential_module_path)
CREDENTIAL_MODEL = getattr(module, credential_model_name)

__all__ = ('get_smart_auth', 'get_credential')


class SmartHTTPToken(HTTPBearer):
    def __init__(
        self,
        *,
        bearerFormat: Optional[str] = None,
        scheme_name: Optional[str] = None,
        auto_error: bool = True,
    ):
        self.model = HTTPBearerModel(bearerFormat=bearerFormat)
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        authorization: str = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            if self.auto_error:
                raise HTTPException(
                    status_code=403, detail="Permission Denied",
                )
            else:
                return None
        if scheme.lower() not in ("token", "bearer"):
            if self.auto_error:
                raise HTTPException(
                    status_code=403, detail="Permission Denied",
                )
            else:
                return None
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)


sec = SmartHTTPToken(bearerFormat='Token', scheme_name='Token')


@no_type_check
async def check_auth_params(
    platform_id: Optional[str] = None,
    auth: HTTPAuthorizationCredentials = Security(sec),
) -> Tuple:
    if not platform_id or platform_id not in ('dev', 'prod'):
        raise HTTPException(
            status_code=403, detail="Permission Denied, invalid platform_id",
        )
    return auth.credentials, platform_id


class Auth(BaseCredentialMixin):
    pass


@no_type_check
async def get_smart_auth(auth_params: tuple = Depends(check_auth_params)):
    auth = Auth()
    _, platform_id = auth_params
    try:
        auth_params = await auth.get_user_info_async(*auth_params)
    except PermissionDenied as e:
        raise HTTPException(status_code=e.status, detail=e.error_detail)
    return {
        'smart_user_name': auth_params['username'],
        'smart_user_id': auth_params['id'],
        'platform_id': platform_id,
    }


async def get_credential(credential_id: str, _=Depends(get_smart_auth)) -> Any:  # type: ignore
    credential = None  # type: ignore
    raise NotImplementedError('implement get credential')
    # if not credential:
    #     HTTPException(
    #         status_code=403, detail="Invalid credential",
    #     )
    # return credential
