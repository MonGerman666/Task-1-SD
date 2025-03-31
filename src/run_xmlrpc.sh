#!/bin/bash
# Script per executar totes les proves per XMLRPC (InsultService i InsultFilter)

echo "=== XMLRPC TESTS ==="

# --- InsultService XMLRPC ---

echo "[XMLRPC] Iniciant servidor InsultService..."
python src/xmlrpc/insult_service_xmlrpc.py > xmlrpc_service.log 2>&1 &
XMLRPC_SERVICE_PID=$!
sleep 3

echo "[XMLRPC] Executant client bàsic (afegir i recuperar insults)..."
python src/xmlrpc/client_insult_service_xmlrpc.py > xmlrpc_client.log 2>&1

echo "[XMLRPC] Executant stress test d'InsultService (connexió reutilitzada)..."
python src/xmlrpc/stress_test_insult_service_xmlrpc_improved.py > xmlrpc_stress_service.log 2>&1

# --- InsultFilter XMLRPC ---

echo "[XMLRPC] Iniciant servidor InsultFilter..."
python src/xmlrpc/insult_filter_xmlrpc.py > xmlrpc_filter_service.log 2>&1 &
XMLRPC_FILTER_PID=$!
sleep 3

echo "[XMLRPC] Executant client bàsic d'InsultFilter..."
python src/xmlrpc/client_insult_filter_xmlrpc.py > xmlrpc_filter_client.log 2>&1

# Nota: si tens scripts de stress test per InsultFilter, els pots afegir aquí.
# Per exemple: python src/xmlrpc/stress_test_insult_filter_xmlrpc_improved.py > xmlrpc_stress_filter.log 2>&1

# Atura els serveis
kill $XMLRPC_SERVICE_PID
kill $XMLRPC_FILTER_PID
echo "[XMLRPC] Tests completats. Logs generats: xmlrpc_service.log, xmlrpc_client.log, xmlrpc_stress_service.log, xmlrpc_filter_service.log, xmlrpc_filter_client.log"
