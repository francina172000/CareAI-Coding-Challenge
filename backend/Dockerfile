# backend/Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for psycopg2 (if any, often build-essential and libpq-dev)
# For slim images, you might need to install gcc and other build tools first if your deps need compiling
# RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY ./requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
# --no-cache-dir: Disables the cache, which can make the image smaller.
# --default-timeout=100: Increases timeout for pip if network is slow.
# --compile: Compiles py files to pyc (optional, can slightly speed up startup).
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# Copy the rest of the backend application code into the container at /app
COPY ./app /app/app

# Make port 8000 available to the world outside this container (FastAPI default)
EXPOSE 8000

# Define environment variable (if needed, though .env is usually preferred for local dev)
# ENV MODULE_NAME app.main
# ENV VARIABLE_NAME app

# Run app.main when the container launches
# The command should be uvicorn app.main:app --host 0.0.0.0 --port 8000
# Using 0.0.0.0 makes the server accessible from outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
