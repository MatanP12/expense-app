docker build --tag e2e_tests:latests ./e2e_tests
docker network create test_network
docker network connect test_network expense_app-app-1
docker run --network=test_network --rm --name e2e_test e2e_tests:latests
test_exit_code=$?
docker network disconnect test_network expense_app-app-1
docker network rm test_network
exit $test_exit_code