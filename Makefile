black:
	pipenv run black kosmorro _kosmorro tests setup.py

.PHONY: tests
tests:
	@if [ "$${TEXLIVE_INSTALLED}" == "" ]; then \
  		echo "If you are running the tests locally and TeXLive is installed on your machine, you will need to set the TEXLIVE_INSTALLED environment variable."; \
  		echo; \
	fi

	pipenv run python3 -m pytest tests/*.py

.PHONY: build
build: manpage
	python3 setup.py sdist bdist_wheel

.PHONY: manpage
manpage:
	ronn --roff manpage/kosmorro.1.md
	ronn --roff manpage/kosmorro.7.md

messages:
	pipenv run pybabel extract --output=_kosmorro/locales/messages.pot _kosmorro

i18n:
	pipenv run pybabel compile --directory=_kosmorro/locales

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
