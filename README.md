# Membership Management

## Project Description

This project is a **Membership Management** system developed in Python using FastAPI.

We use [uv](https://docs.astral.sh/uv/) as package manager.

## Setup

1. Install [uv](https://docs.astral.sh/uv/) if you don’t have it yet.
2. Install the dependencies with `uv sync`.
3. Install [docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/) then run `docker-compose -f docker-compose-dev.yml up -d` to start the database.
4. Create a `.env` file in the root directory with the following content:
```bash
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5440/membership
```
5. Then after the database is up and the dependencies are installed, run `uv run alembic upgrade head` to upgrade the database.
6. Run the app with `uv run fastapi dev`.

## Pre-Commit

We use [pre-commit](https://pre-commit.com/) to keep code clean.

Install the hooks after cloning the repository and setting up the environment:

```bash
uv run pre-commit install
```

Run checks on all files:

```bash
uv run pre-commit run --all-files
```
