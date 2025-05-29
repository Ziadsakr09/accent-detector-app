English Accent Detection Tool
A Streamlit-based tool that analyzes video URLs to detect and classify English accents using AI.
Features

✅ Accepts public video URLs (YouTube, Loom, MP4)
✅ Extracts audio automatically
✅ Classifies English accents (British, American, Australian, etc.)
✅ Provides confidence scores (0-100%)
✅ Returns detailed explanations

Quick Setup & Testing
Prerequisites

Python 3.8+
Google AI API key 
ffmpeg (for audio processing)

Installation
bash# Clone or download the script
# Install dependencies
pip install streamlit yt-dlp google-generativeai

# Set your API key (replace with your actual key)
export GOOGLE_API_KEY="your_api_key_here"
Run the App
bashstreamlit run accent_detector.py
The app will open in your browser at http://localhost:8501
Testing URLs
Try these sample URLs to test the tool:
YouTube Videos:

https://www.youtube.com/watch?v=dQw4w9WgXcQ (English speaker)
Any public YouTube video with clear English speech

Direct MP4:

Any direct link to MP4/audio files

Loom:

Public Loom recording URLs

Usage

Open the Streamlit app
Paste a public video URL
Click "Analyze Accent"
Wait for processing (30-60 seconds)
View results with accent classification and confidence score

Output Format
Accent: American English
Confidence: 85%
Explanation: Clear American pronunciation with typical vowel patterns and rhotic accent characteristics.
Technical Architecture

Audio Extraction: yt-dlp (supports 1000+ sites)
AI Analysis: Google Gemini 2.5 Pro
Interface: Streamlit web app
File Handling: Temporary file processing with cleanup



Limitations

Requires internet connection
English accents only
Processing time depends on video length
Requires valid Google AI API key
