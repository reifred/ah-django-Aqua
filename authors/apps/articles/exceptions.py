from rest_framework.exceptions import APIException

class ArticleDoesNotExist(APIException):
    status_code = 404
    default_detail = "Article does not exist in your articles."
