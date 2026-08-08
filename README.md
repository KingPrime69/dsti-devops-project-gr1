# DSTI DevOps Project - GROUP 1

## Authors

- Lyna MOUHOUBI - Infrastructure as Code, Docker and Kubernetes
- Quentin RIPOT - Application, automated tests and continuous integration

## Project overview

This project implements a complete DevOps workflow for a REST API developed with FastAPI.

The application provides CRUD operations for managing users and stores its data in PostgreSQL. The project includes automated tests, continuous integration, Infrastructure as Code, Docker containerization and Kubernetes orchestration.

The application can run in three environments:

- An Ubuntu VM created with Vagrant and provisioned with Ansible.
- Docker containers.
- A local Kubernetes cluster created with Minikube.

All environments run locally.

## Work performed

- FastAPI User API with CRUD operations
- PostgreSQL data persistence
- Application and database health check
- Unit, API, configuration and connection tests
- Continuous integration with GitHub Actions
- Ubuntu virtual machine configured with Vagrant
- Docker image creation and Docker Hub publication
- Docker health check
- Kubernetes Deployments and Services
- PersistentVolume and PersistentVolumeClaim
- Kubernetes Secret

## Technologies

| Category | Technology |
|---|---|
| Programming language | Python |
| Web framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Data validation | Pydantic |
| Automated testing | Pytest |
| Continuous integration | GitHub Actions |
| Virtual machine | Vagrant and VirtualBox |
| Provisioning | Ansible |
| Containerization | Docker |
| Image registry | Docker Hub |
| Orchestration | Kubernetes and Minikube |

## Project structure

```text
.
|-- .github/
|   `-- workflows/
|       `-- ci.yml
|-- iac/
|   `-- playbooks/
|       |-- inventory.ini
|       `-- playbook.yml
|-- image/
|   `-- Dockerfile
|-- k8s/
|   |-- postgres_storage.yml
|   |-- postgres.yml
|   `-- userapi.yml
|-- userapi/
|   |-- tests/
|   |-- main.py
|   |-- config.py
|   |-- database.py
|   |-- crud.py
|   |-- models.py
|   |-- schemas.py
|   `-- requirements.txt
|-- .dockerignore
|-- .gitignore
|-- Vagrantfile
`-- README.md
```

The main directories have the following responsibilities:

- `userapi/` contains the FastAPI application and automated tests.
- `.github/workflows/` contains the continuous integration workflow.
- `iac/` contains the Ansible inventory and playbook.
- `image/` contains the Dockerfile.
- `k8s/` contains the Kubernetes manifests.
- `Vagrantfile` defines the Ubuntu virtual machine.
- `.dockerignore` excludes unnecessary files from the Docker build context.

---

# 1. Web application

## Application features

The application is a REST API used to manage users.

A user contains:

- an identifier;
- a username;
- an email address;
- a creation date.

Pydantic validates the submitted data before it is stored in PostgreSQL.

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Check the API and database connection |
| `POST` | `/users` | Create a user |
| `GET` | `/users` | List users |
| `GET` | `/users/{user_id}` | Retrieve a user |
| `PATCH` | `/users/{user_id}` | Update a user |
| `DELETE` | `/users/{user_id}` | Delete a user |

## Health endpoint

`GET /health` checks both the API and PostgreSQL.

When the application is running and PostgreSQL answers, it returns HTTP `200`:

```json
{"status":"healthy"}
```

If PostgreSQL cannot be reached, it returns HTTP `503`:

```json
{"status":"unhealthy"}
```

This endpoint is also used by Ansible, Docker and Kubernetes to verify the application.

## Configuration

The application uses environment variables as its configuration source.

| Variable | Default | Description |
|---|---|---|
| `DB_HOST` | `localhost` | PostgreSQL host |
| `DB_PORT` | `5432` | PostgreSQL port |
| `DB_USER` | `userapi` | PostgreSQL user |
| `DB_NAME` | `userapi` | PostgreSQL database |
| `DB_PASSWORD` | none | Required database password |
| `APP_PORT` | `8000` | Application port |

For local development, the variables can be placed in:

```text
userapi/.env
```

In Docker and Kubernetes, environment variables take precedence over the `.env` file.

The PostgreSQL image uses its own initialization variables:

- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`

These values must match the database configuration used by the application.

## Requirements

The following tools are required depending on the selected environment:

- Git
- Python
- PostgreSQL
- Docker Desktop
- Vagrant
- VirtualBox
- Minikube
- kubectl

---

# 2. Automated tests and continuous integration

## Automated tests

The project contains several test levels:

- unit tests for Pydantic validation;
- API tests for CRUD operations;
- configuration tests;
- PostgreSQL connection test.

### Prepare the Python environment

From the repository root:

```powershell
cd userapi
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Run the complete test suite

A configured PostgreSQL database is required for the connection test.

```powershell
pytest -v
```

The test files can also be executed separately:

```powershell
pytest -v tests/test_unit.py
pytest -v tests/test_api.py
pytest -v tests/test_config.py
pytest -v tests/test_connection.py
```

## Continuous integration

Continuous integration is implemented using GitHub Actions.

The workflow is located in:

```text
.github/workflows/ci.yml
```

It runs automatically:

- when code is pushed to `main`;
- when a pull request targets `main`.

The pipeline:

- Checks out the repository.
- Starts a PostgreSQL 16 service container.
- Installs Python and the application dependencies.
- Executes the complete Pytest suite.
- Builds and publishes the Docker image after successful tests on `main`.

The Docker publication job only runs if the tests pass.

Docker Hub credentials are stored using GitHub Secrets:

```text
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
```

These credentials are not committed to the repository.

---

# 3. Infrastructure as Code with Vagrant and Ansible

## Description

Vagrant creates one Ubuntu 22.04 virtual machine using VirtualBox.

The repository is synchronized with `/vagrant` inside the VM. Ansible provisions the machine and runs the application from this synchronized directory.

The Ansible playbook:

- Installs Python and PostgreSQL.
- Enables and starts PostgreSQL.
- Creates the database and PostgreSQL user.
- Creates a Python virtual environment.
- Installs the application dependencies.
- Creates a systemd service.
- Starts the User API.
- Calls `/health` to validate the deployment.

## Validate the Vagrant configuration

Run from the repository root:

```powershell
vagrant validate
```

Expected result:

```text
Vagrantfile validated successfully.
```

## Create and provision the VM

```powershell
vagrant up --provision
```

For an existing VM, rerun Ansible with:

```powershell
vagrant provision
```

## Verify the VM and services

```powershell
vagrant status
vagrant ssh -c "sudo systemctl is-active postgresql"
vagrant ssh -c "sudo systemctl is-active userapi"
```

The VM should be `running`, and both services should return:

```text
active
```

## Test the application

The application runs on port `8000` inside the VM. Vagrant forwards it to port `8080` on Windows.

```powershell
curl.exe http://localhost:8080/health
curl.exe http://localhost:8080/users
```

## Stop the VM

```powershell
vagrant halt
```

---

# 4. Docker image

## Description

The application is packaged as a Docker image .

The Dockerfile:

1. Creates the "/app" working directory.
2. Installs the Python dependencies.
3. Copies the application source code.
4. Exposes port `8000`.
5. Defines a health check using `/health`.
6. Starts the application with Uvicorn.

The `.dockerignore` file excludes unnecessary files such as virtual environments, caches, secrets and Infrastructure as Code files.

## Docker Hub

The User API image is publicly available at:

[Docker Hub - User API](https://hub.docker.com/r/lynamouhoubi/userapi)

The latest project version is `1.1`.

Pull the image:

```powershell
docker pull lynamouhoubi/userapi:1.1
```

The image can also be built locally:

```powershell
docker build -f image/Dockerfile -t userapi:1.1 .
```

## Run the Docker environment

Create a network:

```powershell
docker network create userapi-network
```

Read the database password:

```powershell
$env:DB_PASSWORD = Read-Host "PostgreSQL password"
```

Start PostgreSQL:

```powershell
docker run -d --name userapi-db `
  --network userapi-network `
  -e "POSTGRES_USER=userapi" `
  -e "POSTGRES_PASSWORD=$env:DB_PASSWORD" `
  -e "POSTGRES_DB=userapi" `
  postgres:16-alpine
```

Check PostgreSQL:

```powershell
docker exec userapi-db pg_isready -U userapi -d userapi
```

Start the application:

```powershell
docker run -d --name userapi-app `
  --network userapi-network `
  -p 8081:8000 `
  -e "DB_HOST=userapi-db" `
  -e "DB_PORT=5432" `
  -e "DB_USER=userapi" `
  -e "DB_PASSWORD=$env:DB_PASSWORD" `
  -e "DB_NAME=userapi" `
  -e "APP_PORT=8000" `
  userapi:1.1
```

## Test the Docker environment

```powershell
curl.exe http://localhost:8081/health
curl.exe http://localhost:8081/users
docker inspect --format="{{.State.Health.Status}}" userapi-app
```

The Docker health status should eventually be:

```text
healthy
```

## Clean the Docker environment

```powershell
docker rm -f userapi-app
docker rm -f userapi-db
docker network rm userapi-network
Remove-Item Env:DB_PASSWORD
```

---

# 5. Kubernetes orchestration

## Description

The application is deployed in a local Kubernetes cluster using Minikube.

The Kubernetes configuration includes:

- one PostgreSQL Deployment;
- one PostgreSQL ClusterIP Service;
- one User API Deployment;
- two User API replicas;
- one User API NodePort Service;
- one PersistentVolume;
- one PersistentVolumeClaim;
- one Kubernetes Secret;


The point of using API replicas is to improve availability. If one pod fails, Kubernetes creates a replacement while the other instance remains available.

## Start Minikube

```powershell
minikube start --driver=docker --cpus=2 --memory=4096
kubectl get nodes
```

The Minikube node should have the status `Ready`.

## Load the application image

The Kubernetes manifest uses the local image `userapi:1.1`.

```powershell
minikube image load userapi:1.1
```

## Create the database Secret

The database password is stored in Kubernetes instead of being written in the manifests.

```powershell
$env:DB_PASSWORD = Read-Host "PostgreSQL password"
kubectl create secret generic database-secret --from-literal="password=$env:DB_PASSWORD"
Remove-Item Env:DB_PASSWORD
```

In our case the secret already exists therefore the result will be: 

```powershell
kubectl get secret database-secret
```

## Deploy the Kubernetes resources

The resources are applied in the following order:

```powershell
kubectl apply -f k8s/postgres_storage.yml
kubectl apply -f k8s/postgres.yml
kubectl rollout status deployment/postgres --timeout=120s
kubectl apply -f k8s/userapi.yml
kubectl rollout status deployment/userapi --timeout=120s
```

## Verify the resources

```powershell
kubectl get pods
kubectl get deployments
kubectl get services
kubectl get pv
kubectl get pvc
```

Expected state:

- PostgreSQL pod: `Running`
- two User API pods: `Running`
- PersistentVolume: `Bound`
- PersistentVolumeClaim: `Bound`

## Test the application

Create a temporary connection:

```powershell
kubectl port-forward service/userapi-service 8082:8000
```

Keep this terminal open.

In a second PowerShell terminal:

```powershell
curl.exe http://localhost:8082/health
curl.exe http://localhost:8082/users
```

Stop the port-forward with `Ctrl+C`.

Stop Minikube after the tests:

```powershell
minikube stop
```

---


# 6. AI usage

Artificial intelligence tools were used to assist with:

- troubleshooting configuration errors;
- reviewing command syntax;
- improving the project documentation.
