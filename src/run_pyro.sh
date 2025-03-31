#!/bin/bash
# Script per executar totes les proves per Pyro (InsultService i InsultFilter)

echo "=== PYRO TESTS ==="

# --- Inici del Name Server (si no està en execució) ---
echo "[Pyro] Iniciant Name Server..."
python -m Pyro4.naming > pyro_nameserver.log 2>&1 &
NS_PID=$!
sleep 3

# --- InsultService Pyro ---

echo "[Pyro] Iniciant servidor InsultService..."
python src/pyro/insult_service_pyro.py > pyro_service.log 2>&1 &
PYRO_SERVICE_PID=$!
sleep 3

echo "[Pyro] Executant client bàsic d'InsultService..."
python src/pyro/client_insult_service_pyro.py > pyro_client.log 2>&1

echo "[Pyro] Executant stress test d'InsultService (connexió reutilitzada)..."
python src/pyro/stress_test_insult_service_pyro_improved.py > pyro_stress_service.log 2>&1

# --- InsultFilter Pyro ---

echo "[Pyro] Iniciant servidor InsultFilter..."
python src/pyro/insult_filter_pyro.py > pyro_filter_service.log 2>&1 &
PYRO_FILTER_PID=$!
sleep 3

echo "[Pyro] Executant client bàsic d'InsultFilter..."
python src/pyro/client_insult_filter_pyro.py > pyro_filter_client.log 2>&1

# Atura els processos de Pyro
kill $PYRO_SERVICE_PID
kill $PYRO_FILTER_PID
kill $NS_PID
echo "[Pyro] Tests completats. Logs generats: pyro_nameserver.log, pyro_service.log, pyro_client.log, pyro_stress_service.log, pyro_filter_service.log, pyro_filter_client.log"
