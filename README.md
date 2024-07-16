# CUSTOM API



## Table of Contents

- [Introduction](#introduction)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Files and Directories](#files-and-directories)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Provide a brief overview of your project, including its purpose and key features. Mention that this project utilizes FastAPI, Docker, and related technologies.

## Project Structure

Briefly describe the structure of your project. Highlight key files and directories relevant to the project setup and functionality.

## Setup Instructions

### Prerequisites

List prerequisites such as Docker, Python, and any specific versions required to run the project.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/tsuriu/custom_api.git
   cd custom_api
   ```

2. Build and run the Docker containers:

   ```bash
   docker-compose up --build
   ```

   This command builds the Docker image using the Dockerfile and starts the containers defined in `docker-compose.yml`.

## Usage

Describe how to use the project once it's set up. Include any specific commands or steps needed to interact with the application or API.

## Endpoints

### Port Scan Endpoint

#### Description

This endpoint scans a specified host and port using Nmap.

#### Usage

- **Method**: GET
- **URL**: `/api/nmap_custom/`
- **Parameters**:
  - `host` (required): Hostname or IP address to scan.
  - `port` (required): Port number to scan.

#### Example

```bash
curl -X 'GET' \
  'http://localhost:8000/api/nmap_custom/?host=example.com&port=80'
```

### HTTP Custom Agent Endpoint

#### Description

This endpoint fetches HTTP request header details from a specified URL.

#### Usage

- **Method**: GET
- **URL**: `/api/http_custom/`
- **Parameters**:
  - `url` (required): URL to fetch details from.
  - `mode` (optional): Mode of fetching details (`http`, `cert`, `both`). Defaults to `both`.

#### Example

```bash
curl -X 'GET' \
  'http://localhost:8000/api/http_custom/?url=https://example.com&mode=both'
```

## Files and Directories

### Dockerfile

Contains instructions to build the Docker image for the project.

### app/

Contains the main application code and related files.

### docker-compose.yml

Defines services, networks, and volumes for multi-container Docker applications.

### requirements.txt

Lists Python dependencies required by the application.

## Contributing

Explain how others can contribute to your project. Include guidelines for pull requests and reporting issues.

## License

Specify the project's license (e.g., MIT, Apache 2.0).
