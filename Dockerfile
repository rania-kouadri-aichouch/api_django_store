# pull the official base image
FROM python:3.8 as production

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a root directory for our project in the container
RUN mkdir store-backend

# Create and virtual environment for python (venv)
RUN python3 -m venv store-backend/venv

# Activate the venv
RUN . store-backend/venv/bin/activate

# Copy the root directory contents into the container at /store-backend
COPY . store-backend/

# create the media and static folder
RUN mkdir store-backend/store_backend/media
RUN mkdir store-backend/store_backend/static

# Install dependencies and any needed packages
RUN pip install -r store-backend/requirements.txt

# Set the working directory to the project directory
WORKDIR store-backend/store_backend

# Make migrations and run them
RUN python manage.py makemigrations
RUN python manage.py migrate

# Collect the static files
RUN python3 manage.py collectstatic

# Specify the port number the container should expose
EXPOSE 8000

# Run the server instance
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "store_backend.wsgi:application"]
