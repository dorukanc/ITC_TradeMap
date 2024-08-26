# Use Python 3.8-slim as base image to avoid compatibility issues
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install dependencies for Firefox and other required packages
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    firefox-esr \
    build-essential \
    gcc \
    gfortran \
    libatlas-base-dev \
    libgfortran5 \
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

# Upgrade pip and install Python dependencies from requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV NAME=app

# Run the application
CMD [ "python", "run.py" ]
