# Use Python 3.7 as base image
FROM python:3.7-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install dependencies for Firefox and other required packages
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    firefox-esr \
    build-essential \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Download and install GeckoDriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz && \
    tar -zxvf geckodriver-v0.35.0-linux64.tar.gz && \
    mv geckodriver /usr/local/bin/geckodriver && \
    rm geckodriver-v0.35.0-linux64.tar.gz && \
    chmod +x /usr/local/bin/geckodriver

# Copy the project source code from the local host to the filesystem of the container
COPY . .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV NAME=app

# Run the application
CMD [ "python", "run.py" ]
