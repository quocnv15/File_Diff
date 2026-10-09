#!/bin/bash

# File Comparison System - Development Startup Script
# This script starts the complete development environment

set -e

echo "🚀 Starting File Comparison System - Development Environment"
echo "=========================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker first."
    exit 1
fi

# Check if we're in the correct directory
if [ ! -f "docker-compose.yml" ]; then
    print_error "Please run this script from the integration directory."
    exit 1
fi

# Create necessary directories
print_status "Creating storage directories..."
mkdir -p storage/{uploads,processed,exports}
mkdir -p logs

# Copy environment file if it doesn't exist
if [ ! -f "../backend/.env" ]; then
    print_status "Setting up backend environment..."
    cp config/.env ../backend/.env
    print_success "Backend environment file created."
fi

# Build and start services
print_status "Building Docker images..."
docker-compose build

print_status "Starting services..."
docker-compose up -d

# Wait for services to be ready
print_status "Waiting for services to be ready..."
sleep 10

# Check service health
print_status "Checking service health..."

# Check backend health
if curl -f http://localhost:8000/api/health > /dev/null 2>&1; then
    print_success "Backend is healthy and running on http://localhost:8000"
else
    print_warning "Backend might still be starting up..."
fi

# Check frontend
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    print_success "Frontend is running on http://localhost:3000"
else
    print_warning "Frontend might still be starting up..."
fi

# Check Redis
if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    print_success "Redis is running and connected"
else
    print_warning "Redis might not be ready yet..."
fi

echo ""
echo "=========================================================="
print_success "🎉 File Comparison System is starting up!"
echo ""
echo "📍 Access Points:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"
echo ""
echo "🔧 Development Commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart services: docker-compose restart"
echo "   Backend shell: docker-compose exec backend bash"
echo ""
echo "📁 Storage Directory: $(pwd)/storage"
echo "📋 Logs Directory: $(pwd)/logs"
echo ""
print_status "Services are starting... Please wait a moment for full initialization."
echo "=========================================================="