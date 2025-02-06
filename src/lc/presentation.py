from django.http import HttpResponse, JsonResponse
from .response import SuccessResponse, FailResponse
class Presentation:

    @staticmethod
    def json_response(response: SuccessResponse | FailResponse, cookie:dict={}) -> HttpResponse:


        response = JsonResponse(response.to_dict())
        for k, v in cookie.items():
            response.set_cookie(key=k, value=v, httponly=True)
        return response
