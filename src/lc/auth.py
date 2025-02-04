from functools import wraps
from django.http import HttpRequest, JsonResponse
from .response import FailResponse
import jwt
from datetime import datetime, timedelta, timezone
# jwt token verification
# this function can be used for all services

ALGORITHM = "HS256"
KEY = "myapp_seCret!"
ISSUER = ""
class Authentication:
    def __init__(self, func):
        self._func = func
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
            print(result)
        except jwt.ExpiredSignatureError:
            return JsonResponse(FailResponse(error="Token is expired").to_dict())
        except jwt.InvalidIssuerError:
            return JsonResponse(FailResponse(error="Invalid Issuer").to_dict())
            
        except jwt.InvalidAudienceError:
            return JsonResponse(FailResponse(error="Invalid Audience").to_dict())
        except jwt.InvalidTokenError:
            return JsonResponse(FailResponse(error="Invalid Token").to_dict())

        
        
        return self._func(*args, **kwds)

def Auth(func):
    return Authentication(func)
    

def encode_jwt(payload):
     
    now = datetime.now(timezone.utc)

    encoded_jwt = jwt.encode({
            "iss": ISSUER,
            'exp': now + timedelta(hours=2),
            'iat': now,
            'scope': 'access_token',
            **payload
        }, KEY, algorithm=ALGORITHM)
    
    return encoded_jwt