import bugsnag
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from src.gpu.models import GpuInstance
from src.gpu.services.my_gpu_service import MyGpuService


@require_POST
@csrf_exempt
def register_gpu(request: HttpRequest) -> JsonResponse:
    try:
        service = MyGpuService()
        gpu_instance_value_object = service.get_my_gpu()
        gpu_instance: GpuInstance = GpuInstance.objects.filter(id=gpu_instance_value_object.instance_id).first()
        
        if gpu_instance is None:
            GpuInstance.objects.create(
                instance_id=int(gpu_instance_value_object.instance_id),
                ip_address=gpu_instance_value_object.public_ip,
                port=gpu_instance_value_object.port,
            )
        else:
            gpu_instance.ip_address = gpu_instance_value_object.public_ip
            gpu_instance.port = gpu_instance_value_object.port
            gpu_instance.status = gpu_instance_value_object.status
            gpu_instance.save()
    except Exception as e:
        bugsnag.notify(e)

    return JsonResponse({'status': 'success'})
