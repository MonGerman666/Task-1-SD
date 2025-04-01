import redis
import time
import csv
import concurrent.futures

INSULTS = [f"insult{i}" for i in range(100)]
FILTERED_WORDS = ["insult13", "insult42", "insult77"]
HOST = 'localhost'
PORT = 6379
CSV_PATH = "logs/stress_redis_filter.csv"

def test_filter(insult):
    try:
        r = redis.Redis(host=HOST, port=PORT, decode_responses=True)
        start = time.perf_counter()
        filtered = insult in FILTERED_WORDS
        result = not filtered
        end = time.perf_counter()
        duration = end - start
        return insult, result, round(duration, 4)
    except Exception:
        return insult, False, -1

def main():
    print("Iniciant stress test Redis (InsultFilter)...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(test_filter, INSULTS))

    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["insult", "acceptat", "temps"])
        writer.writerows(results)

    print(f"Test completat. Resultats a {CSV_PATH}")

if __name__ == "__main__":
    main()
