import redis
import time
import csv
import concurrent.futures

INSULTS = [f"insult{i}" for i in range(100)]
HOST = 'localhost'
PORT = 6379
CSV_PATH = "logs/stress_redis_service.csv"

def make_request(insult):
    try:
        r = redis.Redis(host=HOST, port=PORT, decode_responses=True)
        start = time.perf_counter()
        r.rpush("insults", insult)
        result = r.lrange("insults", -1, -1)[0] == insult
        end = time.perf_counter()
        duration = end - start
        return insult, result, round(duration, 4)
    except Exception as e:
        return insult, False, -1

def main():
    print("Iniciant stress test Redis (InsultService)...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(make_request, INSULTS))

    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["insult", "resultat", "temps"])
        writer.writerows(results)

    print(f"Test completat. Resultats a {CSV_PATH}")

if __name__ == "__main__":
    main()
