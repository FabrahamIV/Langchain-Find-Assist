import os
import sys
import traceback

from app.api.file_upload import app_graph
from app.agents.agents_state import ChatState

def test():
    state: ChatState = {
        "message": "test",
        "file_path": "data/policies/health_policy_premium.pdf",
        "conversation_id": "test_id"
    }
    print("Invoking graph...")
    try:
        result = app_graph.invoke(state)
        print("Success!", result.keys())
        print("Answer:", result.get("answer"))
    except Exception as e:
        with open("error.log", "w") as f:
            traceback.print_exc(file=f)
        print("Error logged to error.log")

if __name__ == "__main__":
    test()
