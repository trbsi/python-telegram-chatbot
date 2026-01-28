import bugsnag
from django.core.management.base import BaseCommand
from requests import HTTPError

from src.gpu.models import GpuInstance
from src.gpu.services.create_gpu_instance_service import CreateGpuInstanceService
from src.gpu.services.destroy_gpu_service import DestroyGpuService
from src.gpu.services.find_gpu_service import FindGpuService
from src.gpu.services.get_gpu_service import GetGpuService
from src.gpu.value_objects.gpu_instance_value_object import GpuInstanceValueObject


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.find_gpu_service = FindGpuService()
        self.create_gpu_service = CreateGpuInstanceService()
        self.destroy_gpu_service = DestroyGpuService()
        self.get_gpu_service = GetGpuService()

    def handle(self, *args, **options):
        gpu_instance: GpuInstance = GpuInstance.objects.order_by('-id').first()

        try:
            if not gpu_instance:
                self._create_new_instance()
                bugsnag.notify(Exception('Instance does not exist in database'))
                return

            current_instance = self.get_gpu_service.get_instance(int(gpu_instance.instance_id))
            gpu_instance.price_per_hour = current_instance.price_per_hour
            gpu_instance.save()

            if not current_instance.is_active():
                self._create_new_instance()
                bugsnag.notify(Exception('GPU not running'))
            elif current_instance.is_expensive():
                self._gpu_is_expensive(current_instance)
                bugsnag.notify(Exception('GPU is expensive'))
            else:
                print('Everything is ok')
        except (Exception, HTTPError) as e:
            self._create_new_instance()
            bugsnag.notify(e)

    def _gpu_is_expensive(self, current_instance: GpuInstanceValueObject):
        print('GPU is expensive. Finding cheap one.')
        offer = self.find_gpu_service.find_cheapest_gpu()
        instance = None

        if offer.price_per_hour < current_instance.price_per_hour:
            print('Found cheap one')
            gpu_instance: GpuInstance = GpuInstance.objects.order_by('-id').first()
            if gpu_instance:
                gpu_instance.delete()

            print('Destroying existing instance. Creating new one.')
            self.destroy_gpu_service.destroy_instance(current_instance.instance_id)
            instance = self.create_gpu_service.create_instance(offer_id=offer.offer_id)
            # database model will be created via /register-gpu endpoint

        print(offer.__dict__)
        print(instance.__dict__)

    def _create_new_instance(self):
        print('Destroying existing. Finding cheapest GPU. Creating new one')
        gpu_instance = GpuInstance.objects.order_by('-id').first()
        if gpu_instance:
            gpu_instance.delete()
            try:
                self.destroy_gpu_service.destroy_instance(gpu_instance.instance_id)
            except Exception:
                pass
        else:
            self.destroy_gpu_service.destroy_other_instance()

        offer = self.find_gpu_service.find_cheapest_gpu()
        instance = self.create_gpu_service.create_instance(offer_id=offer.offer_id)
        # database model will be created via /register-gpu endpoint

        print(offer.__dict__)
        print(instance.__dict__)
