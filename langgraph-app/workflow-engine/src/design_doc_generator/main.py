from graph import DesignState, build_graph
from doc_writer import write_docx
from dotenv import load_dotenv
from utils.mermaid import extract_mermaid_block, save_mermaid_to_png
load_dotenv()

def main(topic):
    graph = build_graph()
    result = graph.invoke(DesignState(topic=topic))

    mermaid_code = extract_mermaid_block(result["dfd"].content)
    img_path = save_mermaid_to_png(mermaid_code)
    
    filename = write_docx(topic, result["summary"], result["dfd"], result["db_schema"], img_path)
    print(f"✅ Document generated: {filename}")

if __name__ == "__main__":
    main("Self learning resuable agent with langgraph and langmem")
