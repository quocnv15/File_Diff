# File Comparison System - Integration

This directory contains the integration configuration for running the complete File Comparison System with both frontend and backend services.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │     Redis       │
│   (Nginx)       │◄──►│   (FastAPI)     │◄──►│   (Cache)       │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 6379    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Git repository cloned locally

### Start Development Environment

1. **Navigate to integration directory:**
   ```bash
   cd integration
   ```

2. **Start all services:**
   ```bash
   ./scripts/start-dev.sh
   ```

3. **Access the application:**
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs

### Manual Start

If you prefer to start services manually:

```bash
# Create storage directories
mkdir -p storage/{uploads,processed,exports}
mkdir -p logs

# Copy environment configuration
cp config/.env ../backend/.env

# Start services
docker-compose up -d

# View logs
docker-compose logs -f
```

## Project Structure

```
integration/
├── config/
│   └── .env                    # Shared environment configuration
├── docker/
│   └── (future Docker configs)
├── nginx/
│   ├── nginx.conf             # Nginx main configuration
│   └── default.conf           # Nginx site configuration
├── scripts/
│   └── start-dev.sh           # Development startup script
├── storage/                   # Shared storage volume
│   ├── uploads/               # Uploaded files
│   ├── processed/             # Processed files
│   └── exports/               # Generated exports
├── logs/                      # Application logs
├── docker-compose.yml         # Main compose file
└── README.md                  # This file
```

## Services

### Frontend Service
- **Image**: nginx:alpine
- **Port**: 3000
- **Purpose**: Serves the frontend application
- **Configuration**: Nginx reverse proxy

### Backend Service
- **Build**: From `../backend/Dockerfile`
- **Port**: 8000
- **Purpose**: FastAPI backend for file processing
- **Health Check**: `/api/health`

### Redis Service
- **Image**: redis:7-alpine
- **Port**: 6379
- **Purpose**: Caching and session storage
- **Persistence**: Data volume

## Configuration

### Environment Variables
Key configuration options in `config/.env`:

```bash
# Service URLs
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000

# File Storage
MAX_FILE_SIZE_MB=50
FILE_RETENTION_HOURS=24

# Rate Limiting
RATE_LIMIT_UPLOADS=10
RATE_LIMIT_COMPARISONS=20

# Caching
REDIS_URL=redis://localhost:6379/0
```

### Nginx Configuration
- **Static Files**: Served from `/usr/share/nginx/html`
- **API Proxy**: `/api/*` → `http://backend:8000/api/*`
- **File Upload**: Max 50MB
- **Caching**: 1 year for static assets

## Development Workflow

### Making Changes

1. **Frontend Changes**:
   - Edit files in `../frontend/`
   - Changes are reflected immediately (hot reload via volume mount)

2. **Backend Changes**:
   - Edit files in `../backend/`
   - Restart backend service:
     ```bash
     docker-compose restart backend
     ```

3. **Configuration Changes**:
   - Edit `config/.env`
   - Restart affected services

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f redis
```

### Debugging

```bash
# Backend shell access
docker-compose exec backend bash

# Redis CLI
docker-compose exec redis redis-cli

# Nginx configuration test
docker-compose exec frontend nginx -t
```

## Production Deployment

### Environment Setup
1. **Update environment variables**:
   ```bash
   cp config/.env config/.env.production
   # Edit production values
   ```

2. **Build production images**:
   ```bash
   docker-compose -f docker-compose.prod.yml build
   ```

3. **Deploy**:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### SSL/HTTPS Setup
1. **Update Nginx configuration** for SSL
2. **Mount SSL certificates**:
   ```yaml
   volumes:
     - ./ssl/cert.pem:/etc/nginx/ssl/cert.pem
     - ./ssl/key.pem:/etc/nginx/ssl/key.pem
   ```

### Monitoring
- **Health Checks**: Built-in Docker health checks
- **Logs**: Centralized in `logs/` directory
- **Metrics**: Enable via `METRICS_ENABLED=true`

## Troubleshooting

### Common Issues

1. **Port Conflicts**:
   - Ensure ports 3000, 8000, 6379 are available
   - Modify ports in `docker-compose.yml` if needed

2. **Permission Issues**:
   ```bash
   sudo chown -R $USER:$USER storage/
   sudo chown -R $USER:$USER logs/
   ```

3. **Backend Not Starting**:
   ```bash
   docker-compose logs backend
   # Check for missing dependencies or configuration errors
   ```

4. **Frontend Not Loading**:
   ```bash
   docker-compose logs frontend
   # Check Nginx configuration
   ```

5. **Redis Connection Issues**:
   ```bash
   docker-compose exec redis redis-cli ping
   # Should return PONG
   ```

### Cleanup

```bash
# Stop and remove containers
docker-compose down

# Remove volumes (WARNING: This deletes all data)
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

## Performance Tuning

### Backend Optimization
- **Workers**: Adjust `WORKERS` in environment
- **Memory**: Monitor with `docker stats`
- **Database**: Add database for persistence (future)

### Frontend Optimization
- **Caching**: Nginx static file caching
- **Compression**: Gzip enabled by default
- **CDN**: Add CDN for production

### File Processing
- **Queue**: Implement background processing queue
- **Limits**: Adjust rate limits as needed
- **Storage**: Monitor disk usage

## Security

### Network Security
- **CORS**: Configured in backend and Nginx
- **Rate Limiting**: Implemented in backend
- **File Validation**: Multiple validation layers

### Best Practices
- **Secrets**: Use environment variables
- **Updates**: Keep Docker images updated
- **Monitoring**: Log monitoring and alerts

## Support

For issues and questions:
1. Check this README
2. Review service logs
3. Consult individual component documentation:
   - Backend: `../backend/README.md`
   - Frontend: `../frontend/README.md`
   - API: http://localhost:8000/docs