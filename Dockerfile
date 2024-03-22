# Set Python base image
FROM python:3.12.1-slim

# Set working directory within Docker image
WORKDIR /app

# Install system dependencies required for Chrome
RUN apt-get update \
    && apt-get install -y wget unzip libglib2.0-0 libnss3 libxcb1-dev \
    && rm -rf /var/lib/apt/lists/*

# Download and install Chrome
RUN wget -q -O /tmp/chrome.zip https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.58/linux64/chrome-linux64.zip \
    && unzip -o /tmp/chrome.zip -d /usr/local/bin/ \
    && rm /tmp/chrome.zip

# Download and install ChromeDriver (assuming you still need it)
RUN wget -q -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.58/linux64/chromedriver-linux64.zip \
    && unzip -o /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip

# Copy the entirety of the current directory into the Docker /app directory
COPY . /app

# Install packages in requirements.txt
RUN pip --no-cache-dir install -r requirements.txt

# Run the app
CMD [ "python3", "app.py" ]

