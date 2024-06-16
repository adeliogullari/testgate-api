# TestGate

### Run Unit Tests
    pytest -p no:cacheprovider

### Autogenerate and Run Migrations
    alembic revision --autogenerate
    alembic upgrade head

 tox -e py
 
docker run \
    --rm \
    -e SONAR_HOST_URL="http://host.docker.internal:9000" \
    -e SONAR_SCANNER_OPTS="-Dsonar.projectKey=testgate-api -Dproject.settings=./sonar-project.properties" \
    -e SONAR_TOKEN="sqp_44e5d7973b0021efcf39e4e7d4ffcd96126f474e" \
    -v "$(pwd):/usr/src" \
    sonarsource/sonar-scanner-cli

docker build -t getting-started .

docker build -t groot .
docker tag groot:latest groot:staging

Bug in claims verify, you should check
Still one function need in token abstract, check that
Cache are not good, check especially update
Check models 1 more time
Permissions
Documentation

execution --> retrieve_by_name --> Name unique ??