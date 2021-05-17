FROM python:3.9-slim

RUN useradd --create-home --shell /bin/bash kosmorro

WORKDIR /home/kosmorro

ENV PATH="/home/kosmorro:${PATH}"

# Prepare environment
RUN python -m pip install --upgrade pip
RUN pip install pipenv
COPY Pipfile.lock .
RUN pipenv sync && pipenv run pip freeze > requirements.txt

# Add files
RUN pip install -r requirements.txt
COPY _kosmorro/ _kosmorro/
COPY kosmorro .

# Compile the translations
RUN pip install Babel
COPY setup.py setup.py
COPY setup.cfg setup.cfg
COPY README.md README.md
RUN python setup.py compile_catalog

# Clean the image
RUN rm setup.py setup.cfg README.md && \
    rm _kosmorro/locales/messages.pot _kosmorro/locales/*/LC_MESSAGES/messages.po && \
    pip uninstall --yes Babel pipenv

USER kosmorro

CMD ["bash"]
