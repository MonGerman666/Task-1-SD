#!/bin/bash

echo "=== REDIS TESTS ==="

mkdir -p logs

# Verificar que Redis està actiu amb Python
echo "[INFO] Comprovant si Redis respon al port 6379..."
python -c "import socket; s = socket.socket(); s.settimeout(1); s.connect(('localhost', 6379))" 2>/dev/null

if [ $? -ne 0 ]; then
  echo "[ERROR] Redis no està en execució o no està al port 6379."
  echo "Assegura't que 'redis-server' s'ha iniciat manualment en una altra terminal."
  exit 1
fi

# InsultService
echo "[Redis] Iniciant servei InsultService..."
python src/redis/insult_service_redis.py > logs/redis_service.log 2>&1 &
PID_SERVICE=$!
sleep 1

echo "[Redis] Executant client bàsic d'InsultService..."
python src/redis/client_insult_service_redis.py > logs/redis_client.log 2>&1

echo "[Redis] Executant stress test d’InsultService..."
python src/redis/stress_test_insult_service_redis.py > logs/redis_stress_service.log 2>&1

# InsultFilter
echo "[Redis] Iniciant servei InsultFilter..."
python src/redis/insult_filter_redis.py > logs/redis_filter_service.log 2>&1 &
PID_FILTER=$!
sleep 1

echo "[Redis] Executant client bàsic d'InsultFilter..."
python src/redis/client_insult_filter_redis.py > logs/redis_filter_client.log 2>&1

echo "[Redis] Executant stress test d’InsultFilter..."
python src/redis/stress_test_insult_filter_redis.py > logs/redis_stress_filter_service.log 2>&1

# Finalitzar serveis
echo "[Redis] Aturant serveis..."
kill $PID_SERVICE $PID_FILTER 2>/dev/null

echo "[Redis] Tests completats. Logs disponibles a la carpeta logs/"
