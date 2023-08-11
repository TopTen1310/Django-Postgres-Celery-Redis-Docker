FROM python:3.10

# Environment setup
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory and install python dependencies
RUN mkdir -p /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt

COPY wait-for-it.sh /app
RUN chmod +x /app/wait-for-it.sh