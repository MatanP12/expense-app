docker build --tag e2e_tests:latests ./e2e_tests
docker run --network=expense_app_mongo_network --rm --name e2e_test e2e_tests:latests