# Show help message
[private]
@default:
    just --list

# Install all depends for developing
@install:
    pdm install -G:all
    pre-commit install

# Run tests
@test:
    pytest tests --cov=pyproject --cov-append --cov-report term-missing -v

# Run pre-commit
@lint:
    pre-commit run --all-files

# Run app in docker container
@up:
	docker compose --profile exchange --profile grafana up --build -d

# Stop docker containers
@down:
	docker compose --profile exchange --profile grafana down
