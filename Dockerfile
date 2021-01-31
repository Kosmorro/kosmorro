FROM python:3.9-slim

RUN useradd --create-home --shell /bin/bash kosmorro

WORKDIR /home/kosmorro

ENV PATH="/home/kosmorro:${PATH}"

RUN python -m pip install --upgrade pip

RUN pip install pipenv

COPY Pipfile.lock .

RUN pipenv sync && pipenv run pip freeze > requirements.txt

RUN pip uninstall pipenv -y

RUN pip install -r requirements.txt

COPY kosmorrolib/ kosmorrolib/

COPY kosmorro .

USER kosmorro

CMD ["bash"]
