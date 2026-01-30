FROM python:3.14.2-alpine3.23

WORKDIR /app

ENV FLASK_APP=app:create_app
ENV FLASK_RUN_HOST=0.0.0.0

RUN mkdir /images && chown 1000:1000 /images

COPY api/requirements.txt app/
RUN pip install --no-cache-dir -r app/requirements.txt

COPY api/app/ app/

ENTRYPOINT ["flask", "run"]