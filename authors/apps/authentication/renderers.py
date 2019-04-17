import json

from authors.apps.core.renderers import AuthorsJSONRenderer


class UserJSONRenderer(AuthorsJSONRenderer):
    object_label = 'user'

        
