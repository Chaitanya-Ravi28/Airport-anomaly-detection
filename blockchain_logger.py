import json, hashlib, uuid
from datetime import datetime
from pathlib import Path

HOME = Path.home()

# INPUT FILES (all anomaly outputs) 
FILES = {
    "video": str(HOME / "Video_analysis+IOT/outputs/video_anomalies.json"),
    "iot": str(HOME / "Video_analysis+IOT/outputs/iot_anomalies.json"),
    "prohibited": str(HOME / "CLCXray_yolo/outputs/prohibited_items.json"),
}

LEDGER_PATH = HOME / "security_ledger.json"

#HELPER FUNCTIONS 
def sha256_hex(s: str):
    return hashlib.sha256(s.encode()).hexdigest()

def load_json(path):
    """Load JSON safely and return list of entries."""
    p = Path(path)
    if not p.exists():
        print(f"⚠️ Missing: {p}")
        return []
    try:
        with open(p) as f:
            data = json.load(f)
        return data if isinstance(data, list) else [data]
    except Exception as e:
        print(f"❌ JSON read error in {p}: {e}")
        return []

def extract_type(entry):
    """Extract anomaly or class label."""
    for key in ["anomaly_type", "item_class", "class", "label", "type", "name"]:
        if key in entry:
            return str(entry[key])
    return "unknown"

#BLOCKCHAIN BUILDING 
def collect_all_events():
    events = []
    for src, file_path in FILES.items():
        records = load_json(file_path)
        for r in records:
            events.append({
                "event_id": str(uuid.uuid4()),
                "timestamp": r.get("timestamp", datetime.utcnow().isoformat() + "Z"),
                "source": src,
                "anomaly_type": extract_type(r),
                "anomaly_score": float(r.get("anomaly_score", r.get("confidence", 0.0))),
                "details": r.get("details", "Detected anomaly")
            })
    return sorted(events, key=lambda x: x["timestamp"])

def make_block(index, prev_hash, event):
    block = {
        "index": index,
        "event_id": event["event_id"],
        "timestamp": event["timestamp"],
        "source": event["source"],
        "anomaly_type": event["anomaly_type"],
        "anomaly_score": event["anomaly_score"],
        "details": event["details"],
        "prev_hash": prev_hash,
    }
    block["hash"] = sha256_hex(json.dumps(block, sort_keys=True))
    return block

def build_chain(events):
    chain = []
    prev_hash = "0"

    for i, e in enumerate(events, 1):
        block = make_block(i, prev_hash, e)
        chain.append(block)
        prev_hash = block["hash"]

    return chain

def save_ledger(chain):
    with open(LEDGER_PATH, "w") as f:
        json.dump(chain, f, indent=4)
    print(f"✅ Ledger saved → {LEDGER_PATH} ({len(chain)} blocks)")

def build_and_save_ledger(rebuild=True):
    events = collect_all_events()
    if not events:
        print("⚠️ No anomalies found.")
        return []

    if rebuild:
        chain = build_chain(events)
    else:
        old = load_json(LEDGER_PATH)
        chain = old + build_chain(events)

    save_ledger(chain)
    return chain
