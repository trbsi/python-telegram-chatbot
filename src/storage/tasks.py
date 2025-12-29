import bugsnag
from celery import shared_task

from src.storage.background_tasks.clear_temp_folder.clear_temp_folder_cron import ClearTempFolderCron


@shared_task
def cron_clear_temp_folder():
    try:
        task = ClearTempFolderCron()
        task.clear_temp_folder()
    except Exception as e:
        bugsnag.notify(e)
