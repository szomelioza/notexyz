FROM python:3.14.2-alpine3.23

WORKDIR /app

RUN mkdir /images && chown 1000:1000 /images

COPY api/requirements.txt app/
RUN pip install --no-cache-dir -r app/requirements.txt

COPY api/app/ app/

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "'app:create_app()'"]