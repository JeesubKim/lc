import json
from django.http import HttpRequest
from lc.dto import DTO
from dataclasses import dataclass
from lc.dto import DTOVerificationResult, DTOVerificationStatus


class LoginDTO(DTO):

    def __init__(self, request:HttpRequest):
        body = json.loads(request.body)
        self.username = body.get("username")
        self.password = body.get("password")

    def verify(self) -> DTOVerificationResult:

        if self.username and self.username.isnumeric():
            return DTOVerificationResult(status=DTOVerificationStatus.FAIL, message="Username is numeric")
        
        return DTOVerificationResult(DTOVerificationStatus.PASS)
        



class SignupDTO(DTO):

    def __init__(self, request:HttpRequest):
        body = json.loads(request.body)
        
        self.username = body.get("username")
        self.password = body.get("password")
        self.email = body.get("email")

    def verify(self) -> DTOVerificationResult:

        if self.username and self.username.isnumeric():
            return DTOVerificationResult(status=DTOVerificationStatus.FAIL, message="Username is numeric")
        
        if self.email and "@" not in self.email:
            return DTOVerificationResult(status=DTOVerificationStatus.FAIL, message="Invalid email format")
        

        return DTOVerificationResult(DTOVerificationStatus.PASS)


class TokenRefreshDTO(DTO):
    def __init__(self, request:HttpRequest):
        body = json.loads(request.body)
        
        self.ref_token = body.get("ref")
    
    def verify(self) -> DTOVerificationResult:

        if not self.ref_token:
            return DTOVerificationResult(status=DTOVerificationStatus.FAIL, message="Token is empty")
        
        return DTOVerificationResult(DTOVerificationStatus.PASS)


@dataclass(frozen=True)
class JwtDTO(DTO):
    token: str
    refresh_token:str

    def verify(self):...
