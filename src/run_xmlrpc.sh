#!/bin/bash
echo "=== XMLRPC TESTS ==="

echo "[XMLRPC] Iniciant servidor InsultService..."
python src/xmlrpc/insult_service_xmlrpc.py > xmlrpc_service.log 2>&1 &
PID1=$!
sleep 2

echo "[XMLRPC] Executant client bàsic..."
python src/xmlrpc/client_insult_service_xmlrpc.py > xmlrpc_client.log 2>&1

echo "[XMLRPC] Executant stress test..."
python src/xmlrpc/stress_test_insult_service_xmlrpc.py > xmlrpc_stress_service.log 2>&1

echo "[XMLRPC] Iniciant servidor InsultFilter..."
python src/xmlrpc/insult_filter_xmlrpc.py > xmlrpc_filter_service.log 2>&1 &
PID2=$!
sleep 2

echo "[XMLRPC] Executant client bàsic d'InsultFilter..."
python src/xmlrpc/client_insult_filter_xmlrpc.py > xmlrpc_filter_client.log 2>&1

kill $PID1
kill $PID2

echo "[XMLRPC] Tests completats."
