FROM python:3.9-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HOST_DEFAULT_IP        prod-4fluid-iot-aurora-cluster.cluster-ro-c6zjoohnrdv4.sa-east-1.rds.amazonaws.com
ENV HOST_DEFAULT_USER      kdi_read
ENV HOST_DEFAULT_PASSWORD  isua@kpufo!
ENV HOST_DEFAULT_NAME      postgres
ENV HOST_DEFAULT_PORT      5432
ENV HOST_SECOND_NAME       devstattus4_4fluid
ENV HOST_SECOND_USER       dev4fluid
ENV HOST_SECOND_PASSWORD   90Br1DXyXE59eRljSv6Z
ENV HOST_SECOND_IP         rds-4fluid-movel.c6zjoohnrdv4.sa-east-1.rds.amazonaws.com
ENV HOST_SECOND_PORT       1433
ENV PYTHONPATH /app:$PYTHONPATH


RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . /app/

EXPOSE 8500

RUN python manage.py migrate

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8500"]


