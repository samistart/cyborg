# Pull base image.
FROM ubuntu

# Install System-Level Dependencies.
RUN \
  apt-get update && \
  apt-get install -y apt-utils nodejs npm curl && \
  rm -rf /var/lib/apt/lists/*

# Copy directories and define working directory.
COPY app /app
WORKDIR /app
VOLUME /app

# Expose port that gunicorn is listening on
EXPOSE 8001

# Define default command.
CMD ["npm", "start"]
