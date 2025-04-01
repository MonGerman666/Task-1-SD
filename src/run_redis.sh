#!/bin/bash
echo "=== REDIS TESTS ==="

# Comprovem si Redis està instal·lat i actiu
if ! command -v redis-cli >/dev/null 2>&1; then
  echo "[ERROR] Redis no està instal·lat. Instal·la'l abans d'executar aquest script."
  exit 1
fi

if ! redis-cli ping | grep -q PONG; then
  echo "[ERROR] Redis no està actiu. Inicia el servei abans de continuar."
  exit 1
fi

# Execució de serveis i clients
python src/redis/insult_service_redis.py > logs/redis_service.log 2>&1 &
SERVICE_PID=$!
sleep 1
python src/redis/client_insult_service_redis.py > logs/redis_client.log 2>&1
python src/redis/insult_filter_redis.py > logs/redis_filter_service.log 2>&1 &
FILTER_PID=$!
sleep 1
python src/redis/client_insult_filter_redis.py > logs/redis_filter_client.log 2>&1

kill $SERVICE_PID 2>/dev/null
kill $FILTER_PID 2>/dev/null
echo "[Redis] Tests completats."
