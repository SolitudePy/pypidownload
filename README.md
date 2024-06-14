# Flask Pip Downloader Web App

This Flask web application allows you to download Python packages from PyPI along with their dependencies. It provides a user-friendly interface for selecting packages and managing downloads.

## Features

- **Search and Download**: Search for Python packages by name and download them directly.
- **Dependency Handling**: Automatically resolves and includes package dependencies.
- **Docker Support**: Easily deploy the application using Docker and Docker Compose.

## Docker Deployment

To run the Flask Pip Downloader application in a Docker container:

### Prerequisites

- Docker
- Docker Compose

### Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/SolitudePy/pypidownload.git
   cd pypidownload

2. Build and start the Docker containers:
    ```bash
    docker-compose up --build

3. Access the application:
    Open your web browser and go to http://[ip]:5000 where ip is the host that exposes the docker container port(e.g localhost)
