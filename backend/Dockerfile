FROM python:3.11-slim-bullseye

WORKDIR /app/backend

# Install system dependencies for PDF generation
RUN apt-get update && apt-get install -y wkhtmltopdf && rm -rf /var/lib/apt/lists/*

# Copy backend files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir .

EXPOSE 8000

# Run FastAPI server
CMD ["uvicorn", "sponsorcheck.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
