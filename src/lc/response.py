from abc import ABC
from dataclasses import dataclass


@dataclass
class BaseResponse(ABC):
    success:bool
    status:int
    def to_dict(self):
        print(self)
        data = vars(self)
        
        return { k:v for k, v in data.items() }

@dataclass
class SuccessResponse(BaseResponse):
    success:bool=True
    status:int=200
    data:any=None



@dataclass
class FailResponse(BaseResponse):
    success:bool=False
    status:int=500
    error:str=""