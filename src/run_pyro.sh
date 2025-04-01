#!/bin/bash

echo "=== PYRO TESTS ==="

LOG_DIR="logs"
mkdir -p "$LOG_DIR"

PYRO_NS_LOG="$LOG_DIR/pyro_nameserver.log"
PYRO_SERVICE_LOG="$LOG_DIR/pyro_service.log"
PYRO_CLIENT_LOG="$LOG_DIR/pyro_client.log"
PYRO_STRESS_LOG="$LOG_DIR/pyro_stress_service.log"
PYRO_FILTER_SERVICE_LOG="$LOG_DIR/pyro_filter_service.log"
PYRO_FILTER_CLIENT_LOG="$LOG_DIR/pyro_filter_client.log"

# Comprovar comandes essencials
check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo "[ERROR] Comanda '$1' no està instal·lada. Cal instal·lar-la per continuar."
        exit 1
    fi
}
check_command python

# Iniciar Name Server
echo "[Pyro] Iniciant Name Server..."
(pyro4-ns > "$PYRO_NS_LOG" 2>&1) &
NS_PID=$!
sleep 1

# Iniciar InsultService
echo "[Pyro] Iniciant servidor InsultService..."
(python src/pyro/insult_service_pyro.py > "$PYRO_SERVICE_LOG" 2>&1) &
SERVICE_PID=$!
sleep 1

# Client bàsic
echo "[Pyro] Executant client bàsic d'InsultService..."
python src/pyro/client_insult_service_pyro.py > "$PYRO_CLIENT_LOG" 2>&1

# Stress test
echo "[Pyro] Executant stress test d'InsultService..."
python src/pyro/stress_test_insult_service_pyro.py > "$PYRO_STRESS_LOG" 2>&1

# Iniciar InsultFilter
echo "[Pyro] Iniciant servidor InsultFilter..."
(python src/pyro/insult_filter_pyro.py > "$PYRO_FILTER_SERVICE_LOG" 2>&1) &
FILTER_PID=$!
sleep 1

# Client d'InsultFilter
echo "[Pyro] Executant client bàsic d'InsultFilter..."
python src/pyro/client_insult_filter_pyro.py > "$PYRO_FILTER_CLIENT_LOG" 2>&1

# Aturar processos
echo "[Pyro] Aturant processos..."
kill "$NS_PID" 2>/dev/null
kill "$SERVICE_PID" 2>/dev/null
kill "$FILTER_PID" 2>/dev/null

echo "[Pyro] Tests completats. Logs disponibles a la carpeta logs/"
