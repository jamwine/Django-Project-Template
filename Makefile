# Define variables
PG_USERNAME := admin
DB_NAME := django_demo_db 

build:
	docker compose -f local.yml up --build -d --remove-orphans

up:
	docker compose -f local.yml up -d

down:
	docker compose -f local.yml down

restart:
	@$(MAKE) down
	@$(MAKE) up

backup-db:
	docker compose -f local.yml exec postgres backup

show-backups:
	docker compose -f local.yml exec postgres backups

restore-db:
	docker compose -f local.yml exec postgres restore ${backup_id}

show-logs:
	docker compose -f local.yml logs

show-logs-api:
	docker compose -f local.yml logs api

django-shell:
	docker compose -f local.yml run --rm api python manage.py shell

makemigrations:
	docker compose -f local.yml run --rm api python manage.py makemigrations

migrate:
	docker compose -f local.yml run --rm api python manage.py migrate  --run-syncdb

make-migrate:
	@$(MAKE) makemigrations
	@$(MAKE) migrate

collectstatic:
	docker compose -f local.yml run --rm api python manage.py collectstatic --no-input --clear

superuser:
	docker compose -f local.yml run --rm api python manage.py createsuperuser

down-v:
	docker compose -f local.yml down -v

volume:
	docker volume inspect django-production_local_postgres_data

reset-db:
	@docker compose -f local.yml exec postgres psql --username=$(PG_USERNAME) --dbname=postgres -c "DROP DATABASE IF EXISTS $(DB_NAME);"
	@docker compose -f local.yml exec postgres psql --username=$(PG_USERNAME) --dbname=postgres -c "CREATE DATABASE $(DB_NAME);"
	@$(MAKE) make-migrate

access-db:
	docker compose -f local.yml exec postgres psql --username=${PG_USERNAME} --dbname=${DB_NAME}

terminate-db-sessions:
	docker compose -f local.yml exec postgres psql --username=${PG_USERNAME} --dbname=${DB_NAME} -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'django_demo_db' AND pid <> pg_backend_pid();"

flake8:
	docker compose -f local.yml exec api flake8 .

black-check:
	docker compose -f local.yml exec api black --check --exclude=migrations .

black-diff:
	docker compose -f local.yml exec api black --diff --exclude=migrations .

black:
	docker compose -f local.yml exec api black --exclude=migrations .

isort-check:
	docker compose -f local.yml exec api isort . --check-only --skip venv --skip migrations

isort-diff:
	docker compose -f local.yml exec api isort . --diff --skip venv --skip migrations

isort:
	docker compose -f local.yml exec api isort . --skip venv --skip migrations