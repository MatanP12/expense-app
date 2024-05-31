
# Build e2e tests image
docker build --tag e2e_tests ./e2e_tests
# create a network and connect the proxy server
docker network create test_network
docker network connect test_network expense_app-proxy-1
# run the test container
docker run --network=test_network --rm --name e2e_test e2e_tests
# get the exit code of docker run(0=tests passed other=tests failed)
test_exit_code=$?
# disconect the proxy server from the network and delete it
docker network disconnect test_network expense_app-proxy-1
docker network rm test_network

exit $test_exit_code