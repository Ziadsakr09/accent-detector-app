import streamlit as st
import os
import download_audio
import re
from pathlib import Path
import analyze_audio
import time

# Configuration - Use environment variable in production
API_KEY = st.secrets["GOOGLE_API_KEY"]

def validate_url(url):
    """Validate if URL is potentially a video URL"""
    video_patterns = [
        r'youtube\.com/watch',
        r'youtu\.be/',
        r'loom\.com/',
        r'\.mp4',
        r'\.mov',
        r'\.avi',
        r'vimeo\.com/',
        r'streamable\.com/'
    ]
    return any(re.search(pattern, url, re.IGNORECASE) for pattern in video_patterns)




def main():
    st.set_page_config(
        page_title="English Accent Detector",
        page_icon="🎙️",
        layout="wide"
    )
    
    st.title("🎙️ English Accent Detection Tool")
    st.markdown("**Analyze video URLs to detect and classify English accents using AI**")
    
    # API Key check
    if not API_KEY:
        st.error("🔑 Google AI API key not configured. Please set GOOGLE_API_KEY environment variable.")
        st.stop()
    
    # Input section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        video_url = st.text_input(
            "Enter public video URL:",
            placeholder="https://www.youtube.com/watch?v=... or https://loom.com/...",
            help="Supports YouTube, Loom, Vimeo, and direct video file links"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacing
        analyze_button = st.button("🔍 Analyze Accent", type="primary", use_container_width=True)
    
    # Validation and Processing
    if analyze_button:
        if not video_url.strip():
            st.warning("⚠️ Please enter a valid video URL.")
        elif not validate_url(video_url):
            st.warning("⚠️ URL doesn't appear to be a video link. Please check the format.")
        else:
            # Progress tracking
            progress_container = st.container()
            
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Step 1: Download audio
                    status_text.info("⬇️ Downloading audio from video...")
                    progress_bar.progress(20)
                    audio_path = download_audio.download_audio(video_url)
                    
                    progress_bar.progress(40)
                    status_text.success("✅ Audio extracted successfully!")
                    
                    # Step 2: Analyze accent
                    progress_bar.progress(60)
                    result = analyze_audio.quick_audio_analysis(API_KEY, audio_path)
                    
                    progress_bar.progress(100)
                    status_text.success("🎉 Analysis complete!")
                    
                    # Clear progress indicators
                    time.sleep(1)
                    progress_bar.empty()
                    status_text.empty()
                    
                    # Display results
                    st.markdown("---")
                    st.markdown("### 📊 **Accent Analysis Results**")
                    
                    # Try to parse structured output
                    if "Accent:" in result and "Confidence:" in result:
                        lines = result.strip().split('\n')
                        for line in lines:
                            if line.strip():
                                if line.startswith("Accent:"):
                                    st.markdown(f"**🗣️ {line}**")
                                elif line.startswith("Confidence:"):
                                    st.markdown(f"**📈 {line}**")
                                elif line.startswith("Explanation:"):
                                    st.markdown(f"**💡 {line}**")
                                else:
                                    st.write(line)
                    else:
                        st.write(result)
                    
                    # Cleanup
                    try:
                        os.remove(audio_path)
                        os.rmdir(os.path.dirname(audio_path))
                    except:
                        pass  # Ignore cleanup errors
                        
                except Exception as e:
                    progress_bar.empty()
                    status_text.empty()
                    st.error(f"❌ **Error:** {str(e)}")
                    
                    # Common troubleshooting
                    with st.expander("🔧 Troubleshooting"):
                        st.markdown("""
                        **Common issues:**
                        - Video is private or restricted
                        - Video is too long (>10 minutes)
                        - No clear English speech detected
                        - Network connectivity issues
                        
                        **Try:**
                        - Using a shorter, public video
                        - Ensuring video has clear English speech
                        - Checking your internet connection
                        """)
    
    # Instructions and Examples
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 **How to Use**")
        st.markdown("""
        1. **Paste** a public video URL
        2. **Click** 'Analyze Accent' 
        3. **Wait** for processing (30-90 seconds)
        4. **View** accent classification results
        
        **Supported platforms:**
        - YouTube, Loom, Vimeo
        - Direct MP4/audio links
        - Most public video platforms
        """)
    
    with col2:
        st.markdown("### 🎯 **Sample Test URLs**")
        st.markdown("""
        Try these for testing:
        - `https://www.youtube.com/watch?v=UByw5C2d1IU`
        - Any public YouTube video
        - Public Loom recordings
        - Direct .mp4 file links
        
        **Best results with:**
        - Clear speech (minimal background noise)
        - Videos under 10 minutes
        - Single speaker preferred
        """)
    
    st.markdown("---")
    st.markdown("*🔒 This tool processes audio temporarily and doesn't store any data permanently.*")

if __name__ == "__main__":
    main()