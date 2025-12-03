import os
import subprocess
import time
from pathlib import Path

from protectapp import settings
from src.core.management.commands.base_command import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--minify_and_obfuscate", type=int, default=1)

    def handle(self, *args, **options):
        minify_and_obfuscate = options['minify_and_obfuscate']

        directory = settings.STATICFILES_DIRS[0]
        exclude_files = [
            'push_notifications.js',
            'service_worker.js',
            'install_app.js'
        ]
        file_min_js = f'{directory}/js/all.min.js'
        if os.path.exists(file_min_js):
            os.unlink(file_min_js)

        # Just to delete the file properly
        time.sleep(1)

        js_content = []
        for root, _, files in os.walk(directory):
            for filename in files:  # loop through files in the current directory
                full_path = Path(os.path.join(root, filename))

                if full_path.suffix != '.js':
                    continue

                if filename in exclude_files:
                    self.warning('Excluding file {}'.format(full_path))
                    continue

                with open(full_path, 'r') as file:
                    js_content.append(file.read())

        with open(file_min_js, 'w') as f:
            f.write('\n\n'.join(js_content))

        # obfuscate
        if (minify_and_obfuscate):
            self._minify_and_obfuscate(file_min_js)

        self.success('File written')

    def _minify_and_obfuscate(self, file_path: str) -> None:
        # Minify step
        subprocess.run([
            "terser",
            file_path,
            "--compress",
            "--mangle",
            "--output",
            file_path
        ], check=True)

        # Obfuscation step
        subprocess.run([
            "javascript-obfuscator",
            file_path,
            "--output",
            file_path,
            "--compact",
            "--control-flow-flattening"
        ], check=True)
