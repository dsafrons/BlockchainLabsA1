import requests, csv, os
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime, UTC
from random import uniform


SESSION = requests.Session()
SESSION.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0'
})


def scrape_phishing_banner(address, timeout=15, min_delay=0.7, max_delay=1.5, max_retries=3):
    """
    Returns a dict:
        {"flagged": True|False|None, "status": ""|"undetermined"}
    - flagged=True  -> phishing banner detected
    - flagged=False -> no phishing banner detected
    - flagged=None  -> could not determine (blocked, captcha, non-200, exception)
    """

    sleep(uniform(min_delay, max_delay))

    url = "https://etherscan.io/address/" + address
    backoff_time_extension = 1.0
    for attempt in range(1, max_retries + 1):
        try:
            response = SESSION.get(url, timeout=timeout)
        except requests.RequestException:
            # backoff and retry
            if attempt <= max_retries:
                sleep(backoff_time_extension + uniform(min_delay, max_delay))
                backoff_time_extension *= 2
                continue
            return {"flagged": None, "status": "undetermined"}


        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # quick block/captcha check
            body_text = soup.get_text(" ", strip=True).lower()
            if ("verify you are human" in body_text) or ("captcha" in body_text):
                return {"flagged": None, "status": "undetermined"}

            # phishing alert (Bootstrap danger alert)
            warning = soup.select_one('div.alert.alert-danger[role="alert"]')
            if not warning:
                return {"flagged": False, "status": ""}

            is_phish = ("phish" in warning.get_text(" ", strip=True).lower()
                        or "suspicious" in warning.get_text(" ", strip=True).lower())
            return {"flagged": bool(is_phish), "status": ""}

        # 429/5xx -> backoff and retry
        if response.status_code in (429, 500, 502, 503, 504) and attempt < max_retries:
            sleep(backoff_time_extension + uniform(min_delay, max_delay))
            backoff_time_extension *= 2
            continue

        # other bad status -> give up
        return {"flagged": None, "status": "undetermined"}

    return {"flagged": None, "status": "undetermined"}


def read_addresses_csv(path="addresses.csv"):
    if not os.path.exists(path):
        raise Exception(f"File {path} does not exist in order to read addresses. Please create addresses.csv first.")
    
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()

    addresses = [a.strip() for a in data.split(",") if a.strip()]

    return addresses


def load_existing_results(path="results.csv"):
    """
    Return SET of addresses that have already run successfully
    (status == ""). Addresses with 'undetermined' will NOT be
    considered done and therefore don't return, so the scraper
    will retry them.
    """
    if not os.path.exists(path):
        return set()

    checked_addresses = set()
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            addr = (row.get("address") or "").strip()
            if addr and row.get("status") == "":
                checked_addresses.add(addr)

    return checked_addresses


def write_results(addresses, out_csv="results.csv"):
    FIELDS = ["address", "flagged", "status", "checked_at"]
    existing = load_existing_results()
    addresses_to_check = [a for a in addresses if a not in existing]

    if not addresses_to_check:
        print("No new addresses to check. Results file unchanged.")
        return

    # open in APPEND mode; write header only if new/empty file
    need_header = not os.path.exists(out_csv) or os.path.getsize(out_csv) == 0
    with open(out_csv, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if need_header:
            writer.writeheader()

        for i, addr in enumerate(addresses_to_check, 1):
            res = scrape_phishing_banner(addr)

            row = {
                "address": addr,
                "flagged": res["flagged"],
                "status": res["status"],
                "checked_at": datetime.now(UTC).isoformat(timespec="seconds")
            }
            writer.writerow(row)
            print(f'Finished {i}/{len(addresses_to_check)}, phishing result: {row["flagged"]}')


if __name__ == '__main__':
    write_results(read_addresses_csv())
