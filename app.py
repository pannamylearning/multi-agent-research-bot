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
This app uses a **multi-agent workflow** powered by Google ADK:

- 🧠 ResearchAgent → gathers information using Google Search  
- ✍️ SummarizerAgent → converts findings into short insights  
- 🧩 Root Agent → coordinates both  
""")

user_query = st.text_area("🔍 Enter your research question:", height=120)
show_intermediate = st.checkbox("Show intermediate agent results (for debugging)", value=False)

if st.button("🚀 Run Research"):
    if not user_query.strip():
        st.warning("Please enter a question first.")
    else:
        with st.spinner("🤖 Agents are working..."):
            try:
                result = runner.run(user_query)
            except Exception as e:
                st.error(f"❌ Agent execution failed: {str(e)}")
                st.stop()

        # ----------------------------
        # Display Results
        # ----------------------------

        st.subheader("📌 Final Summary")
        
        if isinstance(result, dict):
            # Try best matching key
            final_answer = (
                result.get("final_summary") or
                result.get("output") or
                result.get("response") or
                str(result)
            )
            st.markdown(final_answer)

            if show_intermediate:
                st.subheader("🧩 Agent Context Data")
                st.code(result)
                
                if "research_findings" in result:
                    st.subheader("🔎 Raw Research Output")
                    st.markdown(result["research_findings"])

        else:
            # Root agent returned string instead of dict
            st.markdown(str(result))


# Footer
st.write("---")
st.caption("Built with ❤️ using Google ADK + Streamlit + Multi-Agent Design")
