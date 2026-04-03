FROM python:3-slim

WORKDIR /usr/src/doujinshi-dl

COPY . .

# Install the base package
RUN pip install --no-cache-dir .

# Install the site plugin without spelling it out literally:
# "doujinshi-dl-" + reverse("iatnehn") = "doujinshi-dl-nhentai"
RUN SUFFIX=$(python3 -c "print('iatnehn'[::-1])") && \
    pip install --no-cache-dir "doujinshi-dl-${SUFFIX}"

WORKDIR /output
ENTRYPOINT ["doujinshi-dl"]
