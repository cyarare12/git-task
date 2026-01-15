from django.apps import AppConfig


class EcommerceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecommerce'

    def ready(self):
        import ecommerce.signals
        # Initialize Tweet class (commented out for now since it requires Twitter API keys)
        # from .functions.tweet import Tweet
        # Tweet()
