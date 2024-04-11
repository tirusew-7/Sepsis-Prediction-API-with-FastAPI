# Use the official Python base image with Python 3.12.2
FROM python:3.12.2

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any dependencies
RUN pip install --timeout 3000 -r requirements.txt

# Copy the entire project directory into the container at /app
COPY . .

# Expose the port that FastAPI runs on
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "src.Sepsis:app", "--host", "0.0.0.0", "--port", "8000"]
