COMPOSE=docker compose

db:
	${COMPOSE} up postgres -d

migrate:
	${COMPOSE} up migrate

db-migrate:
	${COMPOSE} up postgres migrate -d