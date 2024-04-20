.PHONY: run docker

run-%: settings.json
	poetry run python3 app/__init__.py $*

settings.json: settings.dhall
	dhall-to-json --file settings.dhall --output settings.json

docker:
	docker build . -t tg-coalesce-announcements
	docker run --env-file=.env --rm -it tg-coalesce-announcements  