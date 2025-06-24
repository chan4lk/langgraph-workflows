# Import core components (1)
from langgraph.graph import StateGraph, START, END
from typing import Sequence
from dataclasses import dataclass, field
from langgraph.graph import add_messages
from typing_extensions import Annotated

from graphiti_core import Graphiti
from graphiti_core.edges import EntityEdge
from graphiti_core.nodes import EpisodeType
from graphiti_core.utils.bulk_utils import RawEpisode
from graphiti_core.utils.maintenance.graph_data_operations import clear_data

from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from typing import TypedDict, Sequence
from dataclasses import dataclass, field
from typing_extensions import Annotated
import os
from datetime import datetime
import asyncio
from langchain_core.messages import AnyMessage
from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from typing import Optional
from graphiti_core.edges import EntityEdge
from graphiti_core.llm_client import OpenAIClient, LLMConfig
# Define agent state for LangGraph
@dataclass
class State:
    messages: Annotated[Sequence[AnyMessage], add_messages] = field(
        default_factory=list
    )
    user_name: Optional[str] = None
    user_node_uuid: Optional[str] = None

# Configure Graphiti


neo4j_uri = os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
neo4j_user = os.environ.get('NEO4J_USERNAME', 'neo4j')
neo4j_password = os.environ.get('NEO4J_PASSWORD', 'password')

# Initialize the OpenAI client with the correct configuration
openai_client = ChatOpenAI(model='gpt-4o-mini', temperature=0)

# Initialize Graphiti with the client
client = Graphiti(
    neo4j_uri,
    neo4j_user,
    neo4j_password,
    llm_client=OpenAIClient(
        config=LLMConfig(
            small_model='gpt-4o-mini',
            model='gpt-4o'
        )
    )
)

def edges_to_facts_string(entities: list[EntityEdge]):
    return '-' + '\n- '.join([edge.fact for edge in entities])

@tool
async def get_user_data(query: str) -> str:
    """Search the graphiti graph for information about the user"""
    edge_results = await client.search(
        query,
        center_node_uuid=manybirds_node_uuid,
        num_results=5,
    )
    return edges_to_facts_string(edge_results)


tools = [get_user_data]
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0).bind_tools(tools)
tool_node = ToolNode(tools)

async def init_graphiti(user_name: str):
    await clear_data(client.driver)
    await client.build_indices_and_constraints()
    result = await client.add_episode(
        name='User Creation',
        episode_body=(f'{user_name} is checking the status of a order'),
        source=EpisodeType.text,
        reference_time=datetime.now(),
        source_description='Assistant',
    )
    # let's get Jess's node uuid
    nl = result.episode
    user_node_uuid = nl.uuid
    print(f"User node uuid: {user_node_uuid}")
    return user_node_uuid


async def chatbot(state: State):
    facts_string = None
    if len(state.messages) > 0:
        last_message = state.messages[-1]
        graphiti_query = f'{"Assistant" if isinstance(last_message, AIMessage) else state.user_name}: {last_message.content}'
        # search graphiti using Jess's node uuid as the center node
        # graph edges (facts) further from the Jess node will be ranked lower
        edge_results = await client.search(
            graphiti_query, center_node_uuid=state.user_node_uuid, num_results=5
        )
        facts_string = edges_to_facts_string(edge_results)

    system_message = SystemMessage(
        content=f"""You are a helpful AI assistant. Answer questions based on the provided context and tools. If you don't know the answer, say 'I don't know'.

        Facts about the user and their conversation:
        {facts_string or 'No facts about the user and their conversation'}"""
    )

    messages = [system_message] + state.messages

    response = await llm.ainvoke(messages)

    # add the response to the graphiti graph.
    # this will allow us to use the graphiti search later in the conversation
    # we're doing async here to avoid blocking the graph execution
    asyncio.create_task(
        client.add_episode(
            name='Chatbot Response',
            episode_body=f"{state.user_name}: {state.messages[-1]}\nAssistant: {response.content}",
            source=EpisodeType.message,
            reference_time=datetime.now(),
            source_description='Chatbot',
        )
    )

    return {'messages': [response]}



graph_builder = StateGraph(State)


# Define the function that determines whether to continue or not
async def should_continue(state, config):
    messages = state.messages
    last_message = messages[-1]
    # If there is no function call, then we finish
    if not last_message.tool_calls:
        return 'end'
    # Otherwise if there is, we continue
    else:
        return 'continue'


graph_builder.add_node('agent', chatbot)
graph_builder.add_node('tools', tool_node)

graph_builder.add_edge(START, 'agent')
graph_builder.add_conditional_edges('agent', should_continue, {'continue': 'tools', 'end': END})
graph_builder.add_edge('tools', 'agent')

# Initialize graph without calling init_graphiti during import
# The graph will be initialized when actually used
graph = graph_builder.compile()

async def get_initialized_graph(user_id: str = 'chandima'):
    """Get an initialized graph with Neo4j indexes created"""
    try:
        # This will create the necessary indexes if they don't exist
        print("Initializing Graphiti...")
        node_uuid = await init_graphiti(user_id)
    except Exception as e:
        print(f"Warning: Failed to initialize Graphiti: {e}")
        print("The application will continue but some features may not work properly.")
    return graph, node_uuid
