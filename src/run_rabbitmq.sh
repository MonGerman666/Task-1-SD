#!/bin/bash
echo "=== RABBITMQ TESTS ==="

echo "[RabbitMQ] Iniciant servidor RPC d'InsultService..."
python src/rabbitmq/insult_service_rabbitmq.py > rabbitmq_service.log 2>&1 &
PID1=$!
sleep 2

echo "[RabbitMQ] Executant client RPC d'InsultService..."
python src/rabbitmq/client_insult_service_rabbitmq.py > rabbitmq_client.log 2>&1

echo "[RabbitMQ] Executant stress test d'InsultService..."
python src/rabbitmq/stress_test_insult_service_rabbitmq.py > rabbitmq_stress_service.log 2>&1

echo "[RabbitMQ] Iniciant servidor RPC d'InsultFilter..."
python src/rabbitmq/insult_filter_rabbitmq.py > rabbitmq_filter_service.log 2>&1 &
PID2=$!
sleep 2

echo "[RabbitMQ] Executant client RPC d'InsultFilter..."
python src/rabbitmq/client_insult_filter_rabbitmq.py > rabbitmq_filter_client.log 2>&1

kill $PID1
kill $PID2

echo "[RabbitMQ] Tests completats."
