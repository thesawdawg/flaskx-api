# Flask Dynamic App

## Project Setup

### Prerequisites
- Python 3.12+
- Poetry

### Installation
1. Install Poetry:
```bash
pip install poetry
```

2. Install dependencies:
```bash
poetry install
```

3. Activate virtual environment:
```bash
poetry shell
```

### Database Configuration
The application supports multiple database types:
- SQLite (default)
- MySQL
- PostgreSQL

Configure your database in the `.env` file:

#### SQLite (Default)
- No additional configuration needed
- Database will be created in the current directory as `/database/app_database.db`

#### MySQL Configuration
```
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database_name
```

#### PostgreSQL Configuration
```
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database_name
```

### Database Migrations
Manage database schema using Flask-Migrate:

#### Create a New Migration
```bash
poetry run flask db migrate -m "Description of changes"
```

#### Apply Migrations
```bash
poetry run flask db upgrade
```

#### Rollback Last Migration
```bash
poetry run flask db downgrade
```

### Running the Application
```bash
poetry run python app.py
```

### API Documentation
Access Swagger UI at: `http://localhost:5000/api/v1/`

### Development
- Use `poetry add` to install new packages
- Use `poetry add --group dev` for development dependencies

### Testing
```bash
poetry run pytest
```

### Production Deployment

#### Environment Configuration
1. Create a `production.env` file with your production settings
2. Set environment variables:
```bash
export FLASK_ENV=production
export FLASK_APP=run.py
```

#### Recommended Production Setup
1. Use a production WSGI server like Gunicorn:
```bash
poetry run pip install gunicorn
poetry run gunicorn -w 4 -b 0.0.0.0:5000 'app:create_app()'
```

2. Use a reverse proxy like Nginx
3. Set up a process manager like Supervisor or systemd

#### Security Recommendations
- Use a strong, unique `PRODUCTION_SECRET_KEY`
- Always use HTTPS
- Regularly update dependencies
- Use PostgreSQL for production databases
- Implement proper logging and monitoring

#### Database Migrations
```bash
poetry run flask db upgrade
```

#### Performance Optimization
- Use connection pooling
- Enable database query caching
- Implement proper indexing
