import json

from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST

from src.report.services.report.report_service import ReportService


@require_POST
def api_report(request: HttpRequest) -> JsonResponse:
    service = ReportService()
    data = json.loads(request.body)
    service.report(
        type=data.get('type'),
        content_id=int(data.get('content_id')),
        description=data.get('description'),
        user=request.user
    )
    return JsonResponse({})
