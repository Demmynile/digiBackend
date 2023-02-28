from rest_framework.exceptions import APIException


class AuthenticationException(APIException):
    status_code = 400
    default_detail = "Password or Username Is Not Correct."
    default_code = "Password or Username Is Not Correct"