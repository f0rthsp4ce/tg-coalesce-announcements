.PHONY: run

run-%: settings.json
	poetry run python3 app/__init__.py $*

settings.json: settings.dhall
	dhall-to-json --file settings.dhall --output settings.json
