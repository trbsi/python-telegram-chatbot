from protectapp import settings


def global_vars(request):
    return {
        'TEMPLATE_APP_NAME': settings.APP_NAME,
    }
