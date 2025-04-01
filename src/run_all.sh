#!/bin/bash
echo "=== EXECUCIÓ AUTOMATITZADA DELS TESTS DE TOT EL PROJECTE ==="

echo "Instal·lant dependències..."
pip install -r requirements.txt

mkdir -p logs

echo "Executant XMLRPC..."
bash src/run_xmlrpc.sh

echo "Executant Pyro..."
bash src/run_pyro.sh

echo "Executant Redis..."
bash src/run_redis.sh

echo "Executant RabbitMQ..."
bash src/run_rabbitmq.sh

echo "=== TOT EXECUTAT ==="
