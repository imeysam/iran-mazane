# Base image with Python
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the port if your bot serves a web interface (optional)
# EXPOSE 5000

# Command to run the bot script
CMD ["python", "bot.py"]
