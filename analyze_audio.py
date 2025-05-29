# First install the required package:
# pip install google-generativeai
import time
import google.generativeai as genai
import streamlit as st
# Simple example
def quick_audio_analysis(api_key, audio_path):
    """Analyze audio file using Google's Gemini AI to detect English accent"""
    if not api_key:
        raise Exception("Google AI API key not provided")
    
    try:
        # Configure API
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Upload and process
        st.info("📤 Uploading audio to AI service...")
        audio_file = genai.upload_file(audio_path)
        
        # Wait for processing with timeout
        st.info("🔄 Processing audio...")
        timeout = 60  # 60 second timeout
        start_time = time.time()
        
        while audio_file.state.name == "PROCESSING":
            if time.time() - start_time > timeout:
                raise Exception("Audio processing timeout")
            time.sleep(2)
            audio_file = genai.get_file(audio_file.name)
        
        if audio_file.state.name == "FAILED":
            raise Exception("Audio processing failed")
        
        # Generate response with specific prompt for accent detection
        prompt = """
        Analyze this audio recording and provide an English accent analysis.
        
        Requirements:
        1. Classify the English accent type (e.g., British, American, Australian, Canadian, etc.)
        2. Provide a confidence score for English language proficiency (0-100%)
        3. Give a brief explanation of the accent characteristics detected
        
        Focus only on English language speakers. If the speaker is not speaking English, indicate that clearly.
        
        Format your response exactly as:
        Accent: [Classification]
        Confidence: [Score]%
        Explanation: [Brief description of accent characteristics]
        """
        
        st.info("🧠 Analyzing accent patterns...")
        response = model.generate_content([prompt, audio_file])
        
        # Cleanup
        genai.delete_file(audio_file.name)
        
        return response.text
        
    except Exception as e:
        return f"❌ Error in analysis: {str(e)}"

# Usage
if __name__ == "__main__":
    API_KEY = "AIzaSyCR90i1ICxihEroxjg3pFuZVb_yED3CSDY"
    AUDIO_FILE = "audio.mp3"
    
    result = quick_audio_analysis(API_KEY, AUDIO_FILE)
    print(result)