import json
import time
from pathlib import Path

# region agent log
def _agent_debug_log(
    hypothesis_id: str,
    location: str,
    message: str,
    data: dict | None = None,
    run_id: str = "pre-fix-1",
    timestamp: float | None = None
) -> None:
    """
    Lightweight debug logger for this AI-assisted debug session.
    Writes NDJSON lines to the session log file without affecting main flow.
    """
    try:
        log_obj = {
            "sessionId": "9f7496",
            "runId": run_id,
            "hypothesisId": hypothesis_id,
            "location": location,
            "message": message,
            "data": data or {},
            "timestamp": int((timestamp or time.time()) * 1000),
        }
        log_path = Path(__file__).resolve().parents[3] / "debug-logs" / "debug-9f7496.log"
        # Auto-create the debug folder if it doesn't exist yet
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(log_obj) + "\n")
        print(f"[Debug Log Success] Log written to {log_path}")
    except Exception as e:
        print(f"[Debug Logger Failed] {e}")

if __name__ == "__main__":
    _agent_debug_log("TEST-1", "self-test", "This is a direct execution test.")