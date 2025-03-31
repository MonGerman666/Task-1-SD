#!/bin/bash
echo "=== REDIS TESTS ==="

echo "[Redis] Iniciant servei InsultService..."
python src/redis/insult_service_redis.py > redis_service.log 2>&1 &
PID1=$!
sleep 2

echo "[Redis] Executant client bàsic d'InsultService..."
python src/redis/client_insult_service_redis.py > redis_client.log 2>&1

echo "[Redis] Iniciant servei InsultFilter..."
python src/redis/insult_filter_redis.py > redis_filter_service.log 2>&1 &
PID2=$!
sleep 2

echo "[Redis] Executant client bàsic d'InsultFilter..."
python src/redis/client_insult_filter_redis.py > redis_filter_client.log 2>&1

kill $PID1
kill $PID2

echo "[Redis] Tests completats."
