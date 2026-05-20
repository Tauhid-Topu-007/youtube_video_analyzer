import streamlit as st
from youtube_analyzer import build_youtube_agent
from datetime import datetime
import re

st.set_page_config(
    page_title="YouTube Video Analyzer",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    .main-title {
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }

    .analysis-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 10px 30px;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }

    .success-message {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title"><h1>🎬 AI YouTube Video Analyzer</h1></div>', unsafe_allow_html=True)


# Cache for fast access
@st.cache_resource
def get_agent():
    return build_youtube_agent()


agent = get_agent()

# Input box
video_url = st.text_input("📎 Enter YouTube video Link:", placeholder="https://www.youtube.com/watch?v=...")

# Example URLs hint
st.caption("💡 Example: https://www.youtube.com/watch?v=rcp-j0StBR0")

button = st.button("🚀 Analyze Video", use_container_width=True)

if video_url and button:
    # Validate YouTube URL
    youtube_regex = r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/'
    if not re.match(youtube_regex, video_url):
        st.error("❌ Please enter a valid YouTube URL")
    else:
        with st.spinner("🎬 Analyzing video... This may take a few moments"):
            try:
                # Get streaming response
                streaming_response = agent.run(
                    f"Analyze this video: {video_url}",
                    stream=True,
                )

                st.markdown("## 📋 Analysis Report")
                st.markdown('<div class="analysis-container">', unsafe_allow_html=True)

                # Create a container for streaming content
                response_container = st.empty()
                full_response = ""

                # Handle streaming response
                for chunk in streaming_response:
                    if hasattr(chunk, 'content') and chunk.content:
                        full_response += chunk.content
                        response_container.markdown(full_response)
                    elif hasattr(chunk, 'delta') and chunk.delta:
                        full_response += chunk.delta
                        response_container.markdown(full_response)
                    elif isinstance(chunk, str):
                        full_response += chunk
                        response_container.markdown(full_response)

                st.markdown('</div>', unsafe_allow_html=True)

                # Success message and download button
                if full_response:
                    st.markdown('<div class="success-message">✅ Analysis completed successfully!</div>',
                                unsafe_allow_html=True)
                    st.balloons()

                    # Download button
                    st.download_button(
                        label="📥 Download Report",
                        data=full_response,
                        file_name=f"youtube_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )

            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.info("💡 Make sure the video is publicly accessible and has captions available.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>Powered by Agno AI Framework | Groq LLM</p>
    <p>🎯 Get intelligent video insights in seconds</p>
</div>
""", unsafe_allow_html=True)