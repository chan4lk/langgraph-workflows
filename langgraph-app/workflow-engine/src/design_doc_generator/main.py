import os
import dotenv

# Load environment variables first
dotenv.load_dotenv()
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
# Now import other modules
from graph import DesignState, build_graph
from doc_writer import write_docx
from utils.mermaid import extract_mermaid_block, save_mermaid_to_png

def main(topic, user_comments):
    graph = build_graph()
    config = {"configurable": {"thread_id": "1"}}
    result = graph.invoke(DesignState(topic=topic, user_comments=user_comments), config=config)

    # checkpoints = list(graph.get_state_history(config))
    # print(checkpoints)

    conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
    memory = SqliteSaver(conn)


    checkpoints = memory.get(config)
    print(checkpoints)
    

    mermaid_code = extract_mermaid_block(result["dfd"].content)
    img_path = save_mermaid_to_png(mermaid_code)
    
    filename = write_docx(topic, result["summary"], result["dfd"], result["db_schema"], img_path)
    print(f"✅ Document generated: {filename}")

if __name__ == "__main__":
    topic = input("Enter topic: ")
    user_comments = input("Enter user comments: ")
    main(topic, user_comments)
