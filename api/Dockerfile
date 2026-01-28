FROM python:3.14.2-alpine3.23

WORKDIR /app

ENV FLASK_APP=app:create_app
ENV FLASK_RUN_HOST=0.0.0.0

COPY api/requirements.txt app/
RUN pip install --no-cache-dir -r app/requirements.txt

COPY api/app/ app/

ENTRYPOINT ["flask", "run"]