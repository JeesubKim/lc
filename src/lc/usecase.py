from .dto import DTO
from lc.dto import DTOVerificationResult, DTOVerificationStatus
from lc.response import SuccessResponse, FailResponse
from lc.external import database
class Usecase:
    def __init__(self, dto:DTO, db_port:database.DBPort):
        self._dto = dto
        self._db_port = db_port

    def exec(self) -> SuccessResponse | FailResponse:

        dto_verification_result:DTOVerificationResult = self._dto.verify()
        if dto_verification_result.status == DTOVerificationStatus.PASS:
            # return SuccessResponse(data=self._run())
            return self._run()
        
        elif dto_verification_result.status == DTOVerificationStatus.FAIL:
            return FailResponse(error=dto_verification_result.message)
        
    @staticmethod
    def _run(self) -> any:
        raise NotImplementedError()