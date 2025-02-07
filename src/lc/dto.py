from abc import ABC, abstractmethod
from dataclasses import dataclass
from django.http import HttpRequest
from enum import Enum

class DTOVerificationStatus(Enum):
    PASS=0
    FAIL=1

@dataclass(frozen=True)
class DTOVerificationResult:
    status: DTOVerificationStatus
    message: str=""

class DTO(ABC):
    def __init__(self, request:HttpRequest):

        auth_header = request.headers.get("Authorization")
        if auth_header:
            self.jwt_token = auth_header.split("Bearer ")[1]

    def to_dict(self):

        data = vars(self)

        return { k:v for k, v in data }

    @abstractmethod
    def verify(self) -> DTOVerificationResult:
        raise NotImplementedError()
    


