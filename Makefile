test:
	tools/test.sh

dev:
	python manage.py runserver

lint:
	flake8 . --select=E9,F63,F7,F82 --show-source --statistics --exclude .venv
	flake8 . --max-complexity=10 --max-line-length=127 --statistics --exclude .venv
	prettier -c "templates/**/*.j2"

format:
	prettier -w "templates/**/*.j2"
