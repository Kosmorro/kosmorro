#!/usr/bin/env python3

# This script's purpose is to retrieve the translations from POEditor (https://poeditor.com).
# It is mainly used in the release process.
# (c) Jérôme Deuchnord - MIT License

import os
import requests

POEDITOR_URL = 'https://api.poeditor.com/v2'
API_TOKEN = os.environ['POEDITOR_API_ACCESS']
PROJECT_ID = os.environ['POEDITOR_PROJECT_ID']

languages = requests.post('%s/languages/list' % POEDITOR_URL,
                          data={'api_token': API_TOKEN,
                                'id': PROJECT_ID})

json = languages.json()

if languages.status_code != 200:
    raise AssertionError(json['response']['message'])

for language in json['result']['languages']:
    if language['percentage'] < 100:
        # Ignore unfinished translations
        continue

    print('Importing finished translation for %s... ' % language['name'], end='')

    translations = requests.post('%s/projects/export' % POEDITOR_URL,
                                 data={'api_token': API_TOKEN,
                                       'id': PROJECT_ID,
                                       'language': language['code'],
                                       'type': 'po'})

    if translations.status_code != 200:
        print('Failed!')
        raise AssertionError(translations.json()['response']['message'])

    translations = requests.get(translations.json()['result']['url'])

    if translations.status_code != 200:
        print('Failed!')
        raise AssertionError('URL given by the API returned a %d status code' % translations.status_code)

    os.makedirs('kosmorrolib/locales/%s/LC_MESSAGES' % language['code'], exist_ok=True)

    with open('kosmorrolib/locales/%s/LC_MESSAGES/messages.po' % language['code'], 'w') as file:
        file.write(translations.text)

    print('OK')

