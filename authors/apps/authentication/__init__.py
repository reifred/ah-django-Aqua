from django.apps import AppConfig


class AuthenticationAppConfig(AppConfig):
    name = 'authors.apps.authentication'
    label = 'authentication'
    verbose_name = 'Authentication'

    def ready(self):
        import authors.apps.authentication.signals


default_app_config = 'authors.apps.authentication.AuthenticationAppConfig'
    # In here we create a custom application that will be used by
    # django to pick up signals of a new user being created ,
    # and then pick it up and use it to create the coresponding
    # profile.

