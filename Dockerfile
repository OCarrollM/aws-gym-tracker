# Use python always
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy everything from root down
COPY . .

# Port
EXPOSE 8080

# Run B)
CMD ["python", "main.py"]