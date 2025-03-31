#!/bin/bash
echo "=== PYRO TESTS ==="

echo "[Pyro] Iniciant Name Server..."
python -m Pyro4.naming > pyro_nameserver.log 2>&1 &
PID_NS=$!
sleep 2

echo "[Pyro] Iniciant servidor InsultService..."
python src/pyro/insult_service_pyro.py > pyro_service.log 2>&1 &
PID1=$!
sleep 2

echo "[Pyro] Executant client bàsic d'InsultService..."
python src/pyro/client_insult_service_pyro.py > pyro_client.log 2>&1

echo "[Pyro] Executant stress test d'InsultService..."
python src/pyro/stress_test_insult_service_pyro.py > pyro_stress_service.log 2>&1

echo "[Pyro] Iniciant servidor InsultFilter..."
python src/pyro/insult_filter_pyro.py > pyro_filter_service.log 2>&1 &
PID2=$!
sleep 2

echo "[Pyro] Executant client bàsic d'InsultFilter..."
python src/pyro/client_insult_filter_pyro.py > pyro_filter_client.log 2>&1

kill $PID1
kill $PID2
kill $PID_NS

echo "[Pyro] Tests completats."
