############## BASE STAGE BUILDING ##############
FROM python:3.10 AS base

# Set python env
ENV PYTHONUNBUFFERED 1

# Create main project folder
RUN mkdir /app
WORKDIR /app

# Copy and install project requirements
COPY requirements/base.txt requirements/base.txt
RUN pip install --no-cache-dir -r requirements/base.txt

# Copy rest of files that not included in .dockeringore
COPY . .

# Set base environments
ENV DJANGO_SETTINGS_MODULE=app.settings.base

# Base stage entrypoint
CMD ["bash"]


############## DEVELOPMENT STAGE BUILDING ##############
FROM base AS development

# Set development environments
ENV DJANGO_SETTINGS_MODULE=app.settings.development
ENV DEBUG=True

# Copy and install project requirements
COPY requirements/development.txt requirements/development.txt
RUN pip install --no-cache-dir -r requirements/development.txt

# Setting the port that the container will listen on
EXPOSE 8000

# Command to be run during container start-up
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


############## PRODUCTION STAGE BUILDING ##############
FROM base AS production

# Set production environments
ENV DJANGO_SETTINGS_MODULE=app.settings.production
ENV DEBUG=False

# Copy and install project requirements
COPY requirements/production.txt requirements/production.txt
RUN pip install --no-cache-dir -r requirements/production.txt

# Setting the port that the container will listen on
EXPOSE 8000

# Command to be run during container start-up
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]
