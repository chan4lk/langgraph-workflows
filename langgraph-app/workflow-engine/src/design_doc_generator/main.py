from graph import DesignState, build_graph
from doc_writer import write_docx
from dotenv import load_dotenv

load_dotenv()

def main(topic):
    graph = build_graph()
    result = graph.invoke(DesignState(topic=topic))
    
    filename = write_docx(topic, result["summary"], result["dfd"], result["db_schema"])
    print(f"✅ Document generated: {filename}")

if __name__ == "__main__":
    main("Self learning resuable agent with langgraph and langmem")
