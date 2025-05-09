from langchain.tools.retriever import create_retriever_tool

from app.services.chatbot.loader import vectordb

retriever_tool = create_retriever_tool(
    vectordb.as_retriever(),
    name="course_retriever",
    description="used to retrieve course content from the database. "
                "You can ask about course content, lessons, and other related information.",
)
