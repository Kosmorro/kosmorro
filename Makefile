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
	python3 setup.py compile_catalog

changelog:
	conventional-changelog -p angular -i CHANGELOG.md -s

prepare-release: messages changelog
	@echo
	@echo "Before tagging, don't forget to update version number in CHANGELOG"

clean:
	rm -rf build dist kosmorro.egg-info manpage/kosmorro.{1,7}{,.html}
