# syntax=docker/dockerfile:1

# Use official Python runtime
FROM python:3.13

# Set working directory
WORKDIR /backend

# add src to pythonpath
ENV PYTHONPATH=/backend/

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (optional for web apps)
EXPOSE 5000

# Run the application
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]
