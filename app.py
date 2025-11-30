import os
import streamlit as st
from google.adk.runners import InMemoryRunner
from agents import root_agent  # Import the root coordinator agent


# ----------------------------
# 1. Setup API Key
# ----------------------------
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
else:
    st.warning("⚠ No GOOGLE_API_KEY found. Add it in Streamlit → Settings → Secrets.")


# ----------------------------
# 2. Create runner
# ----------------------------
runner = InMemoryRunner(root_agent)


# ----------------------------
# 3. Streamlit UI
# ----------------------------
st.set_page_config(page_title="Multi-Agent Research Assistant", page_icon="📚")

st.title("📚 Multi-Agent Research Assistant")
st.write("""
This app uses a **multi-agent workflow powered by Google ADK**:

- 🧠 ResearchAgent → performs Google Search  
- ✍️ SummarizerAgent → summarizes knowledge  
- 🤖 Root Agent → coordinates everything  
""")

user_query = st.text_area("🔍 Enter your research question:", height=120)
show_intermediate = st.checkbox("Show research agent output", value=False)


if st.button("🚀 Run Research"):
    if not user_query.strip():
        st.warning("Please enter a question first.")
    else:
        with st.spinner("🤖 Agents are working..."):
            try:
                # ⬇️ CORRECT INPUT FORMAT FOR google_search
                result = runner.run(input=user_query)
            except Exception as e:
                st.error(f"❌ Agent execution failed: {str(e)}")
                st.stop()

        # ----------------------------
        # Display Results
        # ----------------------------
        st.subheader("📌 Final Summary")

        if isinstance(result, dict):
            final_answer = (
                result.get("final_summary") or
                result.get("output") or
                str(result)
            )
            st.markdown(final_answer)

            if show_intermediate and "research_findings" in result:
                st.subheader("🧩 ResearchAgent Output")
                st.markdown(result["research_findings"])

        else:
            st.markdown(str(result))


# Footer
st.write("---")
st.caption("Built with ❤️ using Google ADK + Gemini 2.5 + Streamlit.")
