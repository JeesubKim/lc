from abc import ABC
from dataclasses import dataclass


@dataclass
class BaseResponse(ABC):
    success:bool

    def to_dict(self):
        print(self)
        data = vars(self)
        
        return { k:v for k, v in data.items() }

@dataclass
class SuccessResponse(BaseResponse):
    success:bool=True
    data:any=None



@dataclass
class FailResponse(BaseResponse):
    success:bool=False
    error:str=""