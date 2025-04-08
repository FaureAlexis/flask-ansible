# Proxmox Deployment Guide

Author: [Alexis Faure](https://github.com/faurealexis)

This guide details how to deploy the Flask Todo App on Proxmox VE using LXC containers.

## Prerequisites

- Proxmox VE 8.0+
- Debian 12 LXC template downloaded
- Network configured on Proxmox host
- SSH access to Proxmox host

## Container Setup

1. Create a new container:
```bash
pct create 100 local:vztmpl/debian-12-standard_12.2-1_amd64.tar.zst \
  --hostname todo-app \
  --memory 2048 \
  --swap 1024 \
  --cores 2 \
  --net0 name=eth0,bridge=vmbr0,ip=dhcp \
  --storage local-lvm \
  --password yourpassword
```

2. Start the container:
```bash
pct start 100
```

3. Enter the container:
```bash
pct enter 100
```

## System Configuration

1. Update system packages:
```bash
apt update && apt upgrade -y
```

2. Install required packages:
```bash
apt install -y python3 python3-pip python3-venv git mariadb-server nginx
```

3. Configure firewall (if enabled):
```bash
apt install -y ufw
ufw allow ssh
ufw allow http
ufw allow https
ufw enable
```

## Application Deployment

Follow the standard [deployment guide](deployment.md) with these Proxmox-specific considerations:

### Resource Allocation

- Monitor container resources using Proxmox web interface
- Adjust memory/CPU allocation as needed:
```bash
pct set 100 --memory 4096 --swap 2048 --cores 4
```

### Backup Strategy

1. Create container backup:
```bash
vzdump 100 --compress zstd --storage local
```

2. Schedule regular backups in Proxmox:
```bash
# Add to /etc/pve/jobs.cfg
job backup-todo {
    schedule "0 2 * * *"
    type vzdump
    vmid 100
    storage local
    compress zstd
    mode snapshot
    maxfiles 5
}
```

### High Availability

For production environments:

1. Enable HA in Proxmox cluster
2. Add container to HA group:
```bash
ha-manager add vm:100 --group todo-app
```

3. Configure migration settings:
```bash
pct set 100 --onboot 1 --startup order=1
```

## Performance Tuning

### Container Settings

1. CPU limits:
```bash
pct set 100 --cpulimit 4
```

2. I/O priority:
```bash
pct set 100 --ionice 4
```

3. Memory ballooning:
```bash
pct set 100 --balloon 512
```

### Network Configuration

1. VLAN tagging (if needed):
```bash
pct set 100 --net0 name=eth0,bridge=vmbr0,tag=10,ip=dhcp
```

2. Multiple network interfaces:
```bash
pct set 100 --net1 name=eth1,bridge=vmbr1,ip=10.0.0.100/24
```

## Monitoring

1. Container metrics in Proxmox web interface:
- CPU usage
- Memory usage
- Network I/O
- Disk I/O

2. Application-level monitoring:
- Configure logging to external service
- Set up monitoring stack (Prometheus/Grafana)

## Troubleshooting

1. Container won't start:
```bash
# Check logs
pvesh get /nodes/proxmox/lxc/100/status/current
```

2. Network issues:
```bash
# Verify network config
cat /etc/pve/lxc/100.conf
```

3. Resource constraints:
```bash
# Check resource usage
pct status 100
```

## Security Considerations

1. Container isolation:
```bash
pct set 100 --protection 1
pct set 100 --unprivileged 1
```

2. Resource limits:
```bash
pct set 100 --cpulimit 80 --memory 4096 --swap 0
```

3. Network security:
- Use private networks
- Configure firewall rules
- Enable HTTPS

## Maintenance

1. Container updates:
```bash
pct exec 100 -- apt update && apt upgrade -y
```

2. Backup verification:
```bash
# List backups
ls /var/lib/vz/dump/
# Verify backup
vzdump-test /var/lib/vz/dump/vzdump-lxc-100-*.tar
```

3. Performance monitoring:
```bash
# Container stats
pct top 100
```

## Migration

If needed, migrate container to another Proxmox node:

1. Online migration:
```bash
pct migrate 100 target-node --online
```

2. Offline migration:
```bash
pct migrate 100 target-node
```

## Disaster Recovery

1. Restore from backup:
```bash
pct restore 100 /var/lib/vz/dump/vzdump-lxc-100-*.tar --storage local-lvm
```

2. Emergency procedures:
- Keep backup of container config
- Document network settings
- Maintain current backup 