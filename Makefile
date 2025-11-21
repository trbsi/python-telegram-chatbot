.PHONY: builddocker

builddocker:
	cd docker && docker compose up -d --build