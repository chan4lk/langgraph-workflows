import os
import dotenv

# Load environment variables first
dotenv.load_dotenv()

# Now import other modules
from graph import DesignState, build_graph
from doc_writer import write_docx
from utils.mermaid import extract_mermaid_block, save_mermaid_to_png

def main(topic, user_comments):
    graph = build_graph()
    result = graph.invoke(DesignState(topic=topic, user_comments=user_comments))

    mermaid_code = extract_mermaid_block(result["dfd"].content)
    img_path = save_mermaid_to_png(mermaid_code)
    
    filename = write_docx(topic, result["summary"], result["dfd"], result["db_schema"], img_path)
    print(f"✅ Document generated: {filename}")

if __name__ == "__main__":
    topic = input("Enter topic: ")
    user_comments = input("Enter user comments: ")
    main(topic, user_comments)
