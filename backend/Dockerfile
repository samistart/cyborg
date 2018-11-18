# Pull base image.
FROM ubuntu

# Install system dependencies
# libssl-dev for SSL certificate verification from pip repositories
RUN apt-get update && apt-get install -y libssl-dev && rm -rf /var/lib/apt/lists/* && apt-get clean

# Install Python.
RUN \
  apt-get update && \
  apt-get install -y python3 python3-pip python3-psycopg2 python3-dev python3-virtualenv gunicorn curl && \
  rm -rf /var/lib/apt/lists/*

# Use Python 3 version of gunicorn
RUN apt-get -y remove gunicorn
RUN pip3 install gunicorn

# Install Python dependencies
COPY app/requirements.txt /requirements.txt
RUN pip3 install --no-cache-dir -r /requirements.txt

# Copy directories and define working directory.
COPY app /app
WORKDIR /app
VOLUME /app

# Expose port that gunicorn is listening on
EXPOSE 8000

# Define default command.
CMD ["gunicorn","run:app","-b",":8000"]
