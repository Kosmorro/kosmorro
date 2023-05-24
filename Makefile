black:
	poetry run black kosmorro tests

.PHONY: tests
tests:
	LANG=C python3 -m poetry run pytest tests/*.py

.PHONY: build
build:
	poetry build

.PHONY: manpage
manpage:
	ronn --roff manpage/kosmorro.1.md
	ronn --roff manpage/kosmorro.7.md

messages:
	poetry run pybabel extract --output=kosmorro/locales/messages.pot kosmorro

i18n:
	poetry run pybabel compile --directory=kosmorro/locales

changelog: install-conventional-changelog generate-changelog delete-conventional-changelog


install-conventional-changelog:
	npm install conventional-changelog-cli

generate-changelog:
	node_modules/.bin/conventional-changelog -p angular -i CHANGELOG.md -s

prepare-release: messages changelog

delete-conventional-changelog:
	rm -rf \
		node_modules \
		package{,-lock}.json

clean: delete-conventional-changelog
	rm -rf \
		build \
		dist appimage-builder-cache \
		kosmorro.egg-info \
		manpage/kosmorro.{1,7}{,.html}
