from duckduckgo_search import DDGS

def research_artist(state):
    print("--- [Node] Researcher (DuckDuckGo) ---")
    track = state.get("selected_track")
    if not track:
        return {"status": "error"}

    artist_name = track['artist']
    query = f"{artist_name} music artist news facts 2025"
    
    print(f"Searching for: {query}")
    
    summary_text = ""
    try:
        with DDGS() as ddgs:
            # Get 3 top results
            results = list(ddgs.text(query, max_results=3))
            for r in results:
                summary_text += f"- Title: {r['title']}\n  Snippet: {r['body']}\n\n"
    except Exception as e:
        print(f"Search failed: {e}")
        summary_text = "No specific recent news found. Relies on general knowledge."

    return {
        "research_summary": summary_text,
        "status": "drafting"
    }
