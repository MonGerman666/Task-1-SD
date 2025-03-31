#!/bin/bash
echo "=== EXECUCIÓ AUTOMATITZADA DELS TESTS DE TOT EL PROJECTE ==="

echo "Instal·lant dependencies"
pip install -r requirements.txt

echo "Executant XMLRPC..."
./src/run_xmlrpc.sh

echo "Executant Pyro..."
./src/run_pyro.sh

echo "Executant Redis..."
./src/run_redis.sh

echo "Executant RabbitMQ..."
./src/run_rabbitmq.sh

echo "=== TOT EXECUTAT ==="
