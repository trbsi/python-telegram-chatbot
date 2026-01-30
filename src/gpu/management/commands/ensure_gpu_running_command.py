import bugsnag
from django.core.management.base import BaseCommand
from requests import HTTPError

from src.chat.services.idle_messaging.idle_messaging_service import IdleMessagingService
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
        self.idle_messaging_service = IdleMessagingService()

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip-idle-message",
            action="store_true",
            help="To skip idle message condition",
        )

    def handle(self, *args, **options):
        creating_instance = GpuInstance.objects.filter(status=GpuInstance.STATUS_CREATING).count()
        if creating_instance > 0:
            print('There is instance being created.')
            return

        if options['skip_idle_message'] == False and self.idle_messaging_service.is_messaging_idle():
            print('There is idle messaging. Not creating instance.')
            return

        try:
            gpu_instance: GpuInstance = GpuInstance.objects.order_by('-id').first()
            if not gpu_instance:
                self._create_new_instance()
                bugsnag.notify(Exception('Instance does not exist in database'))
                return

            current_instance = self.get_gpu_service.get_instance(int(gpu_instance.instance_id))
            gpu_instance.price_per_hour = current_instance.price_per_hour
            gpu_instance.save()

            if not current_instance.is_active():
                self._create_new_instance()
                bugsnag.notify(Exception('GPU not running. Creating new one.'))
            elif current_instance.is_expensive():
                self._gpu_is_expensive(current_instance)
                bugsnag.notify(Exception('GPU is expensive. Trying to find cheaper.'))
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
            self._create_temp_instance(instance)

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
            self.destroy_gpu_service.destroy_all_instance()

        offer = self.find_gpu_service.find_cheapest_gpu()
        instance = self.create_gpu_service.create_instance(offer_id=offer.offer_id)
        self._create_temp_instance(instance)

        print(offer.__dict__)
        print(instance.__dict__)

    def _create_temp_instance(self, instance: GpuInstanceValueObject):
        GpuInstance.objects.create(
            instance_id=instance.instance_id,
            ip_address='0',
            port=0,
            status=GpuInstance.STATUS_CREATING
        )
