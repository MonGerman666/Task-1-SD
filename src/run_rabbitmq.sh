#!/bin/bash
export PATH="$PATH:/c/Program\ Files/RabbitMQ\ Server/rabbitmq_server-4.0.7/sbin"


echo "=== RABBITMQ TESTS ==="

LOGDIR="logs"
mkdir -p "$LOGDIR"

echo "[INFO] Verificant estat de RabbitMQ (Windows)..."
if ! rabbitmqctl status > "$LOGDIR/rabbitmq_status.log" 2>&1; then
  echo "[ERROR] RabbitMQ no està instal·lat o no està al PATH."
  echo "Si estàs a Windows, comprova que tens RabbitMQ instal·lat i afegeix rabbitmqctl al PATH."
  exit 1
fi

echo "[RabbitMQ] Iniciant servidor RPC d'InsultService..."
python src/rabbitmq/insult_service_rabbitmq.py > "$LOGDIR/rabbitmq_service.log" 2>&1 &
SERVICE_PID=$!
sleep 2

echo "[RabbitMQ] Executant client RPC d'InsultService..."
python src/rabbitmq/client_insult_service_rabbitmq.py > "$LOGDIR/rabbitmq_client.log" 2>&1

echo "[RabbitMQ] Executant stress test d'InsultService..."
python src/rabbitmq/stress_test_insult_service_rabbitmq.py > "$LOGDIR/rabbitmq_stress_service.log" 2>&1

kill $SERVICE_PID 2>/dev/null

echo "[RabbitMQ] Iniciant servidor RPC d'InsultFilter..."
python src/rabbitmq/insult_filter_rabbitmq.py > "$LOGDIR/rabbitmq_filter_service.log" 2>&1 &
FILTER_PID=$!
sleep 2

echo "[RabbitMQ] Executant client RPC d'InsultFilter..."
python src/rabbitmq/client_insult_filter_rabbitmq.py > "$LOGDIR/rabbitmq_filter_client.log" 2>&1

echo "[RabbitMQ] Executant stress test d'InsultFilter..."
python src/rabbitmq/stress_test_insult_filter_rabbitmq.py > "$LOGDIR/rabbitmq_stress_filter.log" 2>&1

echo "[RabbitMQ] Aturant serveis..."
kill $FILTER_PID 2>/dev/null

echo "[RabbitMQ] Tests completats. Logs disponibles a la carpeta logs/"
