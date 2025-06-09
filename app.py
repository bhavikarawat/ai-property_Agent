from typing import Tuple

from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import create_react_agent, AgentExecutor,initialize_agent,AgentType
from langchain.tools import Tool
from tool_func import property_search
from outputparser import parser
from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env into os.environ

google_api_key = os.getenv("GOOGLE_API_KEY")



def user_input(query: str):
    # Get the property data
    properties = property_search({})
    
    summary_template = """
    You are a real estate assistant. Filter and return properties based on user requirements.
    
    Available properties:
    {property_data}
    
    User query: {user_query}
    
    Instructions:
    1. Carefully analyze each property
    2. Filter based on location and area requirements
    3. Return ONLY matching properties
    4. Use exactly this format:
    {format_instructions}
    
    Final Answer:
    """
    
    summary_prompt_template = PromptTemplate(
        input_variables=["property_data", "user_query"],
        template=summary_template,
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        }
    )

    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        google_api_key=google_api_key
    )
    
    # Create chain
    chain = (
        summary_prompt_template 
        | llm 
        | StrOutputParser()
    )
    
    # Invoke the chain
    result = chain.invoke({
        "property_data": properties,
        "user_query": query
    })
    
    try:
        # Parse the output using your parser
        return parser.parse(result)
    except Exception as e:
        return {
            "error": f"Failed to parse response: {str(e)}",
            "raw_response": result
        }


if __name__ == "__main__":
    print("Hello LangChain!")
    result = user_input(query="I am looking for a commercial property in Mumbai with an area above seven thousand square feet. What do you have available?")
    print(result)