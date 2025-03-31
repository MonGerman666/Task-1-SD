import time
import Pyro4
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
_thread_local_pyro = threading.local()

def get_pyro_proxy():
    """Crea (o reutilitza) una instància de Pyro4.Proxy per al fil actual."""
    if not hasattr(_thread_local_pyro, "pyro_proxy"):
        ns = Pyro4.locateNS()
        uri = ns.lookup("insult.service")
        _thread_local_pyro.pyro_proxy = Pyro4.Proxy(uri)
    return _thread_local_pyro.pyro_proxy

def send_pyro_request(insult):
    start = time.time()
    try:
        proxy = get_pyro_proxy()
        result = proxy.add_insult(insult)
    except Exception as e:
        logging.error("Pyro error per %s: %s", insult, e)
        result = None
    end = time.time()
    return insult, result, end - start

def stress_test_pyro(num_requests=100, max_workers=10):
    insults = [f"insult{i}" for i in range(num_requests)]
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_insult = {executor.submit(send_pyro_request, insult): insult for insult in insults}
        for future in as_completed(future_to_insult):
            res = future.result()
            results.append(res)
            logging.info("Pyro completat: %s (Resultat: %s, Temps: %.4fs)", res[0], res[1], res[2])
    return results

def main():
    logging.info("Iniciant el test d'estrès Pyro (connexió reutilitzada) amb 100 peticions...")
    results = stress_test_pyro(num_requests=100, max_workers=10)
    total_time = sum(r[2] for r in results if r[2] is not None)
    avg_time = total_time / len(results)
    logging.info("Pyro Temps total: %.4fs per %d peticions", total_time, len(results))
    logging.info("Pyro Temps mitjà per petició: %.4fs", avg_time)

if __name__ == "__main__":
    main()
