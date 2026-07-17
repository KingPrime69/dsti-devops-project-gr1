# DSTI DevOps Project - GROUP 1

## Configuration

This application uses configuration from the environment variables. This is the source of truth, shared by the app Ansible, Docker and Kubernetes.

| Variable | Default | Description |
|---|---|---|
| `DB_HOST` | `localhost` | PostgreSQL host |
| `DB_PORT` | `5432` | PostgreSQL port |
| `DB_USER` | `userapi` | PostgreSQL user |
| `DB_NAME` | `userapi` | PostgreSQL database |
| `DB_PASSWORD` | none | Required. The app won't start without it. |
| `APP_PORT` | `8000` | Port the API listens on |

In local development, put the variables in `userapi/.env` (git-ignored). In containers and in Kubernetes, environment variables take precedence over that file.

Note: these configure only the client side. The `postgres` image uses its own `POSTGRES_USER`, `POSTGRES_PASSWORD` and `POSTGRES_DB` to initialise the server. Both sets must match.

## Health endpoint

`GET /health` returns `200 {"status": "healthy"}` when the API is up and the DB answers, `503 {"status": "unhealthy"}` otherwise.

## Authors

- Lyna - infrastructure, Docker, Kubernetes
- Quentin - application, tests, CI