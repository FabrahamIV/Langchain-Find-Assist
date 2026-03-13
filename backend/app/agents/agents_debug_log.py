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
            "timestamp": int(time.time() * 1000),
        }
        log_path = Path(__file__).resolve().parents[3] / "debug" / "debug-9f7496.log"
        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(log_obj) + "\n")
    except Exception:
        # Never allow logging failures to break the main processing flow.
        pass