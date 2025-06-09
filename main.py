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
    summary_template = """
        You are a real estate assistant,Answer the following questions as best you can. You have access to the following tools:
        {tools}

        Use the following format:
        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}] 
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question
        Important include all the details of the properties in the result
        
        

        Begin!

        Question: {input}
        Thought:{agent_scratchpad}
    """
    tools=[
        Tool(
            name="property_search",
            func=property_search,
            description="Search for the properties based on the user criteria"
        )
    ]

    summary_prompt_template = PromptTemplate(
        input_variables=["input", "agent_scratchpad"],
        template=summary_template,
        partial_variables={
            "tools": "\n".join([f"{tool.name}: {tool.description}" for tool in tools]),
            "tool_names": ", ".join([tool.name for tool in tools]),
            # "format_instructions":parser.get_format_instructions()
        }
    )

    #initialize llm
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    
    #Initialize the agent
    agent = create_react_agent(
        tools=tools,
        llm=llm,
        prompt=summary_prompt_template,
    )
    #Wrap it with AgentExecutor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )
    result = agent_executor.invoke({
        "input": query,                 # Required by the agent
    })
    return result["output"]

if __name__ == "__main__":
    print("Hello LangChain!")
    result = user_input(query="I am looking for a commercial property in Mumbai with an area above seven thousand square feet. What do you have available?")
    print(result)