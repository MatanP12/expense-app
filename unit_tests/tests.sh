docker build --tag unit_tests:latests ./unit_tests
docker run --rm --name unit_test unit_tests:latests