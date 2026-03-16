from dotenv import load_dotenv
import os 
from openai import OpenAI
import requests
import json

load_dotenv()

SerpAI_API=os.getenv("SERAPI_KEY")
OPENROUTER_API_KEY=os.getenv("OPENROUTER_API_KEY")
YOUTUBE_API_KEY=os.getenv("YOUTUBE_API_KEY")


client= OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

#Tools 

def search_google(query):
    print("\n 🔎 Searching FOr your query ....", query)
    url="https://serpapi.com/search"
    parmas={
        "q":query,
        "api_key":SerpAI_API,
        "engine":"google"
    }

    respnse=requests.get(url, params=parmas   )

    data=respnse.json()

    results=[]

    if "organic_results" in data:

        for items in data["organic_results"][:5]:

            title=items.get("title")
            link=items.get("link")

            results.append( {
                "title":title,
                "link":link
            })
    return results

# Youtube Search

def search_youtube(topic):

    print(" \n 🔎 Searching for the YT video... ", topic)
    url="https://www.googleapis.com/youtube/v3/search"
    params={
        "q":topic,
        "max-len":5,
        "part":"snippet",
        type:"video",
        "key":YOUTUBE_API_KEY
    }

    response=requests.get(url,params=params)

    data=response.json()

    videos=[]

    for item in data.get("items",[]):

        title=item['snippet']['title']
        video_id=item["id"]['videoId']

        link = f"https://www.youtube.com/watch?v={video_id}"

        videos.append({
            "title":title,
            "link":link
        })

    return videos
    
# Generate roadmap using  the llm 

def genarate_roadmap(goal,google_results, youtube_results):
    print("💘 Generating you road mapp")

    prompt=f"""You are a career mentor life coach
    create a roadmap for the  the topic :{goal}
    keep yout response concise and clear 
    for your refrences :

google_articles:
{google_results}
youtube_results:
{youtube_results}

i want yout to generate  structred roadmap the stesps are 
step 1:fundamentals 
step 2:intermediate 
step 3:advanced  
step 4:project ideas atleast 5  

Also recommend learining resources 
        
        """
    
    response=client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":'system',"content":"Your are a roadmap generater"},
            {"role":'user',"content":prompt}
        ]
    )

    return response.choices[0].message.content


#main code 

def main():
    print(" \n AI ROad map Generator")
    goal = input("Enter learning goal (example: Backend Developer): ")

    # Step 1: Search Google

    google_results = search_google(f"{goal} roadmap")

    print("\nTop Google Results:\n")

    for r in google_results:
        print(r["title"], "-", r["link"])


    # Step 2: Search YouTube

    youtube_results = search_youtube(f"{goal} tutorial")

    print(type(youtube_results))
    print("\nTop YouTube Videos:\n")
    for v in youtube_results:
        print(v["title"], "-", v["link"])


    # Step 3: Generate Roadmap

    roadmap = genarate_roadmap(goal, google_results, youtube_results)

    print("\n==============================")
    print("📚 Generated Learning Roadmap")
    print("==============================\n")

    print(roadmap)


# -----------------------------------

# if __name__ == "__main__":
#     main()