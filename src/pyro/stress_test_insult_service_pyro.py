import time
import Pyro4
import threading
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
thread_local = threading.local()

def get_pyro_proxy():
    if not hasattr(thread_local, 'pyro_proxy'):
        ns = Pyro4.locateNS()
        uri = ns.lookup("insult.service")
        thread_local.pyro_proxy = Pyro4.Proxy(uri)
    return thread_local.pyro_proxy

def send_request_pyro(insult):
    start = time.time()
    try:
        proxy = get_pyro_proxy()
        result = proxy.add_insult(insult)
    except Exception as e:
        logging.error("Error en enviar la petició per %s: %s", insult, e)
        result = None
    end = time.time()
    return insult, result, end - start

def stress_test_pyro(num_requests=100, max_workers=10):
    insults = [f"insult{i}" for i in range(num_requests)]
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_insult = {executor.submit(send_request_pyro, insult): insult for insult in insults}
        for future in as_completed(future_to_insult):
            res = future.result()
            results.append(res)
            logging.info("PyRO completat: %s (Resultat: %s, Temps: %.4fs)", res[0], res[1], res[2])
    return results

def main():
    logging.info("Iniciant el test d'estrès PyRO amb %d peticions...", 100)
    results = stress_test_pyro(100, 10)
    total_time = sum(r[2] for r in results if r[2] is not None)
    avg_time = total_time / len(results)
    logging.info("PyRO Temps total: %.4f segons per %d peticions", total_time, len(results))
    logging.info("PyRO Temps mitjà per petició: %.4f segons", avg_time)

if __name__ == "__main__":
    main()
