.PHONY: test

test:
	export LC_ALL=C.UTF-8; \
	export LANG=C.UTF-8; \
	unset KOSMORRO_LATITUDE; \
	unset KOSMORRO_LONGITUDE; \
	unset KOSMORRO_TIMEZONE; \
	LANG=C pipenv run python3 -m coverage run -m unittest test

build: i18n manpages
	python3 setup.py sdist bdist_wheel

messages:
	pipenv run python setup.py extract_messages --output-file=kosmorrolib/locales/messages.pot

manpages:
	ronn --roff manpage/kosmorro.1.md
	ronn --roff manpage/kosmorro.7.md

i18n:
	if [ "$$POEDITOR_API_ACCESS" != "" ]; then \
		python3 .scripts/build/getlangs.py; \
		python3 setup.py compile_catalog; \
	fi

env:
	@if [[ "$$RELEASE_NUMBER" == "" ]]; \
		then echo "Missing environment variable: RELEASE_NUMBER."; \
		echo 'Example: export RELEASE_NUMBER="1.0.0" (without the leading "v")'; \
		exit 1; \
	fi

release: env
	@echo -e "\e[1mCreating release with version number \e[36m$$RELEASE_NUMBER\e[0m"
	@echo

	sed "s/^VERSION =.*/VERSION = '$$RELEASE_NUMBER'/g" kosmorrolib/version.py > version.py
	mv version.py kosmorrolib/version.py

	pipenv run python setup.py extract_messages --output-file=kosmorrolib/locales/messages.pot > /dev/null

	conventional-changelog -p angular -i CHANGELOG.md -s
	sed "0,/\\[\\]/s/\\[\\]/[v$$RELEASE_NUMBER]/g" CHANGELOG.md > /tmp/CHANGELOG.md
	sed -e "s/...v)/...v$$RELEASE_NUMBER)/" /tmp/CHANGELOG.md > CHANGELOG.md
	rm /tmp/CHANGELOG.md

	@echo
	@echo -e "\e[1mRelease \e[36m$$RELEASE_NUMBER\e[39m is ready to commit."
	@echo -e "Please review the changes, then invoke \e[33mmake finish-release\e[39m."

finish-release: env
	git add CHANGELOG.md kosmorrolib/version.py kosmorrolib/locales/messages.pot
	git commit -m "build: bump version $$RELEASE_NUMBER"
	git tag "v$$RELEASE_NUMBER"
	git checkout features
	git merge master
	git checkout master

	@echo
	@echo -e "\e[1mVersion \e[36m$$RELEASE_NUMBER\e[39m successfully tagged!"
	@echo -e "Invoke \e[33mgit push origin master features v$$RELEASE_NUMBER\e[39m to finish."
