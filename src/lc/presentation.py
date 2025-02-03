from django.http import HttpResponse, JsonResponse
from .response import SuccessResponse, FailResponse
class Presentation:

    @staticmethod
    def json_response(response: SuccessResponse | FailResponse) -> HttpResponse:

        return JsonResponse(response.to_dict())
