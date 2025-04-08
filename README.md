# Flask Todo App with Ansible Deployment

A modern todo list application built with Flask and deployed using Ansible.

## Author

[Alexis Faure](https://github.com/faurealexis)

## Features

- Create, read, update, and delete todos
- Mark todos as complete/incomplete
- Modern, responsive UI with HTMX for dynamic updates
- SQLite for development, MariaDB for production
- Automated deployment with Ansible

## Local Development Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
cd app
pip install -r requirements.txt
```

3. Set up environment variables (optional):
```bash
echo "SECRET_KEY=your-secret-key" > .env
echo "DATABASE_URL=sqlite:///todos.db" >> .env
```

4. Run the development server:
```bash
python app.py
```

The application will be available at http://localhost:5000

## Production Deployment

The application can be deployed to production using Ansible. See the [deployment documentation](docs/deployment.md) for detailed instructions.

### Prerequisites for Deployment

- Ansible installed on the control machine
- SSH access to target servers
- Python 3.9+ on target servers
- Target servers running Debian 12

### Quick Deployment

1. Configure your inventory in `ansible/inventory/hosts.ini`
2. Set up your variables in `ansible/inventory/group_vars/`
3. Run the deployment:
```bash
cd ansible
ansible-playbook -i inventory/hosts.ini playbooks/site.yml
```

## Project Structure

```
ansible-flask-todoapp/
├── README.md
├── app/
│   ├── app.py              # Main Flask application
│   ├── models.py           # Database models
│   ├── templates/          # Jinja2 templates
│   ├── static/            # CSS, JS, and other static files
│   └── requirements.txt    # Python dependencies
├── ansible/
│   ├── inventory/         # Ansible inventory files
│   ├── roles/            # Ansible roles
│   └── playbooks/        # Ansible playbooks
└── docs/                 # Documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 