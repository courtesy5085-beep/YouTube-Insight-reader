import os import streamlit as st from googleapiclient.discovery import build import google.generativeai as genai from urllib.parse import urlparse, parse_qs

Config

st.set_page_config(page_title='YouTube Insight Pro', layout='wide')

YOUTUBE_API_KEY = os.getenv('AIzaSyBf3XQ1_-MBEynmsglRMtnqQeFXePw-pQU') GEMINI_API_KEY = os.getenv('AIzaSyAlxQOAJ8TGp2i8PKz4azEMOqK5Eeb7pto')

if GEMINI_API_KEY: genai.configure(api_key=GEMINI_API_KEY)

Helpers

def extract_video_id(url): parsed = urlparse(url) if 'youtube.com' in parsed.netloc: return parse_qs(parsed.query).get('v', [None])[0] if 'youtu.be' in parsed.netloc: return parsed.path[1:] return None

def get_video_data(video_id): youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY) request = youtube.videos().list(part='snippet,statistics', id=video_id) response = request.execute() return response['items'][0] if response['items'] else None

def summarize(text): model = genai.GenerativeModel('gemini-2.0-flash') response = model.generate_content(f'Summarize and analyze this YouTube video metadata: {text}') return response.text

UI

st.title('🎥 YouTube Insight Pro') url = st.text_input('Paste YouTube Video URL')

if st.button('Analyze') and url: video_id = extract_video_id(url) if not video_id: st.error('Invalid YouTube URL') else: data = get_video_data(video_id) if data: snippet = data['snippet'] stats = data['statistics'] st.subheader(snippet['title']) st.write(snippet['description']) st.metric('Views', stats.get('viewCount', 0)) st.metric('Likes', stats.get('likeCount', 0))

with st.spinner('Generating AI insights...'):
            analysis = summarize(str(data))
            st.markdown('## AI Analysis')
            st.write(analysis)
    else:
        st.error('Video not found')
