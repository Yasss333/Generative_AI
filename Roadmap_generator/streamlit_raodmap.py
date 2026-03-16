import streamlit as st
from dotenv import load_dotenv
import os
from openai import OpenAI
import requests

# -----------------------------
# Load Environment Variables
# -----------------------------

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# -----------------------------
# Initialize LLM Client
# -----------------------------

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# -----------------------------
# Tool 1: Google Search
# -----------------------------

def search_google(query):

    st.write("🔎 Searching Google...")

    url = "https://serpapi.com/search"

    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "engine": "google"
    }

    response = requests.get(url, params=params)

    data = response.json()

    results = []

    if "organic_results" in data:

        for item in data["organic_results"][:5]:

            title = item.get("title")
            link = item.get("link")

            results.append({
                "title": title,
                "link": link
            })

    return results


# -----------------------------
# Tool 2: YouTube Search
# -----------------------------

def search_youtube(topic):

    st.write("📺 Searching YouTube...")

    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "q": topic,
        "maxResults": 5,
        "part": "snippet",
        "type": "video",
        "key": YOUTUBE_API_KEY
    }

    response = requests.get(url, params=params)

    data = response.json()

    videos = []

    for item in data.get("items", []):

        title = item["snippet"]["title"]
        video_id = item["id"]["videoId"]

        link = f"https://www.youtube.com/watch?v={video_id}"

        videos.append({
            "title": title,
            "link": link
        })

    return videos


# -----------------------------
# Tool 3: Generate Roadmap
# -----------------------------

def generate_roadmap(goal, google_results, youtube_results):

    prompt = f"""
You are an expert career mentor.

Create a structured learning roadmap for:

{goal}

Use these resources as reference:

Google Articles:
{google_results}

YouTube Tutorials:
{youtube_results}

Return roadmap with sections:

1. Fundamentals
2. Intermediate
3. Advanced
4. Project Ideas (at least 5)

Also recommend useful resources.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You generate structured learning roadmaps."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# -----------------------------
# Streamlit UI
# -----------------------------

st.title("🚀 AI Roadmap Generator")

st.write("Generate a learning roadmap using AI + Google + YouTube resources.")

goal = st.text_input(
    "Enter your learning goal",
    placeholder="Example: Backend Developer, AI Engineer, MERN Stack"
)

if st.button("Generate Roadmap"):

    if goal == "":
        st.warning("Please enter a learning goal.")
    else:

        with st.spinner("Researching resources and generating roadmap..."):

            # Google search
            google_results = search_google(f"{goal} roadmap")

            st.subheader("🌐 Google Resources")

            for r in google_results:
                st.write(f"- [{r['title']}]({r['link']})")

            # YouTube search
            youtube_results = search_youtube(f"{goal} tutorial")

            st.subheader("📺 YouTube Tutorials")

            for v in youtube_results:
                st.write(f"- [{v['title']}]({v['link']})")

            # Generate roadmap
            roadmap = generate_roadmap(goal, google_results, youtube_results)

            st.subheader("📚 Generated Learning Roadmap")

            st.write(roadmap)