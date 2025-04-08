# Docker Configuration Guide

Author: [Alexis Faure](https://github.com/faurealexis)

This document details the Docker configuration for the Flask Todo App, including container architecture, networking, and security measures.

## Architecture Overview

The application uses a three-container architecture:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    Nginx    │ --> │  Flask App  │ --> │   MariaDB   │
└─────────────┘     └─────────────┘     └─────────────┘
     80/443           Port 5000         Port 3306
   (Frontend)     (App + Gunicorn)     (Database)
```

### Network Isolation
- `frontend` network: Nginx <-> Flask App
- `backend` network: Flask App <-> MariaDB
- Internal network for backend services

## Container Specifications

### Flask Application (app)
- Base: Python 3.11 slim
- Multi-stage build for smaller image
- Non-root user: appuser (UID 1000)
- Resource limits:
  - CPU: 0.5 cores
  - Memory: 512MB
- Health check: HTTP GET /health
- Gunicorn with 4 workers

### MariaDB Database (db)
- Base: MariaDB 10.11
- Persistent volume for data
- Custom configuration for performance
- Resource limits:
  - CPU: 0.5 cores
  - Memory: 512MB
- Health check: mysqladmin ping

### Nginx Reverse Proxy (nginx)
- Base: Nginx 1.25 Alpine
- Non-root user: nginx (UID 1000)
- Static file serving
- Resource limits:
  - CPU: 0.25 cores
  - Memory: 256MB
- Health check: HTTP GET /health

## Security Measures

1. Container Security
   - Non-root users in all containers
   - Read-only root filesystem where possible
   - Limited capabilities
   - Resource constraints
   - Health checks for monitoring

2. Network Security
   - Internal backend network
   - Exposed ports minimization
   - TLS termination at Nginx
   - Security headers configured

3. Data Security
   - Encrypted environment variables
   - Secure volume permissions
   - Regular backups
   - MariaDB security hardening

## Configuration Files

### docker-compose.yml
```yaml
version: '3.8'
services:
  app:
    build: ./app
    networks: [backend, frontend]
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
  db:
    build: ./db
    networks: [backend]
    volumes:
      - db_data:/var/lib/mysql
  nginx:
    build: ./nginx
    networks: [frontend]
    ports:
      - "80:80"
```

### Environment Variables
Required variables in `.env`:
```
MYSQL_DATABASE=todo
MYSQL_USER=todo
MYSQL_PASSWORD=<secure-password>
MYSQL_ROOT_PASSWORD=<secure-root-password>
SECRET_KEY=<flask-secret-key>
```

## Volume Management

1. Database Volume
   - Location: `/var/lib/mysql`
   - Backup schedule: Daily at 3 AM
   - Retention: 7 days

2. Static Files
   - Mounted read-only in Nginx
   - Location: `/app/static`

## Logging Configuration

All containers use json-file driver with limits:
- Max size: 10MB
- Max files: 3

## Performance Tuning

1. MariaDB
   - InnoDB buffer pool: 256MB
   - Query cache: 32MB
   - Connection limits: 100

2. Nginx
   - Worker connections: 1024
   - Gzip compression
   - File descriptor cache
   - Keepalive connections

3. Flask/Gunicorn
   - Workers: 4
   - Timeout: 60s
   - Keep-alive: 5s

## Deployment

1. Build images:
```bash
docker compose build
```

2. Start services:
```bash
docker compose up -d
```

3. View logs:
```bash
docker compose logs -f
```

4. Scale services:
```bash
docker compose up -d --scale app=2
```

## Monitoring

1. Container Health
```bash
docker compose ps
docker compose top
```

2. Resource Usage
```bash
docker stats
```

3. Logs
```bash
docker compose logs -f [service]
```

## Troubleshooting

1. Container won't start:
```bash
docker compose logs <service>
docker inspect <container>
```

2. Database connection issues:
```bash
docker compose exec db mysql -u root -p
docker compose exec app ping db
```

3. Nginx errors:
```bash
docker compose exec nginx nginx -t
docker compose logs nginx
```

## Maintenance

1. Update images:
```bash
docker compose pull
docker compose up -d
```

2. Backup database:
```bash
./backup.sh
```

3. Clean up:
```bash
docker compose down --volumes --remove-orphans
docker system prune
```

## Best Practices

1. Image Building
   - Use multi-stage builds
   - Minimize layer count
   - Cache dependencies
   - Regular security updates

2. Security
   - Non-root users
   - Minimal base images
   - Regular vulnerability scanning
   - Proper secret management

3. Resource Management
   - Set resource limits
   - Monitor usage
   - Regular cleanup
   - Optimize cache usage
``` 