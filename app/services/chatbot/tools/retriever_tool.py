from langchain.tools.retriever import create_retriever_tool

from app.services.chatbot.loader import vectordb

retriever_tool = create_retriever_tool(
    vectordb.as_retriever(),
    name="course_retriever",
    description="Use this tool to retrieve relevant course content from the database. The database is a vector store that contains embeddings of course content. You can use this tool to find specific information or answer questions related to the course material.",
)
