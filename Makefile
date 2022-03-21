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

changelog:
	conventional-changelog -p angular -i CHANGELOG.md -s

prepare-release: messages changelog
	@echo
	@echo "Before tagging, don't forget to update version number in CHANGELOG"

appdir:
	appimage-builder --skip-tests
	mv *.AppImage dist/
	mv *.zsync dist/

appimage: appdir

clean:
	rm -rf build dist appimage-builder-cache kosmorro.egg-info manpage/kosmorro.{1,7}{,.html}
