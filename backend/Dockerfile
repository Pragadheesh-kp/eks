# Use an official Python runtime as the base image

FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install the required Python dependencies
RUN pip install --no-cache-dir flask flask-cors psycopg2-binary

# Expose the port on which the backend will run
EXPOSE 5000

# Define environment variables (these can be overridden at runtime)
ENV DB_NAME=cruddb
ENV DB_USER=pragadheeshwaran
ENV DB_PASSWORD=Pragade123@
ENV DB_HOST=192.168.113.114
ENV DB_PORT=5432

# Command to run the backend application
CMD ["python3", "backend.py"]

