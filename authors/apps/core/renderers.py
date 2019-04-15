import json

from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList

class AuthorsJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = 'object'
    object_labels = 'objects'

    def render(self, data, media_type=None, renderer_context=None):
        if isinstance(data, ReturnList):
            _data = json.loads(
                super(AuthorsJSONRenderer, self).render(data).decode('utf-8')
            )

            return json.dumps({
                self.object_labels : _data,
                "ProfilesCount" : len(_data)
            })
        else:
            # If the view throws an error (such as the user can't be authenticated)
            # `data` will contain an `errors` key. We want
            # the default JSONRenderer to handle rendering errors, so we need to
            # check for this case.
            errors = data.get('errors', None)

        if errors is not None:
            # As mentioned above, we will let the default JSONRenderer handle
            # rendering errors.
            return super(AuthorsJSONRenderer, self).render(data)

        return json.dumps({
            self.object_label: data
        })

