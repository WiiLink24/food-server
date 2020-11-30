FROM python:3.9-alpine

RUN adduser -D server
WORKDIR /home/server

# Copy requirements first as to not disturb cache for other changes.
COPY requirements.txt .

# Required base dependencies for lxml.
RUN apk add -U --no-cache libxslt-dev libxml2-dev

RUN apk add --no-cache --virtual .build-deps build-base && \
  pip3 install -r requirements.txt && \
  pip3 install gunicorn && \
  apk del .build-deps

USER server

# Finally, copy the entire source.
COPY . .

ENV FLASK_APP food.py
EXPOSE 5000
ENTRYPOINT ["gunicorn", "-b", ":5000", "--access-logfile", "-", "--error-logfile", "-", "food:app"]
