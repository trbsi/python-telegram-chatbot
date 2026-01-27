import bugsnag
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST

from src.gpu.models import GpuInstance


@require_POST
def register_gpu(request: HttpRequest) -> JsonResponse:
    try:
        post = request.POST
        gpu_instance = GpuInstance.objects.filter(id=post['instance_id']).first()
        if gpu_instance is None:
            GpuInstance.objects.create(
                instance_id=post['instance_id'],
                ip_address=post['ip'],
                port=post['port'],
            )
        else:
            gpu_instance.ip_address = post['ip']
            gpu_instance.port = post['port']
            gpu_instance.save()
    except Exception as e:
        bugsnag.notify(e)

    return JsonResponse({'status': 'success'})
