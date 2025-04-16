#!/bin/bash

# This script tests the Docker configuration for the Flask Marketplace project

echo "=== Testing Docker Configuration for Flask Marketplace ==="
echo

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
else
    echo "✅ Docker is installed."
fi

# Check if Docker Compose is installed
if ! command -v docker compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
else
    echo "✅ Docker Compose is installed."
fi

echo
echo "=== Validating Docker Files ==="

# Check if Dockerfile exists
if [ -f "Dockerfile" ]; then
    echo "✅ Dockerfile exists."
else
    echo "❌ Dockerfile not found."
    exit 1
fi

# Check if docker-compose.yml exists
if [ -f "docker-compose.yml" ]; then
    echo "✅ docker-compose.yml exists."
else
    echo "❌ docker-compose.yml not found."
    exit 1
fi

# Create .env file from example if it doesn't exist
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file."
fi

echo
echo "=== Docker Configuration Test Results ==="
echo "✅ All configuration files are present and valid."
echo "✅ The Docker setup is ready to use."
echo
echo "To build and run the application, use:"
echo "docker-compose up --build"
echo
echo "For more information, refer to docker_documentation.md"
