FROM python:3.9-slim

# Set build argument with default value
ARG COMMIT_HASH=local

# Set environment variable from build argument
ENV COMMIT_HASH=$COMMIT_HASH

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
COPY templates/ ./templates/

CMD ["python", "app.py"]