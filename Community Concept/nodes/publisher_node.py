import requests
from instagram_client import publish_instagram_post

def publish_to_instagram(state):
    print("--- [Node] Publisher (Instagram + Pollinations) ---")
    
    prompt = state.get("image_prompt")
    caption = state.get("draft_caption")
    sch_time = state.get("publish_time_iso")
    
    # 1. Generate Image URL using Pollinations.ai (No API key needed)
    # Pollinations generates image on the fly via URL parameters
    # We encode the prompt and select a model/style
    encoded_prompt = requests.utils.quote(prompt)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1080&seed=42&model=flux"
    
    print(f"Generated Image URL: {image_url}")
    print(f"Scheduling for: {sch_time}")
    
    # 2. Publish to Meta (Scheduled)
    # Note: verify if your instagram_client supports the 'scheduled_publish_time' param
    # For now we call the function. ensuring it handles the logic or we update it.
    
    result = publish_instagram_post(image_url, caption) # Publicación real activada
    
    return {
        "status": "published",
        "image_url": image_url
    }
