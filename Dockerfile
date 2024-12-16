# Use an official Python runtime as a parent image
FROM python:3.12.8 AS backend-build

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --upgrade pip
RUN pip install poetry

# Add Poetry to PATH
ENV PATH="${PATH}:/root/.local/bin"

# Copy project files
COPY pyproject.toml poetry.lock* ./

# Copy the rest of the application
COPY . .

# Build frontend
WORKDIR /app/frontend
RUN npm install
RUN npm run build

# Set work directory
WORKDIR /app

# Expose port
EXPOSE 80

# Install backend dependencies
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

# Run the application
CMD ["poetry", "run", "python", "app.py"]
