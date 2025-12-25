import os
import subprocess
import time
from pathlib import Path

from chatapp import settings
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
        subprocess.run(
            [
                "javascript-obfuscator",
                file_path,
                "--output", file_path,
        
                # Core
                "--compact", "true",
                "--log", "false",
        
                # Control flow
                "--control-flow-flattening", "true",
                "--control-flow-flattening-threshold", "1",
        
                # Dead code
                "--dead-code-injection", "true",
                "--dead-code-injection-threshold", "1",
        
                # Debug protection
                "--debug-protection", "true",
                "--debug-protection-interval", "4000",
                "--disable-console-output", "true",
        
                # Identifiers
                "--identifier-names-generator", "hexadecimal",
                "--rename-globals", "false",
        
                # Self defending
                "--self-defending", "true",
        
                # Optimizations
                "--numbers-to-expressions", "true",
                "--simplify", "true",
        
                # Strings
                "--split-strings", "true",
                "--split-strings-chunk-length", "5",
        
                # String array
                "--string-array", "true",
                "--string-array-threshold", "1",
                "--string-array-calls-transform", "true",
                "--string-array-encoding", "rc4",
                "--string-array-index-shift", "true",
                "--string-array-rotate", "true",
                "--string-array-shuffle", "true",
        
                # String array wrappers
                "--string-array-wrappers-count", "5",
                "--string-array-wrappers-chained-calls", "true",
                "--string-array-wrappers-parameters-max-count", "5",
                "--string-array-wrappers-type", "function",
        
                # Object keys
                "--transform-object-keys", "true",
        
                # Unicode
                "--unicode-escape-sequence", "false",
            ],
            check=True
        )


