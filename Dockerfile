FROM python:3

WORKDIR /usr/src/doujinshi-dl

COPY . .
RUN pip install --no-cache-dir .

WORKDIR /output
ENTRYPOINT ["doujinshi-dl"]
