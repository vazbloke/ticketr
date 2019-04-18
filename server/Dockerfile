# Use an official Python runtime as a parent image
FROM python:2.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY app.py /app

# Install any needed packages specified in requirements.txt
RUN pip install flask requests flask-cors pymongo

# Make port 80 available to the world outside this container
EXPOSE 5000

# Run server.py when the container launches
CMD ["python", "-u", "app.py"]