import json
import os
import time
import statistics
from datetime import datetime, UTC

LEDGER_PATH = "security_ledger_test_analysis.json"


def log_event(event):
    """Simulate blockchain ledger logging"""
    with open(LEDGER_PATH, "a") as f:
        f.write(json.dumps(event) + "\n")


def measure_latency(num_trials=100):
    """Measure latency for logging events"""

    latencies = []

    for i in range(num_trials):

        event = {
            "event_id": i,
            "timestamp": datetime.now(UTC).isoformat(),
            "status": "TEST_EVENT",
            "risk_score": 0.5
        }

        start = time.perf_counter()

        log_event(event)

        end = time.perf_counter()

        latencies.append(end - start)

    avg_latency = statistics.mean(latencies)
    std_latency = statistics.stdev(latencies)

    return avg_latency, std_latency


def measure_throughput(num_events=1000):
    """Measure transactions per second"""

    start = time.perf_counter()

    for i in range(num_events):

        event = {
            "event_id": i,
            "timestamp": datetime.now(UTC).isoformat(),
            "status": "TEST_EVENT",
            "risk_score": 0.5
        }

        log_event(event)

    end = time.perf_counter()

    total_time = end - start

    tps = num_events / total_time

    return tps


def measure_storage(num_events=1000):
    """Measure storage cost per event"""

    if os.path.exists(LEDGER_PATH):
        os.remove(LEDGER_PATH)

    for i in range(num_events):

        event = {
            "event_id": i,
            "timestamp": datetime.now(UTC).isoformat(),
            "status": "TEST_EVENT",
            "risk_score": 0.5
        }

        log_event(event)

    file_size = os.path.getsize(LEDGER_PATH)

    storage_per_event = file_size / num_events

    return file_size, storage_per_event


if __name__ == "__main__":

    print("\n------ Blockchain Quantitative Analysis ------\n")

    latency_avg, latency_std = measure_latency()

    print(f"Average Logging Latency: {latency_avg*1000:.3f} ms")
    print(f"Latency Std Deviation: {latency_std*1000:.3f} ms")

    throughput = measure_throughput()

    print(f"Throughput: {throughput:.2f} transactions/sec")

    file_size, storage_per_event = measure_storage()

    print(f"Ledger File Size: {file_size} bytes")
    print(f"Storage Per Event: {storage_per_event:.2f} bytes")

    print("\n----------------------------------------------")