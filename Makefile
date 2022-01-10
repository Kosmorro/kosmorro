black:
	pipenv run black kosmorro _kosmorro setup.py

.PHONY: build
build: manpage
	python3 setup.py sdist bdist_wheel

.PHONY: manpage
manpage:
	ronn --roff manpage/kosmorro.1.md
	ronn --roff manpage/kosmorro.7.md

messages:
	pipenv run python setup.py extract_messages --output-file=_kosmorro/locales/messages.pot

i18n:
	pipenv run python setup.py compile_catalog

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
