# ./src/agent/webapp.py
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from smart_goals.graph import make_graph  # Adjust import if you want a different graph
from pydantic import BaseModel
from langchain_core.messages import AIMessageChunk
from langchain_core.runnables import RunnableConfig
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command
from pprint import pprint

class Item(BaseModel):
    thread_id: str
    message: str

app = FastAPI()


@app.get("/hello")
def read_root():
    return {"Hello": "World"}


def is_current_conversation_interrupted(
        graph: CompiledStateGraph, graph_config: RunnableConfig
    ) -> bool:
        """Check if the current conversation state contains any interrupts."""
        current_graph_state = graph.get_state(graph_config)
        interrupt_exists = bool(
            current_graph_state is not None
            and hasattr(current_graph_state, "tasks")
            and current_graph_state.tasks
            and hasattr(current_graph_state.tasks[0], "interrupts")
            and len(current_graph_state.tasks[0].interrupts) > 0
        )
        return interrupt_exists

def event_stream(graph, thread_id, message):
    graph_config = RunnableConfig(configurable={"thread_id": thread_id})
    interrupt_exists = is_current_conversation_interrupted(graph, graph_config)
    stream_input = (
                    Command(resume=True)
                    if interrupt_exists
                    else {"messages": [("user", message)]}
                )
    for s in graph.stream(
            input=stream_input,
            config=graph_config,
            subgraphs=True,
            stream_mode=["updates", "messages"],
        ):
        if s[1] == "updates":
            interrupt_message = s[-1].get("__interrupt__", None)
            if interrupt_message:
                yield interrupt_message[0].value
        elif isinstance(s[-1][0], AIMessageChunk):
            content = s[-1][0].content
            if isinstance(content, list) and not content:
                return
            if content:
                yield content

@app.post("/chat")
async def chat(request: Item):
    """
    Streams messages from the graph as they are produced.
    """
    thread_id = request.thread_id
    message = request.message

    graph = make_graph()

    return StreamingResponse(event_stream(graph, thread_id, message), media_type="text/event-stream")

