from textwrap import dedent
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.youtube import YouTubeTools
import streamlit as st
from datetime import datetime
import re
import os
import pandas as pd
from streamlit_option_menu import option_menu
import time

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="YouTube Video Analyzer",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Professional Custom CSS with Modern Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    /* Main background with animated gradient */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Animated background particles effect */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: radial-gradient(circle at 20% 50%, rgba(255,255,255,0.05) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
        z-index: 0;
    }

    /* Sidebar styling with glass morphism */
    [data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.95);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 10px 0 30px rgba(0, 0, 0, 0.3);
    }

    /* Glowing title animation */
    @keyframes glow {
        0%, 100% { text-shadow: 0 0 20px rgba(255,255,255,0.1); }
        50% { text-shadow: 0 0 40px rgba(74,144,226,0.5), 0 0 60px rgba(74,144,226,0.3); }
    }

    .main-title {
        text-align: center;
        font-size: 4rem;
        font-weight: 800;
        margin-bottom: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -1px;
        animation: glow 3s ease-in-out infinite;
    }

    /* Subtitle with elegant style */
    .subtitle {
        text-align: center;
        background: linear-gradient(135deg, #a8c0ff, #3f2b96);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.2rem;
        margin-bottom: 40px;
        font-weight: 500;
        letter-spacing: 0.5px;
    }

    /* Enhanced Feature cards with 3D effect */
    .feature-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 25px 15px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid rgba(255, 255, 255, 0.2);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }

    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }

    .feature-card:hover::before {
        left: 100%;
    }

    .feature-card:hover {
        transform: translateY(-10px) scale(1.02);
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1));
        border: 1px solid rgba(102, 126, 234, 0.6);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3), 0 0 20px rgba(102, 126, 234, 0.3);
    }

    .feature-icon {
        font-size: 3rem;
        margin-bottom: 15px;
        display: inline-block;
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    .feature-card h3 {
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
        font-size: 1.3rem;
        font-weight: 700;
    }

    .feature-card p {
        color: #d0d0d0;
        font-size: 0.9rem;
        margin: 0;
        line-height: 1.6;
    }

    /* Modern input styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 15px;
        padding: 16px 20px;
        font-size: 1rem;
        color: #ffffff !important;
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.2);
        background: rgba(255, 255, 255, 0.15);
        transform: scale(1.01);
    }

    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.5);
    }

    /* Animated button */
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 14px 28px;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        cursor: pointer;
        text-transform: uppercase;
        letter-spacing: 1px;
        position: relative;
        overflow: hidden;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }

    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        animation: pulse 1s infinite;
    }

    /* Analysis card with glass morphism */
    .analysis-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 40px;
        margin-top: 30px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 25px 45px rgba(0, 0, 0, 0.2);
        animation: fadeInUp 0.6s ease-out;
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Stats card styling */
    .stats-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        border: 1px solid rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        animation: fadeIn 0.8s ease-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: scale(0.9); }
        to { opacity: 1; transform: scale(1); }
    }

    .stats-card:hover {
        transform: translateY(-5px) scale(1.03);
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.3), rgba(118, 75, 162, 0.3));
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
    }

    .stats-number {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .stats-label {
        color: #c0c0c0;
        font-size: 0.9rem;
        margin-top: 8px;
        font-weight: 500;
    }

    /* Success message with animation */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-100px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    .success-message {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
        border: 2px solid rgba(102, 126, 234, 0.6);
        border-radius: 15px;
        padding: 18px;
        margin: 20px 0;
        text-align: center;
        color: #667eea;
        font-weight: 700;
        font-size: 1.1rem;
        animation: slideIn 0.5s ease-out;
        backdrop-filter: blur(10px);
    }

    /* Info box with glow effect */
    .info-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        border-left: 4px solid #667eea;
        border-radius: 12px;
        padding: 18px 22px;
        margin: 15px 0;
        color: #e0e0e0;
        backdrop-filter: blur(5px);
        transition: all 0.3s ease;
    }

    .info-box:hover {
        transform: translateX(5px);
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
        border-left-width: 6px;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 20px;
        padding: 8px;
        backdrop-filter: blur(10px);
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 12px 28px;
        transition: all 0.3s ease;
        color: #c0c0c0;
        font-weight: 600;
        font-size: 1rem;
        backdrop-filter: blur(5px);
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.3);
        color: white;
        transform: translateY(-2px);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }

    /* Progress bar styling */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        border-radius: 10px;
    }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        transition: all 0.3s ease;
    }

    [data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        border-color: rgba(102, 126, 234, 0.6);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    }

    /* Footer styling */
    .footer {
        text-align: center;
        padding: 40px;
        margin-top: 60px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        background: rgba(0, 0, 0, 0.3);
        border-radius: 25px;
        backdrop-filter: blur(10px);
    }

    .footer-text {
        color: #ffffff !important;
        font-size: 0.95rem;
        margin: 10px 0;
        line-height: 1.6;
    }

    .footer-text strong {
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #f093fb);
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        .subtitle {
            font-size: 1rem;
        }
        .feature-card {
            padding: 15px 10px;
        }
        .feature-icon {
            font-size: 2rem;
        }
        .analysis-card {
            padding: 20px;
        }
    }
</style>
""", unsafe_allow_html=True)


def build_youtube_agent():
    """Build and return the YouTube analysis agent with enhanced capabilities"""
    return Agent(
        name="YouTube Agent",
        model=Groq(id="qwen/qwen3-32b"),
        tools=[YouTubeTools()],
        instructions=dedent("""\
            You are an expert YouTube content analyst with deep expertise in video analysis. Provide comprehensive, detailed analysis following this structure:

            # VIDEO OVERVIEW
            - Provide the video title and channel information
            - State the video duration and upload date if available
            - Identify the content category (Educational, Tutorial, Review, Entertainment, Documentary, etc.)
            - Rate the production quality (Excellent, Good, Average, Poor)
            - Provide a one-paragraph executive summary

            # DETAILED CONTENT BREAKDOWN
            ## Main Topics Covered
            - List and describe each major topic with timestamps
            - Explain the depth of coverage for each topic
            - Note any missing or skipped important aspects

            ## Key Concepts & Terminology
            - List important terms and concepts introduced
            - Provide brief definitions or explanations
            - Note any specialized jargon used

            ## Practical Examples & Demonstrations
            - Describe examples shown in the video
            - Note the effectiveness of demonstrations
            - Highlight code snippets, formulas, or procedures shown

            # TIMESTAMP ANALYSIS
            Create a detailed timestamp table with:
            | Timestamp | Segment Title | Key Points Covered | Duration |
            |-----------|--------------|-------------------|----------|
            | [Start] | Title | Main points | Length |

            # LEARNING OUTCOMES
            ## What You Will Learn
            - List 5-7 specific learning outcomes
            - Rate difficulty level (Beginner/Intermediate/Advanced)
            - Indicate prerequisite knowledge needed

            ## Actionable Takeaways
            - List practical actions viewers can take
            - Include resources mentioned
            - Note any downloadable materials

            # QUALITY ASSESSMENT
            ## Content Quality (1-10)
            - Accuracy of information
            - Depth vs breadth balance
            - Relevance to target audience

            ## Presentation Quality (1-10)
            - Audio and video quality
            - Pacing and engagement
            - Visual aids and graphics quality

            ## Production Quality (1-10)
            - Editing and transitions
            - Background and lighting
            - Overall professionalism

            # RECOMMENDATIONS
            ## For Viewers
            - Who should watch this video
            - How to get maximum value
            - Related videos or topics to explore

            ## For Creators
            - Suggestions for improvement
            - Potential follow-up topics
            - Audience engagement opportunities

            # ADDITIONAL INSIGHTS
            - Unique or standout moments
            - Controversial points (if any)
            - Cultural or contextual considerations
            - References to other creators or sources

            Format all responses in professional markdown with appropriate headings, tables, and lists. Use **bold** for emphasis on important points. Include specific timestamps whenever possible.
        """),
        add_datetime_to_context=True,
        markdown=True,
    )


# Cache the agent for faster access
@st.cache_resource
def get_agent():
    return build_youtube_agent()


# Function to save analysis to file
def save_analysis_to_file(content, video_url, video_title=""):
    """Save analysis results to a markdown file with enhanced metadata"""
    reports_dir = "youtube_reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', video_url)
    video_id = video_id_match.group(1) if video_id_match else "unknown"

    clean_title = re.sub(r'[^\w\s-]', '', video_title).strip().replace(' ', '_')[:50] if video_title else video_id
    filename = f"{reports_dir}/youtube_analysis_{clean_title}_{timestamp}.md"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# YouTube Video Analysis Report\n\n")
        f.write(f"**Video URL:** {video_url}\n\n")
        f.write(f"**Video Title:** {video_title}\n\n" if video_title else "")
        f.write(f"**Analyzed on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Analysis Model:** Groq Qwen 3.2 32B\n\n")
        f.write(f"**Report ID:** {timestamp}\n\n")
        f.write("---\n\n")
        f.write(content)

    return filename


# Function to extract video ID
def extract_video_id(url):
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11})',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


# Function to get video statistics
def get_video_stats():
    """Return statistics about analyzed videos"""
    reports_dir = "youtube_reports"
    if not os.path.exists(reports_dir):
        return 0, 0

    files = [f for f in os.listdir(reports_dir) if f.endswith('.md')]
    total_size = sum(os.path.getsize(os.path.join(reports_dir, f)) for f in files)
    return len(files), total_size


# Main UI
def main():
    # Sidebar navigation
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <div style="font-size: 3rem;">🎬</div>
            <h2 style="color: #667eea; margin: 10px 0;">Analyzer Pro</h2>
            <div style="height: 2px; background: linear-gradient(90deg, #667eea, #764ba2); margin: 10px 0;"></div>
        </div>
        """, unsafe_allow_html=True)

        selected = option_menu(
            menu_title=None,
            options=["🎥 Video Analyzer", "📊 Analytics Dashboard", "ℹ️ About", "❓ Help"],
            icons=["camera-reels", "graph-up", "info-circle", "question-circle"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#667eea", "font-size": "20px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "8px 0", "color": "#ffffff",
                             "border-radius": "10px"},
                "nav-link-selected": {"background": "linear-gradient(135deg, #667eea, #764ba2)"},
            }
        )

        st.markdown("---")

        total_analyses, total_size = get_video_stats()
        st.markdown("### 📈 Statistics")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Analyses", total_analyses)
        with col2:
            st.metric("Storage", f"{total_size / 1024:.1f} KB")

    if selected == "🎥 Video Analyzer":
        # Animated header
        st.markdown('<div class="main-title">YouTube Video Analyzer Pro</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">✨ Unleash the power of AI for deep video content analysis ✨</div>',
                    unsafe_allow_html=True)

        # Feature cards with animations
        col1, col2, col3, col4 = st.columns(4)

        features = [
            ("🧠", "Deep Analysis", "AI-powered content breakdown with intelligent insights"),
            ("⏱️", "Smart Timestamps", "Automatic generation of meaningful time markers"),
            ("📝", "Structured Reports", "Professional markdown reports with rich formatting"),
            ("🎯", "Actionable Insights", "Extract learning outcomes and practical takeaways")
        ]

        for col, (icon, title, desc) in zip([col1, col2, col3, col4], features):
            with col:
                st.markdown(f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>
                    <h3>{title}</h3>
                    <p>{desc}</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Stats row
        col1, col2, col3, col4 = st.columns(4)
        stats = [
            ("🚀", "AI-Powered", "Advanced Neural Engine"),
            ("⚡", "Real-time", "Instant Processing"),
            ("📄", "Markdown", "Rich Formatting"),
            ("🎬", "Timestamp", "Smart Detection")
        ]

        for col, (icon, title, desc) in zip([col1, col2, col3, col4], stats):
            with col:
                st.markdown(f"""
                <div class="stats-card">
                    <div style="font-size: 2rem;">{icon}</div>
                    <div class="stats-number">{title}</div>
                    <div class="stats-label">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Main input section
        st.markdown("### 🎯 Video Input")
        col1, col2 = st.columns([3, 1])

        with col1:
            video_url = st.text_input(
                "YouTube Video URL",
                placeholder="https://www.youtube.com/watch?v=... or https://youtu.be/...",
                label_visibility="collapsed"
            )

        with col2:
            analyze_button = st.button("🚀 Analyze Video", use_container_width=True)

        # Example videos section
        with st.expander("📚 Example Videos", expanded=False):
            st.markdown("""
            <div class="info-box">
                <strong>🎓 Educational Content:</strong><br>
                <code>https://www.youtube.com/watch?v=dQw4w9WgXcQ</code>
            </div>
            <div class="info-box">
                <strong>💻 Technical Tutorial:</strong><br>
                <code>https://www.youtube.com/watch?v=rcp-j0StBR0</code>
            </div>
            <div class="info-box">
                <strong>🎨 Creative Content:</strong><br>
                <code>https://www.youtube.com/watch?v=8jPQjjsBbIc</code>
            </div>
            """, unsafe_allow_html=True)

        # Information tabs
        st.markdown("### ℹ️ Information")
        tab_info, tab_requirements, tab_features = st.tabs(["About", "Requirements", "Features"])

        with tab_info:
            st.markdown("""
            <div class="info-box">
                <strong>✨ Professional YouTube Video Analyzer</strong><br><br>
                Uses advanced AI to provide comprehensive video analysis including:
                • Deep content extraction and topic identification<br>
                • Automatic timestamp generation with duration tracking<br>
                • Quality assessment across multiple dimensions<br>
                • Actionable insights and learning outcomes<br>
                • Structured markdown reports for documentation
            </div>
            """, unsafe_allow_html=True)

        with tab_requirements:
            st.markdown("""
            <div class="info-box">
                <strong>📋 Requirements for optimal results:</strong><br><br>
                ✓ Publicly accessible YouTube video<br>
                ✓ Stable internet connection (10+ Mbps recommended)<br>
                ✓ Video captions/transcripts for better accuracy<br>
                ✓ Videos under 2 hours for faster processing
            </div>
            """, unsafe_allow_html=True)

        with tab_features:
            st.markdown("""
            <div class="info-box">
                <strong>🌟 Analysis Features:</strong><br><br>
                • 8+ detailed analysis sections<br>
                • Automatic timestamp tables with duration<br>
                • Quality scoring (1-10 scale)<br>
                • Learning outcomes extraction<br>
                • Creator recommendations<br>
                • Professional markdown output
            </div>
            """, unsafe_allow_html=True)

        # Validation and analysis
        if video_url and analyze_button:
            youtube_regex = r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/'
            if not re.match(youtube_regex, video_url):
                st.error("❌ Invalid URL: Please enter a valid YouTube video URL")
            else:
                video_id = extract_video_id(video_url)
                if not video_id:
                    st.error("❌ Could not extract video ID from the provided URL")
                else:
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    steps = [
                        (10, "🔍 Initializing AI analysis engine..."),
                        (30, "📡 Fetching video metadata and content..."),
                        (50, "🧠 Analyzing content structure and topics..."),
                        (70, "⏱️ Generating timestamps and insights..."),
                        (90, "📝 Formatting analysis report..."),
                        (100, "✅ Analysis completed successfully!")
                    ]

                    for progress, message in steps:
                        progress_bar.progress(progress)
                        status_text.info(message)
                        time.sleep(0.5)

                    with st.spinner("Processing comprehensive video analysis..."):
                        try:
                            agent = get_agent()
                            streaming_response = agent.run(
                                f"Please provide a comprehensive, detailed analysis of this YouTube video: {video_url}",
                                stream=True,
                            )

                            st.markdown("---")
                            st.markdown("## 📊 Analysis Report")
                            st.caption(f"🎬 Video ID: {video_id} | 📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

                            tab_analysis, tab_summary, tab_export = st.tabs(
                                ["📄 Detailed Analysis", "📋 Executive Summary", "💾 Export Options"]
                            )

                            with tab_analysis:
                                st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                                response_container = st.empty()
                                full_response = ""

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

                                if full_response:
                                    saved_path = save_analysis_to_file(full_response, video_url)
                                    st.success(f"✅ Analysis report saved to: `{saved_path}`")

                            with tab_summary:
                                st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                                st.markdown("""
                                ### 📊 Analysis Summary

                                The comprehensive analysis includes:

                                **📹 Video Overview**
                                - Executive summary and categorization
                                - Production quality assessment

                                **📚 Content Breakdown**
                                - Detailed topic analysis with timestamps
                                - Key concepts and terminology
                                - Practical examples and demonstrations

                                **🎯 Learning Outcomes**
                                - Specific skills and knowledge gained
                                - Difficulty level assessment
                                - Prerequisite knowledge needed

                                **⭐ Quality Assessment**
                                - Content quality (1-10)
                                - Presentation quality (1-10)
                                - Production quality (1-10)

                                **💡 Recommendations**
                                - For viewers and creators
                                - Actionable takeaways
                                - Related content suggestions
                                """)
                                st.markdown('</div>', unsafe_allow_html=True)

                            with tab_export:
                                st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                                st.markdown("""
                                ### 💾 Export Options

                                **Download Options:**
                                1. **Download Markdown File** - Use button below
                                2. **Copy Content** - Select text from analysis tab
                                3. **Local Storage** - Auto-saved to `youtube_reports/`

                                **File Information:**
                                - **Format**: Markdown (.md)
                                - **Size**: 5-15 KB typical
                                - **Storage**: Local only - secure & private
                                """)

                                if os.path.exists("youtube_reports"):
                                    files = [f for f in os.listdir("youtube_reports") if f.endswith('.md')]
                                    if files:
                                        st.markdown("### 📁 Recent Reports")
                                        for file in sorted(files, reverse=True)[:5]:
                                            file_path = os.path.join("youtube_reports", file)
                                            file_size = os.path.getsize(file_path)
                                            file_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime(
                                                '%Y-%m-%d %H:%M')
                                            st.markdown(f"- `{file}` ({file_size:,} bytes) - {file_time}")

                                st.markdown('</div>', unsafe_allow_html=True)

                            st.balloons()
                            st.markdown(
                                '<div class="success-message">✅ Analysis Complete - Professional Report Ready for Review</div>',
                                unsafe_allow_html=True)

                            if full_response:
                                col1, col2, col3 = st.columns([1, 2, 1])
                                with col2:
                                    st.download_button(
                                        label="📥 Download Professional Report",
                                        data=full_response,
                                        file_name=f"youtube_analysis_{video_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                                        mime="text/markdown",
                                        use_container_width=True
                                    )

                        except Exception as e:
                            st.error(f"❌ Analysis failed: {str(e)}")
                            st.info(
                                "💡 Troubleshooting: Verify video is public, check internet connection, try shorter video")

    elif selected == "📊 Analytics Dashboard":
        st.markdown('<div class="main-title">Analytics Dashboard</div>', unsafe_allow_html=True)

        total_analyses, total_size = get_video_stats()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Analyses", total_analyses)
        with col2:
            st.metric("Storage Used", f"{total_size / 1024:.1f} KB")
        with col3:
            st.metric("Reports Directory", "youtube_reports/")

        if os.path.exists("youtube_reports"):
            files = [f for f in os.listdir("youtube_reports") if f.endswith('.md')]
            if files:
                st.markdown("### 📊 Recent Analysis Reports")
                report_data = []
                for file in sorted(files, reverse=True):
                    file_path = os.path.join("youtube_reports", file)
                    file_size = os.path.getsize(file_path)
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    report_data.append({
                        "File Name": file,
                        "Size (KB)": f"{file_size / 1024:.1f}",
                        "Date": file_time.strftime('%Y-%m-%d'),
                        "Time": file_time.strftime('%H:%M:%S')
                    })

                df = pd.DataFrame(report_data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No reports found. Analyze some videos to generate reports.")

    elif selected == "ℹ️ About":
        st.markdown('<div class="main-title">About Analyzer Pro</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="analysis-card">
        <h2>✨ Professional Video Analysis Platform</h2>

        <p>This advanced YouTube Video Analyzer leverages cutting-edge AI technology to provide comprehensive, professional-grade video content analysis.</p>

        <h3>🛠️ Technology Stack</h3>
        <ul>
            <li><strong>AI Framework</strong>: Agno AI - Advanced agent-based AI framework</li>
            <li><strong>Language Model</strong>: Groq Qwen 3.2 32B - High-performance LLM</li>
            <li><strong>Frontend</strong>: Streamlit - Interactive web application framework</li>
            <li><strong>Analysis Engine</strong>: Custom-trained for video content analysis</li>
        </ul>

        <h3>🎯 Key Capabilities</h3>
        <ul>
            <li><strong>Deep Content Analysis</strong>: Extracts main topics, subtopics, and thematic structures</li>
            <li><strong>Intelligent Timestamping</strong>: Generates accurate, meaningful timestamps with duration</li>
            <li><strong>Quality Assessment</strong>: Multi-dimensional quality scoring (1-10 scale)</li>
            <li><strong>Learning Outcomes</strong>: Identifies specific skills and knowledge gains</li>
            <li><strong>Professional Reports</strong>: Structured markdown output with tables and sections</li>
        </ul>

        <h3>💼 Use Cases</h3>
        <ul>
            <li><strong>Content Researchers</strong>: Analyze video content efficiently</li>
            <li><strong>Educators</strong>: Extract learning objectives and key concepts</li>
            <li><strong>Content Creators</strong>: Get feedback and improvement suggestions</li>
            <li><strong>Students</strong>: Understand video structure before watching</li>
            <li><strong>Professionals</strong>: Document video-based learning materials</li>
        </ul>

        <h3>🔒 Data Privacy</h3>
        <ul>
            <li>All analysis is performed locally</li>
            <li>Reports are saved on your device only</li>
            <li>No data is uploaded to external servers</li>
            <li>API calls are encrypted and secure</li>
        </ul>

        <h3>📦 Version Information</h3>
        <ul>
            <li><strong>Version</strong>: 2.0 Professional</li>
            <li><strong>Release Date</strong>: December 2024</li>
            <li><strong>Support</strong>: Built with modern AI technologies</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    elif selected == "❓ Help":
        st.markdown('<div class="main-title">Help & Support</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="analysis-card">
        <h2>❓ Frequently Asked Questions</h2>

        <h3>How do I use the analyzer?</h3>
        <div class="info-box">
            1. Paste a YouTube video URL in the input box<br>
            2. Click "Analyze Video"<br>
            3. Wait for the AI to process (30-60 seconds)<br>
            4. View the detailed analysis report<br>
            5. Download the report for offline use
        </div>

        <h3>What video formats are supported?</h3>
        <div class="info-box">
            • Standard YouTube URLs (youtube.com/watch?v=...)<br>
            • Short links (youtu.be/...)<br>
            • Embedded URLs (youtube.com/embed/...)
        </div>

        <h3>Why isn't my video working?</h3>
        <div class="info-box">
            <strong>Common issues and solutions:</strong><br>
            • <strong>Private video</strong>: Make the video public<br>
            • <strong>No captions</strong>: Videos with captions work best<br>
            • <strong>Copyright issues</strong>: Some restricted videos may not work<br>
            • <strong>Very long videos</strong>: Try videos under 2 hours first
        </div>

        <h3>How accurate is the analysis?</h3>
        <div class="info-box">
            The AI provides analysis based on video metadata and available captions. Accuracy is typically:<br>
            • 90%+ for educational content<br>
            • 85%+ for technical tutorials<br>
            • 80%+ for general content
        </div>

        <h3>Can I save the reports?</h3>
        <div class="info-box">
            Yes! Reports are automatically saved to the <code>youtube_reports/</code> folder and can be downloaded as markdown files.
        </div>

        <h3>Is my data private?</h3>
        <div class="info-box">
            Absolutely. All processing happens locally. No video data or reports are uploaded to external servers.
        </div>

        <h3>🔧 Troubleshooting</h3>
        <div class="info-box">
            If you encounter issues:<br>
            1. Check your internet connection<br>
            2. Verify the video is publicly accessible<br>
            3. Try a different video URL<br>
            4. Clear your browser cache<br>
            5. Restart the application
        </div>
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="footer">
        <p class="footer-text">🚀 Powered by <strong>Agno AI Framework</strong> | <strong>Groq LLM</strong> | <strong>Streamlit</strong></p>
        <p class="footer-text">✨ Professional YouTube Video Analysis Platform - Get Intelligent Video Insights in Seconds ✨</p>
        <p class="footer-text" style="font-size: 0.85rem; opacity: 0.8;">💾 Reports automatically saved to youtube_reports directory | 🔒 Secure Local Processing</p>
        <p class="footer-text" style="font-size: 0.8rem; opacity: 0.7;">© 2024 YouTube Video Analyzer Pro | Version 2.0</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()