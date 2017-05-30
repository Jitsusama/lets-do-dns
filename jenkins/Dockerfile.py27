FROM python:2.7

RUN mkdir /environment
WORKDIR /environment
COPY dev-requirements.txt test-requirements.txt requirements.txt /environment/

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r dev-requirements.txt
