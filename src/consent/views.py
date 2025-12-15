from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET, require_POST

from src.consent.enums import ConsentEnum
from src.consent.services.media_consent.media_consent_service import MediaConsentService
from src.media.models import Media
from src.user.models import User


@require_GET
def request_consent(request: HttpRequest, media_id: int) -> HttpResponse:
    media_consent = __get_media_consent_cookies(request, media_id)
    response = redirect(reverse_lazy('consent.display_media_for_consent'))
    response.set_cookie(ConsentEnum.MEDIA_CONSENT_COOKIE.value, ','.join(media_consent), httponly=True)
    return response


@require_GET
@login_required
def display_media_for_consent(request: HttpRequest) -> HttpResponse:
    media_consent = __get_media_consent_cookies(request, None)
    user: User = request.user
    if not user.is_creator():
        raise Http404()

    media: QuerySet[Media] = Media.objects.select_related('user').filter(id__in=media_consent)
    return render(
        request,
        'display_media_for_consent.html',
        {
            'media': media
        })


@require_POST
@login_required
def give_media_consent(request: HttpRequest) -> HttpResponse:
    media_ids = request.POST.getlist('selectedMedia')
    messages.success(request, 'Consent successfully added for chosen media.')

    if not media_ids:
        return redirect(reverse_lazy('consent.display_media_for_consent'))

    service = MediaConsentService()
    service.attach_user_to_media(media_ids=media_ids, user=request.user)

    response = redirect(reverse_lazy('consent.display_media_for_consent'))
    response.delete_cookie(ConsentEnum.MEDIA_CONSENT_COOKIE.value)

    return response


def __get_media_consent_cookies(request: HttpRequest, media_id: int | None) -> list:
    media_consent = request.COOKIES.get(ConsentEnum.MEDIA_CONSENT_COOKIE.value)
    if media_consent:
        media_consent = media_consent.split(',')
    else:
        media_consent = []

    if media_id is not None:
        media_consent.append(str(media_id))
    media_consent = list(filter(None, media_consent))
    media_consent = list(set(media_consent))

    return media_consent
