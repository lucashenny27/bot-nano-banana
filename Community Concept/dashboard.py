import streamlit as st
import os
import time
import sys
from io import StringIO
from dotenv import load_dotenv
from graph import app  # Import our LangGraph agent
import json

# Load env variables
load_dotenv()

st.set_page_config(page_title="Futura Radio AI", page_icon="📻", layout="wide")

# Custom CSS for Cyberpunk vibe
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #00ff41;
    }
    .stButton>button {
        background-color: #00ff41;
        color: black;
        border-radius: 5px;
        font-weight: bold;
    }
    h1, h2, h3 {
        font-family: 'Courier New', monospace;
    }
</style>
""", unsafe_allow_html=True)

st.title("📻 Futura Radio: AI Community Manager")
st.markdown("### *Control Panel 2099*")

# Sidebar for Status
with st.sidebar:
    st.header("System Status")
    
    # Check Credentials
    openai_key = os.getenv("OPENAI_API_KEY")
    spotify_id = os.getenv("SPOTIFY_CLIENT_ID")
    
    if openai_key:
        st.success("🧠 OpenAI (Connected)")
    else:
        st.error("🧠 OpenAI (Missing Key)")
        
    if spotify_id:
        st.success("🎵 Spotify API (Connected)")
    else:
        st.warning("🎵 Spotify API (Fallback Mode)")
        
    st.info(f"Model: {os.getenv('OPENAI_MODEL_NAME', 'gpt-4o-mini')}")

# Main Logic
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📡 Operations")
    if st.button("🚀 EXECUTE DAILY WORKFLOW", use_container_width=True):
        status_box = st.status("Initializing AI Agent...", expanded=True)
        try:
            # Capture output to show logs
            # This is a simple way to show progress, heavily simplified for Streamlit
            
            status_box.write("🎵 Fetching Top 5 Ranking (Spotify/Web)...")
            # We invoke the graph
            inputs = {"retry_count": 0}
            
            # Run the graph and stream updates if possible, or just run
            # For this MVP, we run it and wait for result
            result = app.invoke(inputs)
            
            status_box.write("✅ Workflow Complete!")
            status_box.update(label="Mission Accomplished", state="complete", expanded=False)
            
            # Display Results in Session State or directly
            st.session_state['last_result'] = result
            st.rerun()
            
        except Exception as e:
            status_box.update(label="System Failure", state="error")
            st.error(f"Critical Error: {str(e)}")

with col2:
    st.subheader("💾 Last Transmission")
    if 'last_result' in st.session_state:
        res = st.session_state['last_result']
        
        # Display Image
        if res.get('image_url'):
            st.image(res['image_url'], caption="Generated Visual (Pollinations.ai)")
        
        # Display Caption
        if res.get('draft_caption'):
            st.text_area("Caption Generated", value=res['draft_caption'], height=300)
            
        # Display Research
        with st.expander("See Research Data"):
            st.write(res.get('research_summary', 'No data.'))
            
        # Display Critique
        if res.get('critique_feedback'):
            if res['critique_feedback'] == "APPROVED":
                st.success("✅ Quality Control: APPROVED")
            else:
                st.warning(f"⚠️ QC Feedback: {res['critique_feedback']}")
    else:
        st.info("No transmissions yet. Execute workflow to generate content.")

# Footer
st.markdown("---")
st.markdown("Try manually executing the agent to see the magic happen.")
