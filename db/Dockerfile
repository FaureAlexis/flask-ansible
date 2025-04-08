FROM mariadb:10.11

# Add custom configuration
COPY mariadb.cnf /etc/mysql/conf.d/

# Add initialization scripts
COPY init.sql /docker-entrypoint-initdb.d/

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD mysqladmin ping -h localhost -u healthcheck --password=$MYSQL_PASSWORD || exit 1

# Set recommended MariaDB configuration
ENV MYSQL_CHARSET=utf8mb4
ENV MYSQL_COLLATION=utf8mb4_unicode_ci 