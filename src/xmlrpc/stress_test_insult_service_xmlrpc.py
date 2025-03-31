import time
import xmlrpc.client
from concurrent.futures import ThreadPoolExecutor, as_completed

def send_request(insult):
    """
    Envia una petició add_insult per a l'insult donat i mesura el temps de resposta.
    Crea una nova instància de ServerProxy per cada petició per evitar problemes de thread-safety.
    Retorna una tupla: (insult, resultat, temps de resposta).
    """
    start = time.time()
    # Crea una nova instància de proxy per aquest fil
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/RPC2")
    result = proxy.add_insult(insult)
    end = time.time()
    return insult, result, end - start

def stress_test(num_requests=100, max_workers=10):
    """
    Realitza un test d'estrès enviant 'num_requests' peticions de forma concurrent
    utilitzant un ThreadPoolExecutor amb 'max_workers' fils.
    Retorna una llista amb els resultats de cada petició.
    """
    insults = [f"insult{i}" for i in range(num_requests)]
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_insult = {executor.submit(send_request, insult): insult for insult in insults}
        for future in as_completed(future_to_insult):
            try:
                result = future.result()
                results.append(result)
                print(f"Completat: {result[0]} (Resultat: {result[1]}, Temps: {result[2]:.4f}s)", flush=True)
            except Exception as e:
                print(f"Error en {future_to_insult[future]}: {e}", flush=True)
    return results

def main():
    print("Iniciant el test d'estrès amb 100 peticions...", flush=True)
    results = stress_test(num_requests=100, max_workers=10)
    total_time = sum(r[2] for r in results)
    print(f"\nTemps total: {total_time:.4f} segons per {len(results)} peticions", flush=True)

if __name__ == "__main__":
    main()
