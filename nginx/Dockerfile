FROM nginx:1.25-alpine

# Create nginx user
RUN adduser -D -H -u 1000 -s /sbin/nologin nginx

# Copy configuration
COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf

# Create cache directories
RUN mkdir -p /var/cache/nginx && \
    chown -R nginx:nginx /var/cache/nginx && \
    mkdir -p /var/run && \
    chown -R nginx:nginx /var/run

# Switch to non-root user
USER nginx

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/health || exit 1

EXPOSE 80 