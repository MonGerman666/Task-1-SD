import sys
import os
import re
import statistics
import matplotlib.pyplot as plt

def extract_times_from_log(filepath, pattern=r"Temps:\s*([0-9.]+)s"):
    """
    Llegeix el fitxer de log i extreu tots els valors numèrics que apareixen després de "Temps:".
    Retorna una llista de floats.
    """
    times = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.search(pattern, line)
                if match:
                    try:
                        times.append(float(match.group(1)))
                    except ValueError:
                        continue
    except Exception as e:
        print(f"Error llegint {filepath}: {e}")
    return times

def compute_statistics(times):
    """
    Calcula estadístiques bàsiques d'una llista de temps.
    Retorna un diccionari amb count, mean, min, max i stdev.
    """
    if not times:
        return None
    stats = {
        "count": len(times),
        "mean": statistics.mean(times),
        "min": min(times),
        "max": max(times),
        "stdev": statistics.stdev(times) if len(times) > 1 else 0
    }
    return stats

def plot_histogram(times, title, output_filename):
    """
    Genera i desa un histograma de la llista de temps.
    """
    plt.figure(figsize=(8, 6))
    plt.hist(times, bins=20, edgecolor='black')
    plt.xlabel("Temps de resposta (s)")
    plt.ylabel("Freqüència")
    plt.title(title)
    plt.savefig(output_filename)
    plt.show()

def main():
    if len(sys.argv) < 2:
        print("Ús: python extract_log_stats.py <log_file1> [<log_file2> ...]")
        sys.exit(1)

    for filepath in sys.argv[1:]:
        if not os.path.exists(filepath):
            print(f"El fitxer {filepath} no existeix.")
            continue

        times = extract_times_from_log(filepath)
        stats = compute_statistics(times)
        print(f"\nEstadístiques per {filepath}:")
        if stats:
            print(f"  Nombre d'entrades: {stats['count']}")
            print(f"  Temps mitjà: {stats['mean']:.4f} s")
            print(f"  Temps mínim: {stats['min']:.4f} s")
            print(f"  Temps màxim: {stats['max']:.4f} s")
            print(f"  Desviació estàndard: {stats['stdev']:.4f} s")
            hist_title = f"Distribució del temps ({os.path.basename(filepath)})"
            hist_output = os.path.splitext(filepath)[0] + "_histogram.png"
            plot_histogram(times, hist_title, hist_output)
        else:
            print("  No s'han trobat dades de temps.")

if __name__ == "__main__":
    main()
