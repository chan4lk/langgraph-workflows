# ./src/agent/webapp.py
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from smart_goals.graph import make_graph  # Adjust import if you want a different graph
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessageChunk
from pprint import pprint

class Item(BaseModel):
    thread_id: str
    message: str

app = FastAPI()


@app.get("/hello")
def read_root():
    return {"Hello": "World"}

def event_stream(graph, thread_id, message):
    for s in graph.stream(
            input={"messages": [HumanMessage(content=message)]},
            config={"configurable": {"thread_id": thread_id}},
            subgraphs=True,
            stream_mode=["updates", "messages"],
        ):
        if s[1] == "updates":
            interrupt_message = s[-1].get("__interrupt__", None)
            if interrupt_message:
                yield interrupt_message[0].value + "\n"
        elif isinstance(s[-1][0], AIMessageChunk):
            content = s[-1][0].content
            if isinstance(content, list) and not content:
                return
            if content:
                print(f"content {content}")
                yield content + "\n"

@app.post("/chat")
async def chat(request: Item):
    """
    Streams messages from the graph as they are produced.
    """
    thread_id = request.thread_id
    message = request.message

    graph = make_graph()

    return StreamingResponse(event_stream(graph, thread_id, message), media_type="text/event-stream")

