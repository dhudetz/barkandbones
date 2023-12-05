# Use the latest Python image
FROM python:latest

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the content to the working directory (if you have any static files)
COPY . .

# Expose port 8000
EXPOSE 8000

# Run Python's built-in HTTP server on port 8000
CMD ["python", "-m", "http.server", "8000"]