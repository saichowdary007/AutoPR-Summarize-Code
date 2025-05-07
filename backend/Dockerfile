FROM python:3.9

# Install build dependencies
RUN apt-get update && apt-get install -y gcc python3-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

# Install dependencies first to leverage Docker cache
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set environment variables
ENV HOST=0.0.0.0
ENV PORT=8000
ENV RELOAD=False

# Expose the API port
EXPOSE 8000

# Run the application
CMD ["python", "src/run.py"] 