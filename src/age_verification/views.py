from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from src.age_verification.services.age_verification.age_verification_service import AgeVerificationService
from src.age_verification.services.creator_agreement.save_agreement_service import SaveAgreementService
from src.age_verification.services.creator_service import CreatorService
from src.core.utils import get_client_ip


@require_GET
@login_required
def become_creator(request: HttpRequest) -> HttpResponse:
    service = CreatorService()
    service.become_creator(user=request.user)

    return render(
        request,
        'become_creator.html',
        {
            'is_creator_agreement_completed': service.is_creator_agreement_completed(request.user),
            'is_age_verification_completed': service.is_age_verification_completed(request.user),
            'age_verification': service.get_age_verification(request.user)
        }
    )


@login_required
def creator_agreement(request) -> HttpResponse:
    creator_service = CreatorService()
    if creator_service.is_creator_agreement_completed(request.user):
        return redirect(reverse_lazy('age_verification.become_creator'))

    if request.method == 'POST':
        post = request.POST
        consent = post.get('consent')
        if consent != 'on':
            messages.error(request, 'You have to agree to the terms')
            return render(request, 'creator_agreement.html')

        service = SaveAgreementService()
        service.save_agreement(
            user=request.user,
            ip=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT')
        )
        messages.success(request, 'Consent was successfully signed')
        return redirect(reverse_lazy('age_verification.become_creator'))

    return render(request, 'creator_agreement.html')


@require_GET
@login_required
def start_age_verification(request: HttpRequest) -> HttpResponse:
    creator_service = CreatorService()
    if creator_service.is_age_verification_completed(request.user):
        return redirect(reverse_lazy('age_verification.become_creator'))

    service = AgeVerificationService()
    url = service.start_verification(request.user)

    return redirect(url)


@require_POST
@csrf_exempt
def webhook_age_verification(request: HttpRequest) -> JsonResponse:
    service = AgeVerificationService()
    result = service.finish_verification(request)

    if result:
        return JsonResponse({})

    return JsonResponse({'result': 'Something happened, check logs'}, status=400)


@require_GET
def country_restricted(request: HttpRequest) -> HttpResponse:
    return render(request, 'country_restricted.html')
