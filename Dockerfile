FROM python:3.9

COPY . .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HOST_DEFAULT_IP       = prod-4fluid-iot-aurora-cluster.cluster-ro-c6zjoohnrdv4.sa-east-1.rds.amazonaws.com
ENV HOST_DEFAULT_USER     = kdi_read
ENV HOST_DEFAULT_PASSWORD = isua@kpufo!
ENV HOST_DEFAULT_NAME     = postgres
ENV HOST_DEFAULT_PORT     = 5432
ENV HOST_SECOND_NAME      = devstattus4_4fluid
ENV HOST_SECOND_USER      = dev4fluid
ENV HOST_SECOND_PASSWORD  = 90Br1DXyXE59eRljSv6Z
ENV HOST_SECOND_IP        = rds-4fluid-movel.c6zjoohnrdv4.sa-east-1.rds.amazonaws.com
ENV HOST_SECOND_PORT      = 1433

# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# running migrations
RUN python manage.py migrate

# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]

