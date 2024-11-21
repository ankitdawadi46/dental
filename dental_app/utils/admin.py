from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered


def admin_autoregister(app_name, exclude_models=[]):
    # Register your models here.
    for pn_model in apps.get_app_config(app_name).get_models():
        if pn_model in exclude_models:
            continue
        try:
            admin.site.register(pn_model)
        except AlreadyRegistered:
            pass
