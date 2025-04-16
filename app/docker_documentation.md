# Dockerizing Flask Marketplace

This documentation provides instructions on how to containerize and run the Flask Marketplace application using Docker.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your system
- [Docker Compose](https://docs.docker.com/compose/install/) installed on your system
- Basic knowledge of Docker and containerization

## Project Structure

The Docker configuration consists of the following files:

- `Dockerfile`: Defines how to build the Flask Marketplace application image
- `docker-compose.yml`: Defines the services, networks, and volumes for the application
- `.env.example`: Template for environment variables needed by the application
- `.dockerignore`: Specifies files and directories to exclude from the Docker build context

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Mohamed-Khalil67/Market-Place.git
cd Market-Place
```

### 2. Configure Environment Variables

Create a `.env` file based on the provided `.env.example`:

```bash
cp .env.example .env
```

Edit the `.env` file to set appropriate values for your environment, especially:
- `SECRET_KEY`: Set a secure random string
- Any API keys if you're implementing payment functionality

### 3. Build and Run with Docker Compose

```bash
docker-compose up --build
```

This command will:
1. Build the Docker image for the Flask Marketplace application
2. Start the container
3. Initialize the database
4. Run the application on port 5000

### 4. Access the Application

Once the container is running, you can access the application at:

```
http://localhost:5000
```

### 5. Managing the Application

- To stop the application: Press `Ctrl+C` in the terminal where docker-compose is running
- To run in detached mode: `docker-compose up -d`
- To view logs: `docker-compose logs -f`
- To stop and remove containers: `docker-compose down`

## Data Persistence

The Docker setup is configured to persist data using volumes:

- `./market.db:/app/market.db`: Persists the SQLite database
- `./instance:/app/instance`: Persists the Flask instance folder

This ensures that your data remains intact even if the container is stopped or removed.

## Customization

### Changing the Port

To change the port on which the application is accessible, modify the `ports` section in `docker-compose.yml`:

```yaml
ports:
  - "8080:5000"  # Change 8080 to your desired port
```

### Using a Different Database

By default, the application uses SQLite. To use a different database:

1. Update the `DATABASE_URL` in your `.env` file
2. Modify the `docker-compose.yml` to include the database service
3. Update the application's database configuration in `config.py`

## Production Deployment

For production deployment, consider the following additional steps:

1. Use a production-grade web server like Gunicorn:
   ```
   CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
   ```

2. Set up a reverse proxy like Nginx to handle static files and SSL termination

3. Use environment-specific configuration for different deployment environments

4. Implement proper logging and monitoring

5. Set up database backups

## Troubleshooting

### Container Fails to Start

Check the logs for errors:
```bash
docker-compose logs
```

Common issues include:
- Database initialization failures
- Permission problems
- Environment variable configuration issues

### Database Issues

If you encounter database issues:
1. Ensure the database file has the correct permissions
2. Check that the volume mapping is correct in `docker-compose.yml`
3. Try removing the volume and letting the application create a new database:
   ```bash
   docker-compose down -v
   docker-compose up --build
   ```

### Performance Issues

If the application is slow:
1. Consider using a production WSGI server like Gunicorn
2. Optimize the Docker image by reducing its size
3. Consider using a more powerful database for larger datasets
