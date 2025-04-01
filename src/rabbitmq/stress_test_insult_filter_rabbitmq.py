import logging
import csv
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from client_insult_filter_rabbitmq import InsultFilterRpcClient

# Configuració
os.makedirs("logs", exist_ok=True)
log_file = "logs/rabbitmq_stress_filter.log"
csv_file = "logs/rabbitmq_stress_filter.csv"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

NUM_CLIENTS = 10
NUM_REQUESTS = 100

def filter_insult(index):
    client = InsultFilterRpcClient()
    insult = f"insult{index}"
    start_time = time.time()
    try:
        result = client.call("is_insult", insult)
        elapsed = time.time() - start_time
        logging.info(f"Filtrat: {insult} (És insult?: {result}, Temps: {elapsed:.4f}s)")
        return {"id": insult, "result": result, "time": elapsed}
    except Exception as e:
        elapsed = time.time() - start_time
        logging.error(f"Error en filtrar {insult}: {e}")
        return {"id": insult, "result": None, "time": elapsed}

def run_filter_stress_test():
    logging.info(f"Iniciant test d'estrès d'InsultFilter RabbitMQ amb {NUM_REQUESTS} peticions i {NUM_CLIENTS} clients...")
    results = []
    with ThreadPoolExecutor(max_workers=NUM_CLIENTS) as executor:
        futures = [executor.submit(filter_insult, i) for i in range(NUM_REQUESTS)]
        for future in as_completed(futures):
            results.append(future.result())

    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "result", "time"])
        writer.writeheader()
        for r in results:
            writer.writerow(r)

    avg_time = sum(r["time"] for r in results) / len(results)
    total_time = sum(r["time"] for r in results)
    logging.info(f"Temps total: {total_time:.4f} segons per {NUM_REQUESTS} peticions")
    logging.info(f"Temps mitjà per petició: {avg_time:.4f} segons")

if __name__ == "__main__":
    run_filter_stress_test()
