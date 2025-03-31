#!/bin/bash
# Script mestre per executar tots els tests

echo "=== EXECUCIÓ AUTOMATITZADA DELS TESTS DE TOT EL PROJECTE ==="

echo "Executant XMLRPC..."
./src/run_xmlrpc.sh

echo "Executant Pyro..."
./src/run_pyro.sh

echo "Executant Redis..."
./src/run_redis.sh

echo "Executant RabbitMQ..."
./src/run_rabbitmq.sh

echo "=== TOT EXECUTAT ==="
