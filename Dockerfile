# Use lightweight Python image
FROM python:3.9.23

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything (backend + frontend + model)
COPY . .

# Expose port
EXPOSE 5000

# Start Flask
CMD ["python", "app.py"]