# Deployment Documentation

Author: [Alexis Faure](https://github.com/faurealexis)

This document describes the deployment process for the Flask Todo App using Ansible.

## Prerequisites

- Ansible 2.9+ installed on your control machine
- SSH access to target servers
- Python 3.9+ installed on target servers
- Target servers running Debian 12
- Sudo access on target servers

## Architecture

The production deployment consists of:

- Nginx as reverse proxy
- Gunicorn as WSGI server
- MariaDB as database
- Systemd service for application management
- Python virtual environment for dependencies

## Configuration

### Inventory Setup

1. Create your inventory file at `ansible/inventory/hosts.ini`:

```ini
[webservers]
web1 ansible_host=your-server-ip ansible_user=your-ssh-user

[dbservers]
db1 ansible_host=your-db-server-ip ansible_user=your-ssh-user

[all:vars]
ansible_python_interpreter=/usr/bin/python3
```

### Variables Configuration

1. Configure common variables in `ansible/inventory/group_vars/all.yml`:

```yaml
app_name: todo
app_user: todo
app_group: todo
app_home: /opt/todo
app_env: production
app_port: 8000

# Python settings
python_version: "3.9"
venv_path: "{{ app_home }}/venv"

# Git settings
repo_url: your-repo-url
repo_version: main

# Gunicorn settings
gunicorn_workers: 3
gunicorn_bind: "127.0.0.1:{{ app_port }}"
```

2. Configure production-specific variables in `ansible/inventory/group_vars/production.yml`:

```yaml
# Database settings
db_name: todo
db_user: todo
db_password: your-secure-password
db_host: localhost

# Flask settings
flask_secret_key: your-secure-secret-key
flask_env: production

# Nginx settings
server_name: your-domain.com
```

## Deployment Process

1. Verify connectivity:
```bash
ansible all -i inventory/hosts.ini -m ping
```

2. Deploy the application:
```bash
ansible-playbook -i inventory/hosts.ini playbooks/site.yml
```

### Available Playbooks

- `site.yml`: Complete deployment
- `deploy.yml`: Application code update only
- `rollback.yml`: Rollback to previous version

## Role Structure

### Common Role
- System dependencies
- Python setup
- Application user/group creation

### MariaDB Role
- Database installation
- Database creation
- User setup
- Secure installation

### Flask App Role
- Code deployment
- Virtual environment setup
- Dependencies installation
- Environment configuration
- Gunicorn setup
- Systemd service configuration

### Nginx Role
- Nginx installation
- Site configuration
- SSL setup (optional)
- Reverse proxy configuration

## Monitoring

The application can be monitored through:

- Systemd service status
- Nginx access/error logs
- Application logs
- MariaDB logs

## Backup

Database backups should be configured through:

1. Daily automated backups
2. Manual backup before deployments
3. Backup verification process

## Security

The deployment includes:

- Secure MariaDB installation
- Firewall configuration
- SSL/TLS setup
- Secure file permissions
- Environment-based secrets management

## Troubleshooting

Common issues and solutions:

1. **Application not starting:**
   - Check systemd service status
   - Verify log files
   - Ensure correct permissions

2. **Database connection issues:**
   - Verify MariaDB service status
   - Check connection credentials
   - Validate network connectivity

3. **Nginx errors:**
   - Check nginx configuration
   - Verify log files
   - Ensure correct permissions

## Maintenance

Regular maintenance tasks:

1. Log rotation
2. Database optimization
3. SSL certificate renewal
4. Security updates
5. Backup verification

## Rollback Procedure

To rollback to a previous version:

1. Run the rollback playbook:
```bash
ansible-playbook -i inventory/hosts.ini playbooks/rollback.yml
```

2. Verify application status
3. Check logs for any errors

## Performance Tuning

Key areas for performance optimization:

1. Gunicorn workers configuration
2. Nginx buffer settings
3. MariaDB query optimization
4. Application caching
5. Static file serving 