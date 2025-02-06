from functools import wraps
from django.http import HttpRequest, JsonResponse
from .response import FailResponse
from .db import REFRESH_TOKEN, TOKEN_MAP
import jwt
from datetime import datetime, timedelta, timezone
# jwt token verification
# this function can be used for all services

ALGORITHM = "HS256"
KEY = "myapp_seCret!"
ISSUER = ""
class Authentication:
    def __init__(self, func, token_type:str="access"):
        self._func = func
        self._token_type = token_type
    @wraps(lambda *args, **kwargs: args[0]._func(*args, **kwargs)) # Important!
    def __call__(self, *args, **kwds):
        
        request = None

        for arg in args:
            if isinstance(arg, HttpRequest):
                request = arg
                break
        
        if not request:
            for kwarg in kwds.values():
                if isinstance(kwarg, HttpRequest):
                    request = kwarg
                    break

        if not request:
            return JsonResponse(FailResponse(error="Request is not found").to_dict())
        
        auth_header = request.headers.get("Authorization")
        jwt_token = auth_header.split("Bearer ")[1]
        
        
        try:
            result = jwt.decode(jwt=jwt_token, key=KEY, algorithms=ALGORITHM)
            
            if result["type"] != self._token_type:
                return JsonResponse(FailResponse(error="Invalid token is used", status=401).to_dict())
            
            if self._token_type == "refresh" and jwt_token not in REFRESH_TOKEN:
                return JsonResponse(FailResponse(error="Invalid refresh token", status=401).to_dict())
            if self._token_type == "access" and jwt_token not in TOKEN_MAP:
                return JsonResponse(FailResponse(error="Invalid access token", status=401).to_dict())

        except jwt.ExpiredSignatureError:
            return JsonResponse(FailResponse(error="Token is expired", status=401).to_dict())
        except jwt.InvalidIssuerError:
            return JsonResponse(FailResponse(error="Invalid Issuer", status=401).to_dict())
            
        except jwt.InvalidAudienceError:
            return JsonResponse(FailResponse(error="Invalid Audience", status=401).to_dict())
        except jwt.InvalidTokenError:
            return JsonResponse(FailResponse(error="Invalid Token", status=401).to_dict())

        
        
        return self._func(*args, **kwds)

def Auth(token_type:str="access"):
    def decorator(func):
        return Authentication(func, token_type=token_type)
    
    return decorator

def encode_jwt(payload):
     
    now = datetime.now(timezone.utc)

    encoded_jwt = jwt.encode({
            "iss": ISSUER,
            'exp': now + timedelta(minutes=10),
            'iat': now,
            'scope': 'access_token',
            **payload
        }, KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def get_jwt_refresh_both(payload):

    encoded_jwt = encode_jwt({
        "type": "access",
        **payload
    })
    refresh_jwt = encode_jwt({
        'type': "refresh",
        'exp': datetime.now(timezone.utc) + timedelta(hours=1),
        **payload
    })

    return {
        "jwt": encoded_jwt,
        "ref": refresh_jwt
    }