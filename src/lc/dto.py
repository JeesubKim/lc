from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

class DTOVerificationStatus(Enum):
    PASS=0
    FAIL=1

@dataclass(frozen=True)
class DTOVerificationResult:
    status: DTOVerificationStatus
    message: str=""

class DTO(ABC):

    def to_dict(self):

        data = vars(self)

        return { k:v for k, v in data }

    @abstractmethod
    def verify(self) -> DTOVerificationResult:
        raise NotImplementedError()
    


