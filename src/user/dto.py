from django.http import HttpRequest
from lc.dto import DTO
from dataclasses import dataclass
from lc.dto import DTOVerificationResult, DTOVerificationStatus

@dataclass
class LoginDTO(DTO):

    username:str
    password:str
    
    def __init__(self, request:HttpRequest):
        self.username = request.POST.get("username")
        self.password = request.POST.get("password")

    def verify(self) -> DTOVerificationResult:

        if self.username and self.username.isnumeric():
            return DTOVerificationResult(status=DTOVerificationStatus.FAIL, message="Username is numeric")
        
        return DTOVerificationResult(DTOVerificationStatus.PASS)
        


@dataclass
class JoinDTO(DTO):
    username:str
    password:str
    email:str
    def __init__(self, request:HttpRequest):
        self.username = request.POST.get("username")
        self.password = request.POST.get("password")
        self.email = request.POST.get("email")

    def verify(self) -> DTOVerificationResult:

        if self.username and self.username.isnumeric():
            return DTOVerificationResult(status=DTOVerificationStatus.FAIL, message="Username is numeric")
        
        if self.email and "@" not in self.email:
            return DTOVerificationResult(status=DTOVerificationStatus.FAIL, message="Invalid email format")
        

        return DTOVerificationResult(DTOVerificationStatus.PASS)

@dataclass(frozen=True)
class JwtDTO(DTO):
    token: str
    refresh_token:str

    def verify(self):...
