from typing import TypedDict, List, Tuple, Union

from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.runnables import Runnable
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain.agents import create_tool_calling_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.services.chatbot.tools.retriever_tool import retriever_tool
from app.services.chatbot.tools.search_tool import search_tool
from app.config import settings

class GraphState(TypedDict, total=False):
    input: str
    chat_history: List[BaseMessage]
    intermediate_steps: List[Tuple[AgentAction, str]]
    agent_outcome: Union[AgentFinish, AgentAction]
    output: str

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=settings.google_api_key,
    temperature=0.3,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that answers questions about course content and can use tools."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

tools = [retriever_tool, search_tool]
agent_runnable: Runnable = create_tool_calling_agent(llm, tools, prompt)

def update_memory(state: GraphState) -> GraphState:
    if isinstance(state["agent_outcome"], AgentFinish):
        input_msg = HumanMessage(content=state["input"])
        output_msg = AIMessage(content=state["agent_outcome"].return_values["output"])
        updated_history = state.get("chat_history", []) + [input_msg, output_msg]
        return {**state, "chat_history": updated_history}
    return state


def run_agent(state: GraphState) -> GraphState:
    response = agent_runnable.invoke({
        "input": state["input"],
        "chat_history": state.get("chat_history", []),
        "intermediate_steps": state.get("intermediate_steps", [])
    })

    # Handle List ToolAgentAction
    if isinstance(response, list) and all(isinstance(r, AgentAction) for r in response):
        return {
            **state,
            "agent_outcome": response[0]
        }

    if isinstance(response, AgentFinish) or isinstance(response, AgentAction):
        return {
            **state,
            "agent_outcome": response
        }

    raise ValueError(f"Unhandled agent response: {response}")

def call_tool(state: GraphState) -> GraphState:
    action: AgentAction = state["agent_outcome"]
    tool_result = None
    for tool in tools:
        if tool.name == action.tool:
            tool_result = tool.invoke(action.tool_input)
            break

    if tool_result is None:
        tool_result = f"Tool {action.tool} not found."

    return {
        **state,
        "intermediate_steps": state.get("intermediate_steps", []) + [(action, tool_result)]
    }

def finish(state: GraphState) -> GraphState:
    res: AgentFinish = state["agent_outcome"]
    return {
        **state,
        "output": res.return_values["output"]
    }

graph = StateGraph(GraphState)
graph.add_node("agent", run_agent)
graph.add_node("tool", call_tool)
graph.add_node("memory", update_memory)
graph.add_node("final", finish)
graph.set_entry_point("agent")
graph.add_conditional_edges(
    "agent",
    lambda state: "tool" if isinstance(state.get("agent_outcome"), AgentAction) else "final"
)
graph.add_edge("tool", "agent")
graph.add_edge("final", "memory")
graph.add_edge("memory", END)

runnable_graph = graph.compile()

def ask_bot(user_input: str, chat_history=None):
    if chat_history is None:
        chat_history = []
    state = {
        "input": user_input,
        "chat_history": chat_history,
    }
    result = runnable_graph.invoke(state)
    return result["output"], result["chat_history"]
