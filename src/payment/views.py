import json

import bugsnag
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from src.payment.models import Balance, Package
from src.payment.services.buy_package.buy_package_service import BuyPackageService
from src.payment.services.my_payments.my_payments_service import MyPaymentsService
from src.payment.services.payment_webhook.payment_webhook_service import PaymentWebhookService
from src.user.models import User


@require_GET
@login_required
def my_spending(request: HttpRequest) -> HttpResponse:
    get = request.GET
    page = int(get.get('page', 1))
    payment_status = get.get('payment_status', None)  # This is when user is redirected from payment provider
    user = request.user

    if payment_status == 'cancel':
        messages.warning(request, 'Payment cancelled')
    elif payment_status == 'success':
        messages.success(request, 'Payment successful. Processing now...')

    service = MyPaymentsService()
    spendings = service.get_my_spendings(user=user, current_page=page)
    balance = Balance.get_user_balance(user)

    return render(
        request,
        'my_spendings.html',
        {
            'spendings': spendings,
            'balance': balance,
            'current_user': user
        },
    )


@require_GET
@login_required
def list_packages(request: HttpRequest) -> HttpResponse:
    context = {
        'packages': Package.objects.all(),
    }
    return render(request, 'list_packages.html', context)


@require_GET
@login_required
def buy_single_package(request: HttpRequest, package_id: int) -> HttpResponse:
    service = BuyPackageService()
    redirect_url = service.buy_defined_package(request.user, package_id).redirect_url
    return redirect(redirect_url)


# expect GET and POST
@csrf_exempt
def payment_webhook(request: HttpRequest) -> JsonResponse:
    if request.content_type == 'application/json':
        data = json.loads(request.body)
    else:
        data = request.POST.dict()

    bugsnag.notify(Exception(data))  # @TODO remove log

    webhook_service = PaymentWebhookService()
    result = webhook_service.handle_webook(request.GET.dict(), data)
    if result:
        return redirect(result)
    return JsonResponse({})


@require_GET
@login_required
def api_get_balance(request: HttpRequest) -> JsonResponse:
    try:
        user: User = request.user
        balance: Balance = Balance.objects.get(user=user)
        status = 'ok'
        if balance.balance < 100:
            status = 'low_balance'

        return JsonResponse({'balance': balance.balance, 'status': status})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)
