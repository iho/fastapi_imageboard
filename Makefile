run:
	uvicorn backend:app --reload

db:
	@echo "Started creation..."
	@psql -c "CREATE USER fastapi WITH PASSWORD 'fastapi';"
	@psql -c "CREATE DATABASE fastdb WITH OWNER fastapi;"
	@echo "Done"

