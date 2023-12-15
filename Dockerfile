FROM python:3.10-slim-buster

# Install necessary packages
RUN apt-get update && apt-get install -y git
RUN pip3 install -U git+https://github.com/Rapptz/discord.py

# Set up work directory
RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

# Copy necessary files
COPY setup.py .
COPY README.md .
COPY ptn ptn

# Install your application
RUN pip3 install .

# Optional: Declare a volume (this is the directory inside the container)
VOLUME ["/app/data"]

# Set the working directory to where the data volume will be mounted
WORKDIR /app/data

# Set an environment variable with a default value for the data directory
ENV PTN_SPYPLANE_DATA_DIR=/app/data

# Set the entry point for the container
ENTRYPOINT ["/usr/local/bin/spyplane"]
