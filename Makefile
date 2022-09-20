test:
	poetry run pytest -sx

lint:
	poetry run pre-commit install && poetry run pre-commit run -a -v

run:
	poetry run python -m banco_imobiliario
