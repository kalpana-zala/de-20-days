import csv
import json
import logging
import sys
from datetime import date
from pathlib import Path

import requests

URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {
    "latitude": 19.07,
    "longitude": 72.88,
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
    "timezone": "Asia/Kolkata",
}
DATA_DIR = Path("data")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("pipeline.log")],
)
log = logging.getLogger(__name__)


def extract():
    log.info("Calling weather API")
    response = requests.get(URL, params=PARAMS, timeout=30)
    response.raise_for_status()
    return response.json()


def transform(data):
    daily = data["daily"]
    rows = []
    for i in range(len(daily["time"])):
        t_max = daily["temperature_2m_max"][i]
        t_min = daily["temperature_2m_min"][i]
        rows.append({
            "date": daily["time"][i],
            "city": "Mumbai",
            "temp_max_c": t_max,
            "temp_min_c": t_min,
            "temp_avg_c": round((t_max + t_min) / 2, 1),
            "rain_mm": daily["precipitation_sum"][i],
        })
    log.info("Transformed %d rows", len(rows))
    return rows


def load(data, rows):
    run_date = date.today().isoformat()

    raw_dir = DATA_DIR / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_path = raw_dir / f"weather_{run_date}.json"
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    clean_dir = DATA_DIR / "clean"
    clean_dir.mkdir(parents=True, exist_ok=True)
    clean_path = clean_dir / f"weather_{run_date}.csv"
    with open(clean_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    log.info("Saved %s and %s", raw_path, clean_path)


if __name__ == "__main__":
    try:
        data = extract()
        rows = transform(data)
        load(data, rows)
        log.info("Pipeline finished OK")
    except Exception:
        log.exception("Pipeline FAILED")
        sys.exit(1)