import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime, timedelta

def draft_content(state):
    print("--- [Node] Copywriter (GPT-4o-mini) ---")
    
    track = state.get("selected_track")
    research = state.get("research_summary")
    retry_count = state.get("retry_count", 0)
    critique = state.get("critique_feedback", "")
    
    model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
    print(f"--- [Node] Copywriter ({model_name}) ---")
    
    llm = ChatOpenAI(model=model_name, temperature=0.7)
    
    # Logic for Scheduling:
    # If it's morning run, schedule for evening (18:00). If evening run, schedule for tomorrow morning.
    # Ideally, the LLM could decide, but hardcoded logic is more reliable for V1.
    now = datetime.now()
    if now.hour < 12:
        # Schedule for today at 18:00
        publish_time = now.replace(hour=18, minute=0, second=0).isoformat()
    else:
        # Schedule for tomorrow at 10:00
        publish_time = (now + timedelta(days=1)).replace(hour=10, minute=0, second=0).isoformat()

    # --- Memory Retrieval ---
    import chromadb
    from chromadb.utils import embedding_functions
    
    past_posts_examples = "No style memory available (System Restriction)."
    
    try:
        # Connect to same DB as critic with same embedding function
        embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name=embedding_model
        )
        chroma_client = chromadb.PersistentClient(path="./brain/memory_openai")
        collection = chroma_client.get_or_create_collection(name="post_history", embedding_function=openai_ef)
        # Fetch 3 randomish recent documents (peek) or query generic
        results = collection.peek(limit=3) 
        if results['documents']:
             past_posts_examples = "\n---\n".join(results['documents'])
    except Exception as e:
        print(f"⚠️ Memory disabled (Permissions/Auth Error): {e}")
        # Proceed without memory
        pass

    prompt_text = """
    You are the Community Manager for 'Futura Radio', a high-tech, cyberpunk radio station from the year 2099.
    
    Task: Write an Instagram caption for the song "{song}" by "{artist}".
    
    Context / Research:
    {research}
    
    Style Reference (Past successful posts):
    {style_context}
    
    Previous Critique (if any, fix this):
    {critique}
    
    Requirements:
    1. Tone: Visionary, energetic, sleek, futuristic.
    2. Use emojis like 🛰️, 💾, 🌌, ⚡.
    3. Include hashtags: #FuturaRadio #MusicRanking #{artist_clean}.
    4. Language: Spanish.
    5. Output ONLY the caption string.
    """
    
    prompt = ChatPromptTemplate.from_template(prompt_text)
    chain = prompt | llm
    
    response = chain.invoke({
        "song": track['name'],
        "artist": track['artist'],
        "artist_clean": track['artist'].replace(" ", ""),
        "research": research,
        "style_context": past_posts_examples,
        "critique": critique
    })
    
    caption = response.content.strip()
    
    # Generate Image Prompt for Pollinations
    image_prompt_text = f"Cyberpunk style promotional poster for {track['artist']} song {track['name']}, neon lights, futuristic city background, masterpiece, 8k, high resolution"

    return {
        "draft_caption": caption,
        "image_prompt": image_prompt_text,
        "publish_time_iso": publish_time,
        "retry_count": retry_count + 1,
        "status": "critique"
    }
