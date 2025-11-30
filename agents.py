# agents.py

import os
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool

# You can override this with an env var if you want
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


# -----------------------------
# 1. ResearchAgent
# -----------------------------
# Uses google_search to gather web info
research_agent = Agent(
    name="ResearchAgent",
    model=MODEL_NAME,
    description="Finds up-to-date information on the web using Google Search.",
    instruction=(
        "You are a research specialist.\n"
        "- Use google_search when needed to answer the user's query.\n"
        "- Return your findings as clear bullet points.\n"
        "- Include sources in parentheses after each key point."
    ),
    tools=[google_search],
)


# -----------------------------
# 2. SummarizerAgent
# -----------------------------
# Takes research notes and writes a clean summary
summarizer_agent = Agent(
    name="SummarizerAgent",
    model=MODEL_NAME,
    description="Summarizes research notes into a user-friendly answer.",
    instruction=(
        "You will receive research notes (bullets + sources).\n"
        "- Write a concise, friendly explanation for the user in Markdown.\n"
        "- Focus on clarity, not length.\n"
        "- You may include 1–2 key sources if helpful."
    ),
)


# -----------------------------
# 3. Root Agent (Coordinator)
# -----------------------------
# Orchestrates ResearchAgent + SummarizerAgent
root_agent = Agent(
    name="RootAgent",
    model=MODEL_NAME,
    description="Coordinates research and summarization into a final answer.",
    instruction=(
        "You are the coordinator of a multi-agent research assistant.\n"
        "\n"
        "Given a user question:\n"
        "1. Call the ResearchAgent tool to gather web research notes.\n"
        "2. Then call the SummarizerAgent tool, passing those notes to create a final answer.\n"
        "3. Respond to the user ONLY with the final summarized answer.\n"
    ),
    tools=[
        AgentTool(
            agent=research_agent,
            name="research_agent_tool",
            description="Use this to perform web research using Google Search."
        ),
        AgentTool(
            agent=summarizer_agent,
            name="summarizer_agent_tool",
            description="Use this to summarize research notes into a final answer."
        ),
    ],
)
