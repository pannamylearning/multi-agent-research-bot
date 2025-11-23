from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool

# Adjust this to match how you used retry_options before
retry_config = {
    "max_retries": 3,
    "timeout": 60,
}

# Research agent – uses google_search
research_agent = Agent(
    name="ResearchAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config,
    ),
    instruction=(
        "You are a specialized research agent. Use the google_search tool "
        "to find 2–3 relevant pieces of information on the given topic and "
        "present the findings with citations."
    ),
    tools=[google_search],
    output_key="research_findings",
)

# Summarizer agent – creates a short bullet list
summarizer_agent = Agent(
    name="SummarizerAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config,
    ),
    instruction=(
        "You are a summarizer. Read the provided research findings and create "
        "a concise bullet-point summary with 3–5 key points."
    ),
    output_key="final_summary",
)

# Root agent – coordinates the two agents
root_agent = Agent(
    name="ResearchCoordinator",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config,
    ),
    instruction=(
        "You are a research coordinator. Your job is to answer the user query by orchestrating a workflow:\n"
        "1. First, call the ResearchAgent tool to find relevant information on the topic.\n"
        "2. After receiving the research findings, call the SummarizerAgent tool to create a concise summary.\n"
        "3. Finally, present the final summary to the user as your response."
    ),
    tools=[
        AgentTool(research_agent),
        AgentTool(summarizer_agent),
    ],
)
