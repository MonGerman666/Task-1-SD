#!/bin/bash
# Script per executar totes les proves per RabbitMQ (InsultService i InsultFilter)
# Nota: RabbitMQ ha d'estar en execució com a servei extern.

echo "=== RABBITMQ TESTS ==="

# --- InsultService RabbitMQ ---
echo "[RabbitMQ] Iniciant servidor RPC d'InsultService..."
python src/rabbitmq/insult_service_rabbitmq.py > rabbitmq_service.log 2>&1 &
RABBITMQ_SERVICE_PID=$!
sleep 3

echo "[RabbitMQ] Executant client RPC d'InsultService..."
python src/rabbitmq/client_insult_service_rabbitmq.py > rabbitmq_client.log 2>&1
kill $RABBITMQ_SERVICE_PID

# --- InsultFilter RabbitMQ ---
echo "[RabbitMQ] Iniciant servidor RPC d'InsultFilter..."
python src/rabbitmq/insult_filter_rabbitmq.py > rabbitmq_filter_service.log 2>&1 &
RABBITMQ_FILTER_PID=$!
sleep 3

echo "[RabbitMQ] Executant client RPC d'InsultFilter..."
python src/rabbitmq/client_insult_filter_rabbitmq.py > rabbitmq_filter_client.log 2>&1
kill $RABBITMQ_FILTER_PID

echo "[RabbitMQ] Tests completats. Logs generats: rabbitmq_service.log, rabbitmq_client.log, rabbitmq_filter_service.log, rabbitmq_filter_client.log"
