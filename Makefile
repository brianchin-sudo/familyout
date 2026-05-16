.PHONY: install run test test-cov

install:
	python3 -m venv venv && venv/bin/pip install -r requirements.txt

run:
	FLASK_APP="app:create_app" venv/bin/flask run

test:
	venv/bin/pytest -v

test-cov:
	venv/bin/pytest --cov=app --cov-report=term-missing
