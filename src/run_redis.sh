#!/bin/bash
# Script per executar totes les proves per Redis (InsultService i InsultFilter)
# Nota: Redis ha d'estar en execució com a servei extern.

echo "=== REDIS TESTS ==="

# --- InsultService Redis ---
echo "[Redis] Iniciant servei InsultService (script)..."
python src/redis/insult_service_redis.py > redis_service.log 2>&1 &
REDIS_SERVICE_PID=$!
sleep 3

echo "[Redis] Executant client bàsic d'InsultService..."
python src/redis/client_insult_service_redis.py > redis_client.log 2>&1

# --- InsultFilter Redis ---
echo "[Redis] Iniciant servei InsultFilter (script)..."
python src/redis/insult_filter_redis.py > redis_filter_service.log 2>&1 &
REDIS_FILTER_PID=$!
sleep 3

echo "[Redis] Executant client bàsic d'InsultFilter..."
python src/redis/client_insult_filter_redis.py > redis_filter_client.log 2>&1

# Atura els serveis (només els scripts que hem iniciat; el servidor Redis extern no s'atura)
kill $REDIS_SERVICE_PID
kill $REDIS_FILTER_PID
echo "[Redis] Tests completats. Logs generats: redis_service.log, redis_client.log, redis_filter_service.log, redis_filter_client.log"
