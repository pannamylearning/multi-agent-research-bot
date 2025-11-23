import streamlit as st
from agents import root_agent  # import the coordinator agent

st.set_page_config(page_title="Multi-Agent Research Assistant", page_icon="📚")

st.title("📚 Multi-Agent Research Assistant")
st.write(
    "Ask a research question. The root agent will coordinate a research agent "
    "and a summarizer agent to answer you."
)

user_query = st.text_area("Enter your research question:", height=120)
show_intermediate = st.checkbox("Show intermediate research findings", value=False)

if st.button("Run Research"):
    if not user_query.strip():
        st.warning("Please enter a question first.")
    else:
        with st.spinner("Running multi-agent workflow..."):
            result = root_agent.run(user_query)

        st.subheader("🧾 Final Answer")

        if isinstance(result, dict):
            # Try to pull out something meaningful
            final_answer = (
                result.get("final_summary")
                or result.get("output")
                or str(result)
            )
            st.markdown(final_answer)

            if show_intermediate:
                research_findings = result.get("research_findings")
                if research_findings:
                    st.subheader("🔍 Research Findings (from ResearchAgent)")
                    st.markdown(research_findings)
        else:
            # If the agent returns plain text
            st.markdown(result)
