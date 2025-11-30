# app.py

import os
import asyncio

import streamlit as st
from google.adk.runners import InMemoryRunner
from google.genai import types

from agents import root_agent  # root_agent from agents.py


# ----------------------------
# 1. Setup API Key
# ----------------------------
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
else:
    st.warning("⚠ No GOOGLE_API_KEY found. Add it in Streamlit → Settings → Secrets.")

APP_NAME = "multi_agent_research_app"
USER_ID = "streamlit_user"


# ----------------------------
# 2. Create runner + session
# ----------------------------
# Attach the root agent to an in-memory runner
runner = InMemoryRunner(agent=root_agent, app_name=APP_NAME)

# Use the runner's session service to create a session
session_service = runner.session_service

# Create one session (reused for all questions)
session = asyncio.run(
    session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        # session_id can be omitted to auto-generate
    )
)
SESSION_ID = session.id


# ----------------------------
# 3. Streamlit UI
# ----------------------------
st.set_page_config(page_title="Multi-Agent Research Assistant", page_icon="📚")

st.title("📚 Multi-Agent Research Assistant")
st.write(
    """
This app uses a **multi-agent workflow powered by Google ADK**:

- 🧠 **ResearchAgent** → performs Google Search  
- ✍️ **SummarizerAgent** → summarizes knowledge  
- 🤖 **RootAgent** → coordinates everything  
"""
)

user_query = st.text_area("🔍 Enter your research question:", height=120)

if st.button("🚀 Run Research"):
    if not user_query.strip():
        st.warning("Please enter a question first.")
    else:
        with st.spinner("🤖 Agents are working..."):
            try:
                # Build the ADK Content message for the user input
                content = types.Content(
                    role="user",
                    parts=[types.Part(text=user_query)],
                )

                final_answer = ""

                # runner.run() yields events; grab the final response
                for event in runner.run(
                    user_id=USER_ID,
                    session_id=SESSION_ID,
                    new_message=content,
                ):
                    if (
                        event.is_final_response()
                        and event.content
                        and event.content.parts
                        and event.content.parts[0].text
                    ):
                        final_answer = event.content.parts[0].text

                if not final_answer:
                    final_answer = "I didn't receive a final response from the agent."

            except Exception as e:
                st.error(f"❌ Agent execution failed: {str(e)}")
                st.stop()

        # ----------------------------
        # Display Results
        # ----------------------------
        st.subheader("📌 Final Summary")
        st.markdown(final_answer)


# Footer
st.write("---")
st.caption("Built with ❤️ using Google ADK + Gemini 2.5 + Streamlit.")
