"""App configuration for ioc app."""
from django.apps import AppConfig


class IocConfig(AppConfig):
    """class for ioc app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "ioc"
