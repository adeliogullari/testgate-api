# TestGate

### Run Unit Tests
    pytest -p no:cacheprovider

### Autogenerate and Run Migrations
    alembic revision --autogenerate
    alembic upgrade head