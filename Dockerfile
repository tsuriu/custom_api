FROM python:3.10-bullseye

# Create a non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Use a Python equivalent package for nmap
RUN pip install --upgrade pip && \
    pip install python-nmap  # Python wrapper for nmap

# Create and set working directory
RUN mkdir /api
WORKDIR /api

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy requirements and install dependencies
COPY ./requirements.txt /api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the application code
COPY ./app /api/app

# Set a HEALTHCHECK instruction to monitor the container's health
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl --fail http://localhost:8000/api/healthchecker || exit 1

# Switch to non-root user
USER appuser

# Default command
CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8000"]