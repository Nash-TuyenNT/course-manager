from langchain.agents import Tool
from langchain_community.utilities import SerpAPIWrapper

search = SerpAPIWrapper()
search_tool = Tool(
    name="google_search",
    func=search.run,
    description="Used to search the web for information or answer questions when the knowledge base is not sufficient."
)
