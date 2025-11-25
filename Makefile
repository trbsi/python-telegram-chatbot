.PHONY: builddocker, migrate

builddocker:
	cd docker && docker compose up -d --build

migrate:
    de docker && docker exec -it protectapp-django poetry run python manage.py migrate