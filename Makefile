.PHONY: test

test:
	unset KOSMORRO_LATITUDE; \
	unset KOSMORRO_LONGITUDE; \
	unset KOSMORRO_TIMEZONE; \
	LANG=C pipenv run python3 -m coverage run -m unittest test

.PHONY: build
build: i18n
	python3 setup.py sdist bdist_wheel

i18n:
	ronn --roff manpage/kosmorro.1.md
	ronn --roff manpage/kosmorro.7.md

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

distmacapp = dist/Kosmorro.app
dist-mac-app: env
	@if [ -e $(distmacapp) ]; then echo "Deleting the existing app."; rm -rf $(distmacapp); fi
	mkdir -p "$(distmacapp)/Contents/MacOS" "$(distmacapp)/Contents/Resources"

	# Add application files
	cp "kosmorro" "$(distmacapp)/Contents/MacOS/kosmorro"
	cp -r "kosmorrolib" "$(distmacapp)/Contents/MacOS/kosmorrolib"
	cp "Pipfile" "$(distmacapp)/Contents/MacOS/Pipfile"
	cp "Pipfile.lock" "$(distmacapp)/Contents/MacOS/Pipfile.lock"

	# Install dependencies
	cd $(distmacapp)/Contents/MacOS && PIPENV_VENV_IN_PROJECT=1 pipenv sync
	cd $(distmacapp)/Contents/MacOS && source .venv/bin/activate && pip install wxPython latex

	# Add Python binaries and remove the links in the virtualenv
	cp -r "$$(dirname $$(realpath $$(which python3)))/.." $(distmacapp)/Contents/MacOS/python
	rm $(distmacapp)/Contents/MacOS/.venv/bin/python{,3,3.9}

	# Add Mac-specific files
	cp "build/distrib/darwin/Info.plist" "$(distmacapp)/Contents/Info.plist"
	cp "build/distrib/darwin/launch-kosmorro.sh" "$(distmacapp)/Contents/MacOS/launch-kosmorro"
	cp "build/distrib/darwin/icon.icns" "$(distmacapp)/Contents/Resources/icon.icns"

	sed "s/{{app_version}}/$$RELEASE_NUMBER/" "build/distrib/darwin/Info.plist" > "$(distmacapp)/Contents/Info.plist"
	chmod +x "$(distmacapp)/Contents/MacOS/launch-kosmorro"

	# Clean package
	rm "$(distmacapp)/Contents/MacOS/Pipfile" "$(distmacapp)/Contents/MacOS/Pipfile.lock"

	@echo "Application created."

distmacdmg = dist/Kosmorro.dmg
dist-mac-dmg: dist-mac-app
	@if [ -e $(distmacdmg) ]; then echo "Deleting the existing DMG."; rm -rf $(distmacdmg); fi
	mkdir -p "$(distmacapp)/Contents/MacOS"
	mkdir -p dist/dmg
	cp -r $(distmacapp) dist/dmg
	create-dmg --volname "Kosmorro installer" \
	           --volicon build/distrib/darwin/dmg.icns \
	           --background build/distrib/darwin/dmg-background.png \
	           --icon-size 72 \
	           --icon Kosmorro.app 140 120 \
	           --window-size 640 365 \
	           --app-drop-link 475 120 \
	           --eula LICENSE.md \
	           $(distmacdmg) \
	           dist/dmg

	rm -rf dist/dmg

dist: dist-mac-dmg
