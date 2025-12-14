from core.utils import full_url_for_route
from protectapp import settings
from user.models import Invitation


def global_vars(request):
    invitation_left = 0
    invitation_url = ''
    if request.user.is_authenticated:
        user = request.user
        invitation_left = Invitation.invitations_left(user)
        invitation_url = full_url_for_route('home', query_params={'invitation': user.username})

    return {
        'TEMPLATE_APP_NAME': settings.APP_NAME,
        'TEMPLATE_APP_ENV': settings.APP_ENV,
        'TEMPLATE_INVITATIONS_LEFT': invitation_left,
        'TEMPLATE_INVITATION_URL': invitation_url,
    }
