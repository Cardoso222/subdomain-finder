import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
from tqdm import tqdm

def check_subdomain(subdomain, domain, results, timeout):
    url = f"http://{subdomain}.{domain}"
    try:
        response = requests.get(url, timeout=timeout / 1000.0)  # Convert milliseconds to seconds
        if response.status_code == 200:
            results.append(f"Subdomain found: {url}")
    except requests.ConnectionError:
        pass
    except requests.Timeout:
        pass

def main():
    if len(sys.argv) != 3:
        print("Usage: python subdomain_finder.py <domain> <timeout_in_ms>")
        sys.exit(1)

    domain = sys.argv[1]
    timeout = float(sys.argv[2])
    subdomains_file = "subdomains.txt" 

    with open(subdomains_file, "r") as file:
        subdomains = [line.strip() for line in file]

    num_threads = 10
    results = []

    with tqdm(total=len(subdomains), desc="Checking subdomains", position=0) as pbar:
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(check_subdomain, subdomain, domain, results, timeout) for subdomain in subdomains]
            
            for future in as_completed(futures):
                pbar.update()

    print("\nResults:")
    for result in results:
        print(result)

if __name__ == "__main__":
    main()
