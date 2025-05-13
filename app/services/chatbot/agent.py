from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings
from app.services.chatbot.memory import memory
from app.services.chatbot.tools.retriever_tool import retriever_tool
from app.services.chatbot.tools.search_tool import search_tool

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=settings.google_api_key,
    temperature=0.3,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that answers questions about course content and can use tools."
               "You can also search the web for information if you don't know the answer."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Tạo agent với retriever + Google search
tools = [retriever_tool, search_tool]
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)
