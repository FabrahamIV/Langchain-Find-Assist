import os
from app.agents.agents_chat_graph import app_graph
from app.agents.agents_state import ChatState
import traceback

def test():
    state: ChatState = {
        "message": "hallo",
        "file_path": "data/policies/health_policy_premium.pdf",
    }
    print("Invoking graph...")
    try:
        result = app_graph.invoke(state)
        print("Success:", result.keys())
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test()
