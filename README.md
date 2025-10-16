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


## Tests

To run the tests after installing the dependencies, run:

```bash
PYTHONPATH=. uv run pytest -v
```

**Important**: The tests drop all the tables in the database before running the tests. So, if you want to run the tests with a clean database, you need to create a new database and set the `DATABASE_URL` environment variable to the new database.

## VSCode Debug

To debug the application, you can use the configurations in the `.vscode` folder.
Using the `Run and Debug` configuration, you can run the application and tests in debug mode.


## API Documentation

The API documentation is available at `http://localhost:8080/docs`. And you can also check the one in json format at `http://localhost:8080/openapi.json`.

There is one already downloaded json file in the `./openapi.json` file.
