import json
import random

import bugsnag
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST

from protectapp import settings
from src.core.utils import reverse_lazy_admin
from src.media.models import Media
from src.notification.services.notification_service import NotificationService
from src.notification.services.web_push_notifications.web_push_subscribe_service import WebPushSubscribeService
from src.notification.value_objects.email_value_object import EmailValueObject
from src.notification.value_objects.push_notification_value_object import PushNotificationValueObject


@require_GET
def api_web_push_keys(request: HttpRequest) -> JsonResponse:
    return JsonResponse({
        'public_key': settings.WEB_PUSH_PUBLIC_KEY
    })


@require_POST
@login_required
def api_web_push_subscribe(request: HttpRequest) -> JsonResponse:
    """
    body example:
    {'endpoint': 'https://web.push.apple.com/QDWQpghdBE...', 'keys': {'p256dh': 'BKSeSkq..., 'auth': '7LdJ...'}}
    """
    body = json.loads(request.body)

    print(body)
    web_service = WebPushSubscribeService()
    web_service.push_subscribe(request.user, body)

    return JsonResponse({})


@require_GET
def test_notifications(request: HttpRequest) -> JsonResponse:
    only = request.GET.get('only')
    for_user = request.GET.get('for_user')
    notifications = []

    if for_user:
        user = User.objects.get(username=for_user)
    else:
        user = User.objects.get(username='dinamo')

    if only == 'push':
        notifications.append(PushNotificationValueObject(
            user_id=user.id,
            body=f'This is test push notification {random.randint(1, 100000)}',
            title='Some cool title'
        ))
    elif only == 'email':
        notifications.append(EmailValueObject(
            subject='Test Email',
            template_path='emails/test_email.html',
            template_variables={'anchor_href': 'www.test.com', 'anchor_label': 'Click here to confirm your new email'},
            to=['admins']
        ))
    else:
        url = reverse_lazy_admin(object=Media(), action='changelist', is_full_url=True)
        notifications.append(EmailValueObject(
            subject='Test Email',
            template_path='emails/test_email.html',
            template_variables={'anchor_href': 'www.test.com', 'anchor_label': 'Click here to confirm your new email'},
            to=['admins']
        ))
        notifications.append(PushNotificationValueObject(
            user_id=user.id,
            body=f'This is test push notification {random.randint(1, 100000)}. {url}',
            title='Some cool title'
        ))

    bugsnag.notify(Exception(f'This is test error {random.randint(1, 100000)}'))
    NotificationService.send_notification(*notifications)

    return JsonResponse({'success': True})
