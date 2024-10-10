# Use the official Python slim image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Make port 7000 available to the world outside this container
EXPOSE 5600

# Run the Python script when the container launches
CMD flask run --host=0.0.0.0 --debug