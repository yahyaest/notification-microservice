# Notification Microservice

## Description

This is a microservice designed to handle notifications in any application. It is built with FastAPI, a lightweight WSGI web application framework, and uses Prisma as an ORM for database interactions.

## Getting Started

### Dependencies

* Python 3.11
* FastAPI
* Prisma
* A suitable database for Prisma (PostgreSQL, MySQL, SQLite, etc.)

### Installing

* Clone the repository
*  ```pip install -r requirements.txt```
*  ```npx prisma init```
*  ```flask run```

### Running with Docker Compose

This service can be run using Docker Compose. Here is an example of the service definition in a `docker-compose.yml` file:

```yaml
notification:
  image: yahyamachat/notification:latest
  container_name: notification
  restart: unless-stopped
  ports:
    - 8001:8000
  depends_on:
    - postgres
  environment:
    - GATEWAY_BASE_URL=$YOUR_GATEWAY_SERVICE_BASE_URL
    - JWT_SECRET=$YOUR_GATEWAY_SERVICE_JWT_SECRET
    - DATABASE_URL=$YOUR_DATABASE_URL
  entrypoint: /app/entrypoint.sh
```

### API Endpoints
* /api/notifications


## Authors
Contributors names and contact info

ex. @Yahya Machat

## Version History
#### 0.2
- Various bug fixes and optimizations
#### 0.1
- Initial Release

## License
This project is licensed under the MIT License - see the LICENSE.md file for details
