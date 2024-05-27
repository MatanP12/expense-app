docker build --tag tests:latests ./e2e_tests
docker run --network=expense_app_mongo_network --rm --name test tests:latests app:5000